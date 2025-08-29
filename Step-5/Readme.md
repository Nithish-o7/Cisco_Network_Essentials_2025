## Step-5:

This is the final and most rewarding step, where all the data you've gathered comes together to perform a powerful simulation.

I will now provide the complete code for your project, adding the final logic for Step 5. To make the simulation meaningful, we need a network with a redundant path. A simple chain (R1-R2-R3) isn't enough, because if a link breaks, there's no alternate route.

Therefore, I've designed the simulation around a more robust four-router square topology (R1 connects to R2 and R4, R3 connects to R2 and R4). This way, when one link fails, your program can find the alternate path.

Here is the final version of network_analyzer.py.

## How to Execute This Code

----------

## Update Your Python Script:

Open network_analyzer.py and replace all the code with the final version above.

Create and Update Configuration Files for the New Topology:

You will need four files: R1.txt, R2.txt, R3.txt, and R4.txt.

----------

## Run the Script:

Open your terminal and run python network_analyzer.py.

----------

## Expected Output:

Your terminal output will now show the full simulation story:


<img width="868" height="732" alt="Screenshot 2025-08-29 at 10 50 45 PM" src="https://github.com/user-attachments/assets/34cebd78-8dd4-44a2-ba01-12efdb15a036" />


<img width="682" height="483" alt="Screenshot 2025-08-29 at 10 51 11 PM" src="https://github.com/user-attachments/assets/6d594342-0d86-498a-a435-410caf122d4f" />

