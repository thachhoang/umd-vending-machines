# !/usr/bin/env python3

import json


if __name__ == '__main__':
    with open('data/machines.json', 'r') as fm, open('data/buildings.json', 'r') as fb:
        machines = json.load(fm)
        buildings = json.load(fb)

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
        geodata.append(feature)

    with open('data/buildings_with_machines.json', 'w+') as f:
        json.dump(geodata, f, sort_keys=True, indent=2)
