import osmnx as ox
import time
from shapely.geometry import Polygon
import os
import pandas as pd


def save_graph_shapefile_directional(G, filepath=None, encoding="utf-8"):
    # default filepath if none was provided
    if filepath is None:
        filepath = os.path.join(ox.settings.data_folder, "graph_shapefile")

    # if save folder does not already exist, create it (shapefiles
    # get saved as set of files)
    if not filepath == "" and not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath_nodes = os.path.join(filepath, "nodes.shp")
    filepath_edges = os.path.join(filepath, "edges.shp")

    # convert undirected graph to gdfs and stringify non-numeric columns
    gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(G)
    gdf_nodes = ox.io._stringify_nonnumeric_cols(gdf_nodes)
    gdf_edges = ox.io._stringify_nonnumeric_cols(gdf_edges)
    # We need an unique ID for each edge
    # NOTE: tuple format not supported. cannot directly use gdf_edges.index since
    # this is a tuple returned. must post process.
    gdf_edges["fid"] = gdf_edges.index
    gdf_edges["fid"] = gdf_edges["fid"].apply(lambda x: str(x))
    # save the nodes and edges as separate ESRI shapefiles
    # NOTE: may raise ValueError for invalid entry type, e.g. tuple, list, bytes
    gdf_nodes.to_file(filepath_nodes, encoding=encoding)
    gdf_edges.to_file(filepath_edges, encoding=encoding)
    pass


print("osmnx version", ox.__version__)

# # format is (long, long, lat, lat). E and N are positive, W and S are negative
# bounds = (18.029122582902115, 18.070836297501724, 59.33476653724975, 59.352622230576124)
# x1, x2, y1, y2 = bounds
# boundary_polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
# G = ox.graph_from_polygon(boundary_polygon, network_type="drive")
# start_time = time.time()
# save_graph_shapefile_directional(G, filepath="./stockholm")
# print("--- %s seconds ---" % (time.time() - start_time))

place = "Stockholm, Sweden"
G = ox.graph_from_place(place, network_type="drive", which_result=1)
save_graph_shapefile_directional(G, filepath="stockholm")
