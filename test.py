import osmnx as ox
import time
from shapely.geometry import Polygon
import os
import pandas as pd


geopath = f"./Porto.graphml"
csvpath = f"./train_1500.csv"


def parse_gps_pos(elem_str: str):
    points = []
    # remove outer pair of brackets
    elem_str_trimmed = elem_str[2:-2]
    pt_strs = elem_str_trimmed.split(f"],[")
    for pt_str in pt_strs:
        # cur_trimmed = pt_str[1:-1]
        cur_lst = pt_str.split(f",")
        for idx in range(len(cur_lst)):
            cur_lst[idx] = float(cur_lst[idx])
        points.append(cur_lst)
    return points


df15 = pd.read_csv(csvpath).head(15)
G = ox.load_graphml(geopath)
gps_pos = df15["POLYLINE"]
gps_pos = gps_pos.apply(parse_gps_pos)

gps_nodes = {}
for idx in range(len(gps_pos)):
    cur_gps_pos = gps_pos[idx]
    cur_long = []
    cur_lat = []
    for point in cur_gps_pos:
        cur_long.append(point[0])
        cur_lat.append(point[1])
    nearest_nodes = ox.distance.nearest_nodes(G, X=cur_long, Y=cur_lat)
    gps_nodes[idx] = nearest_nodes

k = 5

# Create a map of the road network using OSMnx
cur_route_raw = gps_nodes[k]
cur_route = []
prev_id = cur_route_raw[0]
for idx in range(1, len(cur_route_raw) - 1):
    if cur_route_raw[idx] != prev_id:
        cur_route.append(cur_route_raw[idx])
        prev_id = cur_route_raw[idx]
    else:
        pass
print(cur_route)

fig, ax = ox.plot.plot_graph_route(
    ox.project_graph(G),
    cur_route,
)
# for node in cur_route:
#     node_data = G.nodes[node]
#     # print(node_data)
#     ax.plot(node_data['y'], node_data['x'], 'ro', markersize=80, zorder=4)  # 'ro' for red circles as markers
#     ax.plot(node_data['x'], node_data['y'], 'ro', markersize=80, zorder=4)  # 'ro' for red circles as markers
# plt.show()
