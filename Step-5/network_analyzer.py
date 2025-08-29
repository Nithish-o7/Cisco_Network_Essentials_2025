# network_analyzer.py
# This is the final version of your project, including all 5 steps.

import os
import itertools
import networkx as nx
import matplotlib.pyplot as plt

# --- FUNCTION FROM STEP 2 (Unchanged) ---
def get_network_address(ip, mask):
    """
    Calculates the network address from an IP address and a subnet mask.
    """
    ip_parts = ip.split('.')
    mask_parts = mask.split('.')
    network_parts = [str(int(ip_parts[i]) & int(mask_parts[i])) for i in range(4)]
    return ".".join(network_parts)

# --- FUNCTION FROM STEP 4 (Unchanged) ---
def parse_cisco_config(filename):
    """
    Parses a Cisco router's running configuration file to extract
    the hostname, interface details, and OSPF routing information.
    """
    try:
        with open(filename, 'r') as f:
            router_data = {"hostname": None, "interfaces": {}, "ospf_networks": []}
            current_interface = None
            in_ospf_config = False
            for line in f:
                line = line.strip()
                if line.startswith("hostname"):
                    in_ospf_config = False
                    parts = line.split()
                    if len(parts) > 1:
                        router_data["hostname"] = parts[1]
                elif line.startswith("interface"):
                    in_ospf_config = False
                    parts = line.split()
                    if len(parts) > 1:
                        current_interface = parts[1]
                        router_data["interfaces"][current_interface] = {}
                elif line.startswith("ip address") and current_interface:
                    parts = line.split()
                    if len(parts) == 4:
                        ip, mask = parts[2], parts[3]
                        router_data["interfaces"][current_interface] = {"ip": ip, "mask": mask}
                elif line.startswith("router ospf"):
                    in_ospf_config = True
                elif in_ospf_config and line.startswith("network"):
                    parts = line.split()
                    if len(parts) > 2:
                        network_addr = parts[1]
                        router_data["ospf_networks"].append(network_addr)
                elif line.startswith("!"):
                    current_interface = None
            return router_data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# --- LOGIC FROM STEP 3 & 4 (Unchanged) ---

config_files = [f for f in os.listdir('.') if f.endswith('.txt')]
all_router_data = [parse_cisco_config(f) for f in config_files]
all_router_data = [data for data in all_router_data if data and data['hostname']]

G = nx.Graph()

for router in all_router_data:
    G.add_node(router['hostname'], ospf_networks=router['ospf_networks'])

print("--- Analyzing for network links between all routers ---")
for router1, router2 in itertools.combinations(all_router_data, 2):
    for r1_interface, r1_details in router1["interfaces"].items():
        if "ip" in r1_details:
            r1_network = get_network_address(r1_details["ip"], r1_details["mask"])
            for r2_interface, r2_details in router2["interfaces"].items():
                if "ip" in r2_details:
                    r2_network = get_network_address(r2_details["ip"], r2_details["mask"])
                    if r1_network == r2_network:
                        G.add_edge(router1['hostname'], router2['hostname'])
                        print(f"✅ Link Found: {router1['hostname']} <--> {router2['hostname']}")

# --- NEW LOGIC FOR STEP 5: SIMULATING FAILURE ---

print("\n--- Running Network Failure Simulation ---")

# Define the start and end points for our traffic path
source_node = 'R1'
dest_node = 'R3'

# 1. Calculate and display the original shortest path
try:
    original_path = nx.shortest_path(G, source=source_node, target=dest_node)
    print(f"Original shortest path from {source_node} to {dest_node}: {' -> '.join(original_path)}")
except nx.NetworkXNoPath:
    print(f"No path exists between {source_node} and {dest_node} initially.")
    original_path = None

# 2. Define the link to fail and simulate the failure
if original_path:
    # Let's fail a link that is part of the original path
    node_to_fail_1 = original_path[0] # R1
    node_to_fail_2 = original_path[1] # R2
    print(f"\n💥 Simulating link failure between {node_to_fail_1} and {node_to_fail_2}...\n")
    G.remove_edge(node_to_fail_1, node_to_fail_2)

    # 3. Recalculate the path on the modified graph
    try:
        new_path = nx.shortest_path(G, source=source_node, target=dest_node)
        print(f"✅ Reroute successful!")
        print(f"New shortest path from {source_node} to {dest_node}: {' -> '.join(new_path)}")
    except nx.NetworkXNoPath:
        print(f"❌ Reroute failed. No path now exists between {source_node} and {dest_node}.")

# 4. Draw the final (post-failure) network map
print("\n--- Generating Final Network Topology Map (Post-Failure) ---")
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold', edge_color='gray')
plt.title("Network Topology After Link Failure")
plt.show()

