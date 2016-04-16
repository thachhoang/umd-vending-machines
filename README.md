# [umd-vending-machines](http://thachhoang.github.io/umd-vending-machines/)

It's exactly that.

## Generate data

Run `get_machines.py` to scrape data:

- The building coordinates from [umd.io](http://umd.io/map/#list_buildings)
- The vending machine list from [dbs.umd.edu](http://www.dbs.umd.edu/corp/vending_list.php)

The results are combined into [a GeoJSON file](data/buildings_with_machines.json) (warning: huge file).
