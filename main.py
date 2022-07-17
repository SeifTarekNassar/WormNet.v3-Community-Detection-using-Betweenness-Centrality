
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm



# plt.axis("off")
# plt.show()


G = nx.read_edgelist("WormNet.v3.benchmark.txt")
nx.draw_networkx(G,
    with_labels=False,
    edge_color="gainsboro",
    alpha=0.4,)
# # # remove low-degree nodes (nodes with degree less than 10)
low_degree = [n for n, d in G.degree() if d < 10]
G.remove_nodes_from(low_degree)

# get the largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)


# compute centrality
centrality = nx.betweenness_centrality(H, k=10, endpoints=True)

# compute community structure
lpc = nx.community.label_propagation_communities(H)
community_index = {n: i for i, com in enumerate(lpc) for n in com}


fig, ax = plt.subplots(figsize=(20, 15))
pos = nx.spring_layout(H, k=0.15, seed=4572321)
node_color = [community_index[n] for n in H]
node_size = [v * 20000 for v in centrality.values()]
nx.draw_networkx(
    H,
    pos=pos,
    with_labels=False,
    node_color=node_color,
    node_size=node_size,
    edge_color="gainsboro",
    alpha=0.4,
)


font = {"color": "k", "fontweight": "bold", "fontsize": 20}
ax.set_title("Gene association network using Betweeness Centrality", font)
font["color"] = "r"
ax.margins(0.1, 0.05)
fig.tight_layout()
plt.axis("off")
plt.show()

print("Modelarity = ")
print(nx_comm.modularity(H, nx_comm.label_propagation_communities(H)))
print("Average clustering coefficient")
print(nx.average_clustering(H))