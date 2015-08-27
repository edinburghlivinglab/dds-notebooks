import numpy as np
from scipy.spatial import Voronoi
import geojson as gj
from dds_lab.datasets import hotel, hood
from json import loads, dumps
import shapely.geometry
import shapely.ops
import shapely
from os import popen
import pandas as pd

def gen_feature_collection(ids, polygons):
    """
    Constructs geojson with areas specified by
    polygons
    """
    iterable = zip(ids, polygons)
    feature_list = []
    for i, poly in iterable:
        # print(poly)
        po = gj.Polygon([list(map(list,poly))])
        # print(po)
        feature = gj.Feature(geometry=po)
        # print(feature)
        feature['id'] = i
        feature_list.append(feature)
        # print(feature)
    return gj.FeatureCollection(feature_list)

def gen_voronoi_polygons(points):
    """
    Ouputs polygons specifying voronoi tessalation
    of points
    """
    vor = Voronoi(points)
    lines = [
        shapely.geometry.LineString(vor.vertices[line])
        for line in vor.ridge_vertices
        if -1 not in line
    ]
    # print(poly)
    pols = list()
    for pol in shapely.ops.polygonize(lines):
        tmp = list(map(list, list(pol.exterior.coords)))
        tmp.append(tmp[0])
        pols.append(tmp)
    return pols

def hotel_vor_gen():
    """
    Creates voronoi tessalation of hotel data
    """
    jstring = open(hotel + "/hotel.json", 'r').read()
    geo_hotel = loads(jstring)
    points = np.array([x["geometry"]["coordinates"] for x in geo_hotel["features"]])
    ids = [x["properties"]["id"] for x in geo_hotel["features"]]
    
    pols = gen_voronoi_polygons(points)

    vor_json = gen_feature_collection(ids, pols)
    out_json = dumps(vor_json)
    # popen()
    open(hotel + "/vor.json", 'w').write(out_json)

def neigh_vor_gen():
    """
    Creates voronoi tessalation of neighbourhood data
    """
    df = pd.read_csv(hood + "/allotments.csv")
    geo_hotel = df
    print(df)
    points = np.array([list(map(float, x.split(","))) for x in df["Location"]])
    ids = [x for x in df["Name"]]
    print(points)
    pols = gen_voronoi_polygons(points)

    vor_json = gen_feature_collection(ids, pols)
    out_json = dumps(vor_json)
    # popen()
    open(hood + "/vor.json", 'w').write(out_json)

    
if __name__ == '__main__':
    hotel_vor_gen()
