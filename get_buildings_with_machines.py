# !/usr/bin/env python3

import json


if __name__ == '__main__':
    with open('machines.json', 'r') as fm, open('buildings.json', 'r') as fb:
        machines = json.load(fm)
        buildings = json.load(fb)

    buildings_by_id = {}
    for b in buildings:
        buildings_by_id[b['building_id']] = b

    for m in machines:
        m_id = m['building_id']
        if m_id in buildings_by_id:
            m.update(buildings_by_id.pop(m_id))

    with open('buildings_with_machines.json', 'w+') as f:
        json.dump(machines, f, sort_keys=True, indent=2)
