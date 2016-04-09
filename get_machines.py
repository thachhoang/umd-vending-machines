# !/usr/bin/env python3

import json
import re
import urllib.request

from bs4 import BeautifulSoup


machine_url = 'http://www.dbs.umd.edu/corp/vending_list.php'


def get_machines():
    main_html = str(urllib.request.urlopen(machine_url).read())
    buildings = []

    # Get list of buildings with machines on main page
    building_ids = sorted(re.findall(r'<a href="vending_list.php\?BldgNum=(\d+)">(.*?) \(\d+\)</a>', main_html))
    for building_id, building_name in building_ids:
        building_html = str(urllib.request.urlopen(machine_url + '?BldgNum=' + building_id).read())
        print(building_id)

        building = {
            'building_id': building_id,
            'name': building_name,
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

if __name__ == '__main__':
    with open('machines.json', 'w+') as f:
        json.dump(get_machines(), f, sort_keys=True, indent=2)
