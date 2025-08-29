# network_analyzer.py
# This is the main file for your project.
# This version includes Step 1 and the new code for Step 2.

# --- NEW FUNCTION FOR STEP 2 ---
def get_network_address(ip, mask):
    """
    Calculates the network address from an IP address and a subnet mask.

    Args:
        ip (str): The IP address (e.g., "10.1.1.1").
        mask (str): The subnet mask (e.g., "255.255.255.0").

    Returns:
        str: The calculated network address (e.g., "10.1.1.0").
    """
    ip_parts = ip.split('.')
    mask_parts = mask.split('.')
    
    # Perform a bitwise AND operation between each part of the IP and the mask
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
                        ip = parts[2]
                        mask = parts[3]
                        router_data["interfaces"][current_interface] = {"ip": ip, "mask": mask}
                
                elif line.startswith("!"):
                    current_interface = None

            return router_data

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# --- NEW LOGIC FOR STEP 2: FINDING LINKS ---

# 1. Parse the configuration for two different routers.
#    Make sure you have created both R1.txt and R2.txt.
r1_data = parse_cisco_config("R1.txt")
r2_data = parse_cisco_config("R2.txt")

# 2. Check if both files were parsed successfully before proceeding.
if r1_data and r2_data:
    print("--- Analyzing for network links between routers ---")
    
    # 3. Use nested loops to compare every interface from R1 with every interface from R2.
    for r1_interface, r1_details in r1_data["interfaces"].items():
        # Check if the interface has an IP address.
        if "ip" in r1_details:
            r1_network = get_network_address(r1_details["ip"], r1_details["mask"])

            for r2_interface, r2_details in r2_data["interfaces"].items():
                if "ip" in r2_details:
                    r2_network = get_network_address(r2_details["ip"], r2_details["mask"])

                    # 4. If the network addresses match, we've found a direct connection!
                    if r1_network == r2_network:
                        print(f"✅ LINK FOUND!")
                        print(f"  - {r1_data['hostname']} Interface: {r1_interface} ({r1_details['ip']})")
                        print(f"  - {r2_data['hostname']} Interface: {r2_interface} ({r2_details['ip']})")
                        print(f"  - On Network: {r1_network}")
                        print("-------------------------------------------------")

