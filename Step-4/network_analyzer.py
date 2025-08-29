# network_analyzer.py
# This is the main file for your project.
# This version includes Steps 1, 2, 3, and the new code for Step 4.

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

# --- FUNCTION FROM STEP 1 (MODIFIED FOR STEP 4) ---
def parse_cisco_config(filename):
    """
    Parses a Cisco router's running configuration file to extract
    the hostname, interface details, and OSPF routing information.
    """
    try:
        with open(filename, 'r') as f:
            # Added "ospf_networks" to the dictionary structure
            router_data = {"hostname": None, "interfaces": {}, "ospf_networks": []}
            current_interface = None
            in_ospf_config = False # Flag to track if we are inside 'router ospf'

            for line in f:
                line = line.strip()
                
                if line.startswith("hostname"):
                    in_ospf_config = False # Exit OSPF section if we see a new major command
                    parts = line.split()
                    if len(parts) > 1:
                        router_data["hostname"] = parts[1]
                
                elif line.startswith("interface"):
                    in_ospf_config = False # Exit OSPF section
                    parts = line.split()
                    if len(parts) > 1:
                        current_interface = parts[1]
                        router_data["interfaces"][current_interface] = {}
                
                elif line.startswith("ip address") and current_interface:
                    parts = line.split()
                    if len(parts) == 4:
                        ip, mask = parts[2], parts[3]
                        router_data["interfaces"][current_interface] = {"ip": ip, "mask": mask}
                
                # --- NEW LOGIC FOR STEP 4: PARSING OSPF ---
                elif line.startswith("router ospf"):
                    in_ospf_config = True # We are now inside the OSPF config block
                
                elif in_ospf_config and line.startswith("network"):
                    # Example line: "network 10.1.1.0 0.0.0.255 area 0"
                    parts = line.split()
                    if len(parts) > 2:
                        network_addr = parts[1]
                        router_data["ospf_networks"].append(network_addr)
                
                elif line.startswith("!"):
                    current_interface = None
                    # We don't reset in_ospf_config here, as "!" can appear inside the section

            return router_data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# --- LOGIC FROM STEP 3 (MODIFIED FOR STEP 4) ---

config_files = [f for f in os.listdir('.') if f.endswith('.txt')]
all_router_data = [parse_cisco_config(f) for f in config_files]
all_router_data = [data for data in all_router_data if data and data['hostname']]

G = nx.Graph()

# Add a node for each router AND attach its OSPF data
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
                        print(f"✅ Link Found: {router1['hostname']} <--> {router2['hostname']} on network {r1_network}")

# --- NEW VERIFICATION STEP FOR STEP 4 ---
print("\n--- Verifying OSPF Data on Graph Nodes ---")
for node in G.nodes(data=True):
    hostname = node[0]
    data = node[1]
    print(f"Router: {hostname}, Advertised OSPF Networks: {data.get('ospf_networks', 'None')}")

print("\n--- Generating Network Topology Map ---")
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold', edge_color='gray')
plt.title("Discovered Network Topology")
plt.show()

