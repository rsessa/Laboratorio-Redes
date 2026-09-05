import os
import sys

# Ensure Graphviz bin is in PATH for Windows
conda_bin = r"C:\Users\Richard\miniconda3\Library\bin"
if os.path.exists(conda_bin) and conda_bin not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + conda_bin

from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Router, Switch, VPN
from diagrams.onprem.network import Internet

os.makedirs("docs/img", exist_ok=True)

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "spline",
}

def generate_topology_es():
    with Diagram("Topologia Fisica y Logica - MikroTik Multi-Site", 
                 filename="docs/img/topologia_red", 
                 show=False, 
                 direction="LR", 
                 graph_attr=graph_attr):
        
        with Cluster("Sede Central (HQ)"):
            lan_hq = Switch("LAN HQ\n10.10.0.1/24")
            hq_core = Router("hq-core-01\nhAP ac2\nRID: 10.255.255.2")
            hq_edge = Router("hq-edge-01\nhEX\nRID: 10.255.255.1")
            lan_hq - hq_core
            hq_core >> Edge(label="10.1.0.0/30\nCoste 10", color="#2563eb") >> hq_edge

        with Cluster("Plano WAN & Overlay Cifrado"):
            wan = Internet("WAN Publica\n198.51.100.0/30")
            vpn = VPN("Tunel gre-vpn (IPsec HW)\n10.100.0.0/30\nCoste 10")

        with Cluster("Sucursal (Branch)"):
            br_edge = Router("branch-edge-01\nhAP ac2\nRID: 10.255.255.3")
            br_core = Router("branch-core-01\nhEX\nRID: 10.255.255.4")
            lan_br = Switch("LAN Branch\n10.30.0.1/24")
            br_edge >> Edge(label="10.2.0.0/30\nCoste 10", color="#2563eb") >> br_core
            br_core - lan_br

        with Cluster("Gestion Fuera de Banda (OOB) - 10.99.0.0/24"):
            oob = Router("oob-master\n192.168.1.210 ↔ 10.99.0.1")

        # Conexiones WAN
        hq_edge >> Edge(label="ether1 (.1)", color="#475569") >> wan
        wan >> Edge(label="ether1 (.2)", color="#475569") >> br_edge

        # Overlay VPN
        hq_edge >> Edge(label="IPsec HW", style="dashed", color="#0284c7") >> vpn
        vpn >> Edge(label="IPsec HW", style="dashed", color="#0284c7") >> br_edge

        # Enlace Standby Directo Core-to-Core
        hq_core >> Edge(label="Linea Privada Directa (ether2)\n10.255.0.0/30 · Coste 50 (STANDBY)", color="#ea580c", style="bold") >> br_core

        # Enlaces OOB
        hq_edge >> Edge(label=":2206", style="dotted", color="#6366f1") >> oob
        hq_core >> Edge(label=":2203", style="dotted", color="#6366f1") >> oob
        br_edge >> Edge(label=":2204", style="dotted", color="#6366f1") >> oob
        br_core >> Edge(label=":2205", style="dotted", color="#6366f1") >> oob

def generate_topology_en():
    with Diagram("Physical & Logical Topology - MikroTik Multi-Site", 
                 filename="docs/img/network_topology", 
                 show=False, 
                 direction="LR", 
                 graph_attr=graph_attr):
        
        with Cluster("Headquarters (HQ)"):
            lan_hq = Switch("HQ LAN\n10.10.0.1/24")
            hq_core = Router("hq-core-01\nhAP ac2\nRID: 10.255.255.2")
            hq_edge = Router("hq-edge-01\nhEX\nRID: 10.255.255.1")
            lan_hq - hq_core
            hq_core >> Edge(label="10.1.0.0/30\nCost 10", color="#2563eb") >> hq_edge

        with Cluster("WAN Plane & Encrypted Overlay"):
            wan = Internet("Public WAN\n198.51.100.0/30")
            vpn = VPN("Tunnel gre-vpn (IPsec HW)\n10.100.0.0/30\nCost 10")

        with Cluster("Branch Site"):
            br_edge = Router("branch-edge-01\nhAP ac2\nRID: 10.255.255.3")
            br_core = Router("branch-core-01\nhEX\nRID: 10.255.255.4")
            lan_br = Switch("Branch LAN\n10.30.0.1/24")
            br_edge >> Edge(label="10.2.0.0/30\nCost 10", color="#2563eb") >> br_core
            br_core - lan_br

        with Cluster("Out-of-Band Management (OOB) - 10.99.0.0/24"):
            oob = Router("oob-master\n192.168.1.210 ↔ 10.99.0.1")

        # WAN Connections
        hq_edge >> Edge(label="ether1 (.1)", color="#475569") >> wan
        wan >> Edge(label="ether1 (.2)", color="#475569") >> br_edge

        # VPN Overlay
        hq_edge >> Edge(label="IPsec HW", style="dashed", color="#0284c7") >> vpn
        vpn >> Edge(label="IPsec HW", style="dashed", color="#0284c7") >> br_edge

        # Standby Direct Core-to-Core Link
        hq_core >> Edge(label="Direct Private Line (ether2)\n10.255.0.0/30 · Cost 50 (STANDBY)", color="#ea580c", style="bold") >> br_core

        # OOB Links
        hq_edge >> Edge(label=":2206", style="dotted", color="#6366f1") >> oob
        hq_core >> Edge(label=":2203", style="dotted", color="#6366f1") >> oob
        br_edge >> Edge(label=":2204", style="dotted", color="#6366f1") >> oob
        br_core >> Edge(label=":2205", style="dotted", color="#6366f1") >> oob

