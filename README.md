# [umd-vending-machines](http://thachhoang.github.io/umd-vending-machines/)

It's exactly that.

## Generate data

- Run `get-buildings.sh` to get building coordinates from [umd.io](http://umd.io/map/#list_buildings).
- Run `get_machines.py` to scrape [the vending machine list](http://www.dbs.umd.edu/corp/vending_list.php).
- Run `get_buildings_with_machines.py` to combine the above two into [a GeoJSON file](data/buildings_with_machines.json) (warning: huge file).
