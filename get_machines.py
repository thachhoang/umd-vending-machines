# !/usr/bin/env python3

import argparse
import json
import re
import urllib.request

from bs4 import BeautifulSoup


def get_machines(machine_url):
    main_html = str(urllib.request.urlopen(machine_url).read())
    buildings = []

    # Get list of buildings with machines on main page
    building_ids = sorted(re.findall(r'<a href="vending_list.php\?BldgNum=(\d+)">(.*?) \(\d+\)</a>', main_html))
    for building_id, building_name in building_ids:
        building_url = machine_url + '?BldgNum=' + building_id
        building_html = str(urllib.request.urlopen(building_url).read())
        print(building_id)

        building = {
            'building_id': building_id,
            'name': building_name,
            'url': building_url,
        }
        buildings.append(building)

        parsed_html = BeautifulSoup(building_html, 'html.parser')
        t = parsed_html.body.find('table', border='1', bordercolor='#333366')
        locations = []

        # Only look at direct children, because there are nested tables
        # Skip first row (header)
        for row in t.find_all('tr', recursive=False)[1:]:
            location = row.find('td', align=re.compile('center')).string
            machines = []
            for li in row.find_all('li'):
                m = re.match(r'(.*) \((\d+)\)', li.string)
                machines.append({
                    'name': m.group(1),
                    'count': int(m.group(2)),
                })

            # print(location + ': ' + str(machines))
            locations.append({
                'location': location,
                'machines': machines,
            })

        building['locations'] = locations

        # first building only
        # break

    return buildings


def get_buildings(building_url):
    data = urllib.request.urlopen(building_url).read().decode('utf8')
    return json.loads(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch and process the UMD vending machine locations.')
    parser.add_argument('-b', action='store_true', help='reload building data')
    parser.add_argument('-m', action='store_true', help='reload machine data')
    args = parser.parse_args()

    # Buildings
    building_file = 'data/buildings.json'
    if args.b:
        building_url = 'http://api.umd.io/v0/map/buildings'
        buildings = get_buildings(building_url)
        with open(building_file, 'w+') as f:
            json.dump(buildings, f, sort_keys=True, indent=2)
        print('Reloaded buildings from ' + building_url)
    else:
        with open(building_file, 'r') as f:
            buildings = json.load(f)
        print('Using cached buildings at ' + building_file)

    # Machines
    machine_file = 'data/machines.json'
    if args.m:
        machine_url = 'http://www.dbs.umd.edu/corp/vending_list.php'
        machines = get_machines(machine_url)
        with open(machine_file, 'w+') as f:
            json.dump(machines, f, sort_keys=True, indent=2)
        print('Reloaded machines from ' + machine_url)
    else:
        with open(machine_file, 'r') as f:
            machines = json.load(f)
        print('Using cached machines at ' + machine_file)

    # Combine!
    buildings_by_id = {}
    for b in buildings:
        buildings_by_id[b['building_id']] = b

    geodata = []
    for m in machines:
        m_id = m['building_id']
        if m_id in buildings_by_id:
            m.update(buildings_by_id.pop(m_id))
        feature = {
            'type': 'Feature',
            'properties': m,
        }
        if 'lat' in m and 'lng' in m:
            feature.update({
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        float(m['lng']),
                        float(m['lat']),
                    ],
                },
            })
            del m['lng']
            del m['lat']
        geodata.append(feature)

    result_file = 'data/buildings_with_machines.json'
    with open(result_file, 'w+') as f:
        json.dump(geodata, f, sort_keys=True, indent=2)
    print('Result: ' + result_file)
