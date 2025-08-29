# Step-3:

We're now at a very exciting stage where your program will go from comparing two files to understanding an entire network topology automatically.

Here is the updated code for Step 3. It incorporates the powerful networkx library to build and visualize the network map. I have integrated the new logic into your existing network_analyzer.py file.

How to Execute This Code

--------------------------------------------------------------------------------------------------------------------------------------------------

## Install New Libraries:

This step requires two popular Python libraries, networkx for graph logic and matplotlib for plotting. Open your terminal and install them:

pip install networkx matplotlib

-------------------------
## Update Your Python Script:

Open your network_analyzer.py file.

Replace all the old code with the complete, updated code from the document above.

-------------------------

## Create the R3.txt Data File:

To make the topology interesting, we need a third router. In your CiscoNetworkProject folder, create a new file named R3.txt.

Paste the following configuration into R3.txt. This router connects to R2.

-------------------------

## Run the Script:

Open your terminal, navigate to your CiscoNetworkProject folder.

Run the script: python network_analyzer.py

## Expected Output

<img width="383" height="134" alt="Screenshot 2025-08-29 at 9 47 51 PM" src="https://github.com/user-attachments/assets/b32fe7d3-d63f-4e67-8046-d1dd47a42b45" />

<img width="912" height="776" alt="Screenshot 2025-08-29 at 9 48 10 PM" src="https://github.com/user-attachments/assets/debe02dc-b05f-442d-b0d1-152af5d12d22" />