def generate_failover_es():
    with Diagram("Comparativa de Rutas OSPF - Normal vs Failover", 
                 filename="docs/img/failover_ospf", 
                 show=False, 
                 direction="TB", 
                 graph_attr=graph_attr):
        
        with Cluster("1. Estado Normal - Camino Primario (Coste Acumulado = 30)"):
            n_lan_hq = Switch("LAN HQ\n10.10.0.0/24")
            n_core_hq = Router("hq-core-01")
            n_edge_hq = Router("hq-edge-01")
            n_vpn = VPN("GRE/IPsec HW")
            n_edge_br = Router("branch-edge-01")
            n_core_br = Router("branch-core-01")
            n_lan_br = Switch("LAN Branch\n10.30.0.0/24")

            n_lan_hq >> n_core_hq
            n_core_hq >> Edge(label="Coste 10", color="#16a34a") >> n_edge_hq
            n_edge_hq >> Edge(label="Coste 10", color="#16a34a") >> n_vpn
            n_vpn >> Edge(label="Coste 10", color="#16a34a") >> n_edge_br
            n_edge_br >> Edge(label="Coste 10", color="#16a34a") >> n_core_br
            n_core_br >> n_lan_br

        with Cluster("2. Caida WAN / Tunel - Failover Directo (Coste = 50)"):
            f_lan_hq = Switch("LAN HQ\n10.10.0.0/24")
            f_core_hq = Router("hq-core-01")
            f_core_br = Router("branch-core-01")
            f_lan_br = Switch("LAN Branch\n10.30.0.0/24")

            f_lan_hq >> f_core_hq
            f_core_hq >> Edge(label="Linea Privada ether2\nCoste 50 · 1 salto (0.3 ms)", color="#ea580c", style="bold") >> f_core_br
            f_core_br >> f_lan_br

def generate_failover_en():
    with Diagram("OSPF Route Comparison - Normal vs Failover", 
                 filename="docs/img/ospf_failover", 
                 show=False, 
                 direction="TB", 
                 graph_attr=graph_attr):
        
        with Cluster("1. Normal State - Primary Path (Cumulative Cost = 30)"):
            n_lan_hq = Switch("HQ LAN\n10.10.0.0/24")
            n_core_hq = Router("hq-core-01")
            n_edge_hq = Router("hq-edge-01")
            n_vpn = VPN("GRE/IPsec HW")
            n_edge_br = Router("branch-edge-01")
            n_core_br = Router("branch-core-01")
            n_lan_br = Switch("Branch LAN\n10.30.0.0/24")

            n_lan_hq >> n_core_hq
            n_core_hq >> Edge(label="Cost 10", color="#16a34a") >> n_edge_hq
            n_edge_hq >> Edge(label="Cost 10", color="#16a34a") >> n_vpn
            n_vpn >> Edge(label="Cost 10", color="#16a34a") >> n_edge_br
            n_edge_br >> Edge(label="Cost 10", color="#16a34a") >> n_core_br
            n_core_br >> n_lan_br

        with Cluster("2. WAN / Tunnel Outage - Direct Failover (Cost = 50)"):
            f_lan_hq = Switch("HQ LAN\n10.10.0.0/24")
            f_core_hq = Router("hq-core-01")
            f_core_br = Router("branch-core-01")
            f_lan_br = Switch("Branch LAN\n10.30.0.0/24")

            f_lan_hq >> f_core_hq
            f_core_hq >> Edge(label="Private Leased Line ether2\nCost 50 · 1 hop (0.3 ms)", color="#ea580c", style="bold") >> f_core_br
            f_core_br >> f_lan_br

if __name__ == "__main__":
    print("[*] Generando diagrama de topologia (ES)...")
    generate_topology_es()
    print("[*] Generating topology diagram (EN)...")
    generate_topology_en()
    print("[*] Generando diagrama de failover (ES)...")
    generate_failover_es()
    print("[*] Generating failover diagram (EN)...")
    generate_failover_en()
    print("[+] Todos los diagramas generados con éxito en docs/img/.")
