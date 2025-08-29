# network_analyzer.py
# This is the main file for your project.
# This version includes Steps 1, 2, and the new code for Step 3.

# --- NEW IMPORTS FOR STEP 3 ---
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

# --- FUNCTION FROM STEP 1 (Unchanged) ---
def parse_cisco_config(filename):
    """
    Parses a Cisco router's running configuration file to extract
    the hostname and interface details (IP address and subnet mask).
    """
    try:
        with open(filename, 'r') as f:
            router_data = {"hostname": None, "interfaces": {}}
            current_interface = None
            for line in f:
                line = line.strip()
                if line.startswith("hostname"):
                    parts = line.split()
                    if len(parts) > 1:
                        router_data["hostname"] = parts[1]
                elif line.startswith("interface"):
                    parts = line.split()
                    if len(parts) > 1:
                        current_interface = parts[1]
                        router_data["interfaces"][current_interface] = {}
                elif line.startswith("ip address") and current_interface:
                    parts = line.split()
                    if len(parts) == 4:
                        ip, mask = parts[2], parts[3]
                        router_data["interfaces"][current_interface] = {"ip": ip, "mask": mask}
                elif line.startswith("!"):
                    current_interface = None
            return router_data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# --- NEW LOGIC FOR STEP 3: BUILDING THE TOPOLOGY MAP ---

# 1. Find all router configuration files in the current directory.
#    We assume they all end with '.txt'.
config_files = [f for f in os.listdir('.') if f.endswith('.txt')]
all_router_data = [parse_cisco_config(f) for f in config_files]
# Filter out any files that couldn't be parsed
all_router_data = [data for data in all_router_data if data and data['hostname']]

# 2. Create a graph object.
G = nx.Graph()

# 3. Add a node for each router.
for router in all_router_data:
    G.add_node(router['hostname'])

# 4. Compare every router to every other router to find links.
#    itertools.combinations gives us all unique pairs, e.g., (R1, R2), (R1, R3), (R2, R3)
print("--- Analyzing for network links between all routers ---")
for router1, router2 in itertools.combinations(all_router_data, 2):
    for r1_interface, r1_details in router1["interfaces"].items():
        if "ip" in r1_details:
            r1_network = get_network_address(r1_details["ip"], r1_details["mask"])
            for r2_interface, r2_details in router2["interfaces"].items():
                if "ip" in r2_details:
                    r2_network = get_network_address(r2_details["ip"], r2_details["mask"])
                    if r1_network == r2_network:
                        # If a link is found, add an edge to the graph
                        G.add_edge(router1['hostname'], router2['hostname'])
                        print(f"✅ Link Found: {router1['hostname']} <--> {router2['hostname']} on network {r1_network}")

# 5. Draw and display the network map.
print("\n--- Generating Network Topology Map ---")
plt.figure(figsize=(8, 6)) # Make the plot a bit larger
nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold', edge_color='gray')
plt.title("Discovered Network Topology")
plt.show()

