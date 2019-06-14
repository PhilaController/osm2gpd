# osm2gpd

A lightweight Python tool to scrape features from OpenStreetMaps' API and return a geopandas GeoDataFrame

## Installation

Via conda:

```
conda install -c controllerphl osm2gpd
```

Via PyPi:

```
pip install osm2gpd
```

## Example

```python
    import osm2gpd

    # get all subway stations within Philadelphia
    philadelphia_bounds = [-75.28030675,  39.86747186, -74.95574856,  40.13793484]
    subway = osm2gpd.get(*philadelphia_bounds, where="station=subway")

    # get all data tagged with "station" that aren't subway stations
    not_subway = osm2gpd.get(*philadelphia_bounds, where=["station", "station!=subway"])
```
