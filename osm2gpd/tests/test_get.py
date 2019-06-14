import osm2gpd
import pytest

philadelphia_bounds = [-75.28030675, 39.86747186, -74.95574856, 40.13793484]


def test_where():
    gdf = osm2gpd.get(*philadelphia_bounds, where="station=subway")
    assert (gdf["station"] == "subway").all()


def test_multiple_where():
    gdf = osm2gpd.get(*philadelphia_bounds, where=["station", "station!=subway"])
    assert (gdf["station"] != "subway").all()


def test_bad_where():
    bad_where = "subway$station"
    with pytest.raises(Exception):
        gdf = osm2gpd.get(*philadelphia_bounds, where=bad_where)


def test_no_data():
    with pytest.raises(RuntimeError):
        gdf = osm2gpd.get(
            *philadelphia_bounds, where=["station=subway", "shop=dry_cleaning"]
        )
