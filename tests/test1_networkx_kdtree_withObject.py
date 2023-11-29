import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import open3d as o3d
import laspy
import time

# Read the LAS file and convert it into a point cloud
las_file = laspy.read("StreetLight_FlyOver.las")
#12.22
#las_file = laspy.read("House_FlyOver.las")
#14.97
#las_file = laspy.read("Tree_FlyOver.las")
#14.59
points = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()

# Timer starts
start_time = time.time()

# k-d Tree Data Structure
class Node:
    def __init__(self, points, depth=0, max_depth=10, max_points=8):
        self.points = points
        self.axis = depth % 3  # Choose axis based on depth
        self.depth = depth
        self.children = []
        self.id = np.random.randint(1e4)  # Assign unique identifier for each node

        if len(points) > max_points and depth < max_depth:
            self.split()

    def split(self):
        sorted_points = sorted(self.points, key=lambda point: point[self.axis])
        median_idx = len(sorted_points) // 2
        median_point = sorted_points[median_idx]

        left_points = sorted_points[:median_idx]
        right_points = sorted_points[median_idx+1:]

        if left_points:
            self.children.append(Node(left_points, self.depth+1))
        if right_points:
            self.children.append(Node(right_points, self.depth+1))

# Create k-d Tree with the points from the LAS file
root = Node(points)

# Visualize k-d tree structure of Point Cloud
def kdtree_visualization(graph, node, node_id):
    for child in node.children:
        child_id = child.id
        graph.add_node(child_id)
        graph.add_edge(node_id, child_id)
        kdtree_visualization(graph, child, child_id)

graph = nx.Graph()
root_id = root.id

graph.add_node(root_id)
kdtree_visualization(graph, root, root_id)

degrees = dict(nx.degree(graph))
normalized_degrees = [(d - min(degrees.values())) / (max(degrees.values()) - min(degrees.values())) for d in degrees.values()]

cmap = plt.get_cmap('coolwarm')
nx.draw(graph, pos=nx.spring_layout(graph),
        nodelist=degrees.keys(),
        node_size=[s * 50 for s in degrees.values()],
        node_color=[cmap(c) for c in normalized_degrees])

# Timer stops
end_time = time.time()

print('Performance: ', end_time - start_time, '\n')

plt.show()
