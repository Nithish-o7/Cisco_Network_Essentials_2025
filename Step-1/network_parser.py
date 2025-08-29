# network_analyzer.py
# This is the main file for your project.
# We will add more code to this file in the next steps.

def parse_cisco_config(filename):
    """
    Parses a Cisco router's running configuration file to extract
    the hostname and interface details (IP address and subnet mask).

    Args:
        filename (str): The path to the configuration file.

    Returns:
        dict: A dictionary containing the router's hostname and a nested
              dictionary of its interfaces and their IP information.
              Returns None if the file cannot be opened.
    """
    try:
        with open(filename, 'r') as f:
            # This dictionary will hold all the info for one router
            router_data = {"hostname": None, "interfaces": {}}
            current_interface = None # Used to track which interface section we are in

            for line in f:
                # Clean up the line by removing leading/trailing whitespace
                line = line.strip()

                # --- Find the hostname ---
                if line.startswith("hostname"):
                    # The line looks like "hostname R1". We split it and take the second part.
                    parts = line.split()
                    if len(parts) > 1:
                        router_data["hostname"] = parts[1]
                
                # --- Find an interface section ---
                elif line.startswith("interface"):
                    # The line looks like "interface GigabitEthernet0/0".
                    parts = line.split()
                    if len(parts) > 1:
                        current_interface = parts[1]
                        # Create a new entry for this interface
                        router_data["interfaces"][current_interface] = {}

                # --- Find the IP address for the current interface ---
                # This check is only valid if we are inside an interface block (current_interface is not None)
                elif line.startswith("ip address") and current_interface:
                    parts = line.split()
                    # The line looks like "ip address 10.1.1.1 255.255.255.0"
                    # We need to make sure it's a valid IP address line, not something else.
                    if len(parts) == 4:
                        ip = parts[2]
                        mask = parts[3]
                        # Add the IP and mask to the dictionary for the current interface
                        router_data["interfaces"][current_interface] = {"ip": ip, "mask": mask}
                
                # --- If we see a "!", it often means the end of an interface section ---
                elif line.startswith("!"):
                    current_interface = None # Reset the current interface tracker

            return router_data

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# --- How to Use and Test This Function ---

# 1. First, create a file named 'R1.txt' in the same directory as this script.
#    Paste the sample router configuration into that file.

# 2. Call the function with the filename.

r1_info = parse_cisco_config("R1.txt")

# 3. Print the result to see if it worked.
if r1_info:
    print("--- Successfully Parsed Router Config ---")
    print(f"Hostname: {r1_info['hostname']}")
    for interface, details in r1_info['interfaces'].items():
        # We only print interfaces that have IP addresses assigned
        if "ip" in details:
            print(f"  Interface: {interface}")
            print(f"    IP Address: {details['ip']}")
            print(f"    Subnet Mask: {details['mask']}")
    print("------------------------------------")
