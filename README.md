# osm2gpd

[![Build Status](https://travis-ci.org/PhiladelphiaController/osm2gpd.svg?branch=master)](https://travis-ci.org/PhiladelphiaController/osm2gpd)
[![Coverage Status](https://coveralls.io/repos/github/PhiladelphiaController/osm2gpd/badge.svg?branch=master)](https://coveralls.io/github/PhiladelphiaController/osm2gpd?branch=master)
[![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/download/releases/3.6.0/) 
![t](https://img.shields.io/badge/status-stable-green.svg) 
[![](https://img.shields.io/github/license/PhiladelphiaController/osm2gpd.svg)](https://github.com/PhiladelphiaController/osm2gpd/blob/master/LICENSE)
[![PyPi version](https://img.shields.io/pypi/v/osm2gpd.svg)](https://pypi.python.org/pypi/osm2gpd/) 
[![Anaconda-Server Badge](https://anaconda.org/controllerphl/osm2gpd/badges/version.svg)](https://anaconda.org/controllerphl/osm2gpd)

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
