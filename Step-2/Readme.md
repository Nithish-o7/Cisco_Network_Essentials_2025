# Step-2

I will now provide the updated code. We will add a new, crucial function called ` get_network_address ` and then use it to compare two router configurations. This new code builds directly on top of what you already have.

Here is the updated network_analyzer.py script. I've included the previous function and added the new logic for link discovery.

## How to Execute This Code
## Update Your Python Script:

Open your network_analyzer.py file.

Replace all the old code with the complete, updated code from the document above.

## Create the R2.txt Data File:

In your CiscoNetworkProject folder, create a new file named R2.txt.

Copy and paste the following configuration into R2.txt. Notice that its GigabitEthernet0/0 interface is on the same network as R1's GigabitEthernet0/0.

## Run the Script:

Open your terminal or command prompt and make sure you are in the CiscoNetworkProject folder.

Run the script: python network_analyzer.py

## Expected Output:

<img width="393" height="239" alt="Screenshot 2025-08-29 at 9 23 21 PM" src="https://github.com/user-attachments/assets/5e418fac-a00e-4d1f-9073-b1e2407246e6" />
