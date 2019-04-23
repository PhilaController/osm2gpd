import pandas as pd
import geopandas as pd
import requests

OSM_ENDPOINT = "http://www.overpass-api.de/api/interpreter"


def _format_node(e):
    """
    Internal function to format a node element into a dictionary.
    """

    ignored_tags = [
        "source",
        "source_ref",
        "source:ref",
        "history",
        "attribution",
        "created_by",
        "tiger:tlid",
        "tiger:upload_uuid",
    ]

    node = {"id": e["id"], "lat": e["lat"], "lon": e["lon"]}

    if "tags" in e:
        for t, v in list(e["tags"].items()):
            if t not in ignored_tags:
                node[t] = v

    return node


def _query_osm(query):
    """
    Internal function to make a request to OSM and return the parsed JSON.
    
    Parameters
    ----------
    query : str
        A string in the Overpass QL format.
    
    Returns
    -------
    data : dict
    """
    req = requests.get(OSM_ENDPOINT, params={"data": query})
    req.raise_for_status()

    return req.json()


def _build_node_query(lng_min, lat_min, lng_max, lat_max, tags={}):
    """
    Internal function that build the string for a node-based OSM query.
    
    Parameters
    ----------
    lng_min, lat_min, lng_max, lat_max : float
    tags : dict
        key/value node tags to filter the search;
        See http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
        for information about OSM Overpass queries
        and http://wiki.openstreetmap.org/wiki/Map_Features
        for a list of tags.
    
    Returns
    -------
    query : str
    """
    assert isinstance(tags, dict)
    tags = "".join("[{k}={v}]".format(k=k, v=v) for (k, v) in tags.items())

    query_fmt = (
        "[out:json];"
        "("
        "  node"
        "  {tags}"
        "  ({lat_min},{lng_min},{lat_max},{lng_max});"
        ");"
        "out;"
    )

    return query_fmt.format(
        lat_min=lat_min, lng_min=lng_min, lat_max=lat_max, lng_max=lng_max, tags=tags
    )


def get(lng_min, lat_min, lng_max, lat_max, tags={}):
    """
    Search for OSM nodes within a bounding box that match given tags.
    
    Parameters
    ----------
    lng_min, lat_min, lng_max, lat_max : float
        the bounding box to search within

    tags : dict
        key/value node tags to filter the search;
        See http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
        for information about OSM Overpass queries
        and http://wiki.openstreetmap.org/wiki/Map_Features
        for a list of tags.
    
    Returns
    -------
    nodes : geopandas.GeoDataFrame
    """
    node_data = _query_osm(
        _build_node_query(lng_min, lat_min, lng_max, lat_max, tags=tags)
    )

    if len(node_data["elements"]) == 0:
        raise RuntimeError("OSM query results contain no data.")

    # make the GeoDataFrame
    nodes = [process_node(n) for n in node_data["elements"]]
    df = pd.DataFrame.from_records(nodes, index="id")

    # return as a GeoDataFrame
    df["geometry"] = df.apply(lambda row: Point(row["lon"], row["lat"]), axis=1)
    return gpd.GeoDataFrame(df, geometry="geometry", crs={"init": "epsg:4326"})

