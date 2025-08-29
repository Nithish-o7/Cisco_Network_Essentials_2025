# 🔗 Network Topology Parser & Visualizer

This project is a **Python-based tool** that *parses router configuration files*, discovers **network links**, and visualizes the complete **network topology**.  
It also provides **OSPF analysis** and allows simulating *link failures* to study **network resilience**.

---

## 📌 Features
✨ The project provides the following capabilities:

- 📂 **Parse router configuration files** (`R1.txt`, `R2.txt`, `R3.txt`).
- 🖥️ **Extract details**:
  - 🏷️ *Router hostname*
  - 🌐 *Interfaces, IP addresses, and subnet masks*
  - 📡 *OSPF advertised networks*
- 🔍 **Discover direct links** between routers.
- 🗺️ **Build and visualize** the network graph using *NetworkX* + *Matplotlib*.
- ⚡ **Simulate link failures** and recalculate shortest paths.

---

## 🛠️ Installation
Follow these steps to set up the project:

1. 📥 **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/network-parser.git
   cd network-parser
