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

# Theme configurations
THEMES = {
    "light": {
        "graph": {
            "fontsize": "16",
            "bgcolor": "#ffffff",
            "fontcolor": "#1f2937",
            "pad": "0.5",
            "splines": "spline",
        },
        "node": {
            "fontcolor": "#1f2937",
            "fontsize": "12",
        },
        "cluster": {
            "bgcolor": "#f8fafc",
            "pencolor": "#cbd5e1",
            "fontcolor": "#1e40af",
            "fontsize": "14",
        },
        "transit_edge": {"color": "#2563eb", "fontcolor": "#334155"},
        "wan_edge": {"color": "#475569", "fontcolor": "#334155"},
        "vpn_edge": {"color": "#0284c7", "fontcolor": "#334155"},
        "standby_edge": {"color": "#ea580c", "fontcolor": "#7c2d12"},
        "oob_edge": {"color": "#6366f1", "fontcolor": "#4338ca"},
        "normal_path": {"color": "#16a34a", "fontcolor": "#14532d"},
    },
    "dark": {
        "graph": {
            "fontsize": "16",
            "bgcolor": "#0d1117",
            "fontcolor": "#f0f6fc",
            "pad": "0.5",
            "splines": "spline",
        },
        "node": {
            "fontcolor": "#f0f6fc",
            "fontsize": "12",
        },
        "cluster": {
            "bgcolor": "#161b22",
            "pencolor": "#30363d",
            "fontcolor": "#58a6ff",
            "fontsize": "14",
        },
        "transit_edge": {"color": "#60a5fa", "fontcolor": "#94a3b8"},
        "wan_edge": {"color": "#94a3b8", "fontcolor": "#94a3b8"},
        "vpn_edge": {"color": "#38bdf8", "fontcolor": "#7dd3fc"},
        "standby_edge": {"color": "#fb923c", "fontcolor": "#fdba74"},
        "oob_edge": {"color": "#818cf8", "fontcolor": "#c7d2fe"},
        "normal_path": {"color": "#4ade80", "fontcolor": "#86efac"},
    }
}

def build_topology(lang="es", theme="dark"):
    t = THEMES[theme]
    suffix = f"_{theme}"
    
    if lang == "es":
        title = f"Topología Física y Lógica - MikroTik Multi-Site ({theme.capitalize()})"
        filename = f"docs/img/topologia_red{suffix}"
        hq_title = "Sede Central (HQ)"
        wan_title = "Plano WAN & Overlay Cifrado"
        br_title = "Sucursal (Branch)"
        oob_title = "Gestión Fuera de Banda (OOB) - 10.99.0.0/24"
        wan_lbl = "WAN Pública\n198.51.100.0/30"
        vpn_lbl = "Túnel gre-vpn (IPsec HW)\n10.100.0.0/30\nCoste 10"
        transit_hq = "10.1.0.0/30\nCoste 10"
        transit_br = "10.2.0.0/30\nCoste 10"
        standby_lbl = "Línea Privada Directa (ether2)\n10.255.0.0/30 · Coste 50 (STANDBY)"
    else:
        title = f"Physical & Logical Topology - MikroTik Multi-Site ({theme.capitalize()})"
        filename = f"docs/img/network_topology{suffix}"
        hq_title = "Headquarters (HQ)"
        wan_title = "WAN Plane & Encrypted Overlay"
        br_title = "Branch Site"
        oob_title = "Out-of-Band Management (OOB) - 10.99.0.0/24"
        wan_lbl = "Public WAN\n198.51.100.0/30"
        vpn_lbl = "Tunnel gre-vpn (IPsec HW)\n10.100.0.0/30\nCost 10"
        transit_hq = "10.1.0.0/30\nCost 10"
        transit_br = "10.2.0.0/30\nCost 10"
        standby_lbl = "Direct Private Line (ether2)\n10.255.0.0/30 · Cost 50 (STANDBY)"

    with Diagram(title, filename=filename, show=False, direction="LR", graph_attr=t["graph"], node_attr=t["node"]):
        with Cluster(hq_title, graph_attr=t["cluster"]):
            lan_hq = Switch("LAN HQ\n10.10.0.1/24")
            hq_core = Router("hq-core-01\nhAP ac2\nRID: 10.255.255.2")
            hq_edge = Router("hq-edge-01\nhEX\nRID: 10.255.255.1")
            lan_hq - hq_core
            hq_core >> Edge(label=transit_hq, **t["transit_edge"]) >> hq_edge

        with Cluster(wan_title, graph_attr=t["cluster"]):
            wan = Internet(wan_lbl)
            vpn = VPN(vpn_lbl)

        with Cluster(br_title, graph_attr=t["cluster"]):
            br_edge = Router("branch-edge-01\nhAP ac2\nRID: 10.255.255.3")
            br_core = Router("branch-core-01\nhEX\nRID: 10.255.255.4")
            lan_br = Switch("LAN Branch\n10.30.0.1/24")
            br_edge >> Edge(label=transit_br, **t["transit_edge"]) >> br_core
            br_core - lan_br

        with Cluster(oob_title, graph_attr=t["cluster"]):
            oob = Router("oob-master\n192.168.1.210 ↔ 10.99.0.1")

        # WAN Connections
        hq_edge >> Edge(label="ether1 (.1)", **t["wan_edge"]) >> wan
        wan >> Edge(label="ether1 (.2)", **t["wan_edge"]) >> br_edge

        # VPN Overlay
        hq_edge >> Edge(label="IPsec HW", style="dashed", **t["vpn_edge"]) >> vpn
        vpn >> Edge(label="IPsec HW", style="dashed", **t["vpn_edge"]) >> br_edge

        # Standby Direct Core-to-Core
        hq_core >> Edge(label=standby_lbl, style="bold", **t["standby_edge"]) >> br_core

        # OOB Links
        hq_edge >> Edge(label=":2206", style="dotted", **t["oob_edge"]) >> oob
        hq_core >> Edge(label=":2203", style="dotted", **t["oob_edge"]) >> oob
        br_edge >> Edge(label=":2204", style="dotted", **t["oob_edge"]) >> oob
        br_core >> Edge(label=":2205", style="dotted", **t["oob_edge"]) >> oob

def build_failover(lang="es", theme="dark"):
    t = THEMES[theme]
    suffix = f"_{theme}"
    
    if lang == "es":
        title = f"Comparativa de Rutas OSPF - Normal vs Failover ({theme.capitalize()})"
        filename = f"docs/img/failover_ospf{suffix}"
        normal_title = "1. Estado Normal - Camino Primario (Coste Acumulado = 30)"
        failover_title = "2. Caída WAN / Túnel - Failover Directo (Coste = 50)"
        cost_step = "Coste 10"
        standby_lbl = "Línea Privada ether2\nCoste 50 · 1 salto (0.3 ms)"
    else:
        title = f"OSPF Route Comparison - Normal vs Failover ({theme.capitalize()})"
        filename = f"docs/img/ospf_failover{suffix}"
        normal_title = "1. Normal State - Primary Path (Cumulative Cost = 30)"
        failover_title = "2. WAN / Tunnel Outage - Direct Failover (Cost = 50)"
        cost_step = "Cost 10"
        standby_lbl = "Private Leased Line ether2\nCost 50 · 1 hop (0.3 ms)"

    with Diagram(title, filename=filename, show=False, direction="TB", graph_attr=t["graph"], node_attr=t["node"]):
        with Cluster(normal_title, graph_attr=t["cluster"]):
            n_lan_hq = Switch("LAN HQ\n10.10.0.0/24")
            n_core_hq = Router("hq-core-01")
            n_edge_hq = Router("hq-edge-01")
            n_vpn = VPN("GRE/IPsec HW")
            n_edge_br = Router("branch-edge-01")
            n_core_br = Router("branch-core-01")
            n_lan_br = Switch("LAN Branch\n10.30.0.0/24")

            n_lan_hq >> n_core_hq
            n_core_hq >> Edge(label=cost_step, **t["normal_path"]) >> n_edge_hq
            n_edge_hq >> Edge(label=cost_step, **t["normal_path"]) >> n_vpn
            n_vpn >> Edge(label=cost_step, **t["normal_path"]) >> n_edge_br
            n_edge_br >> Edge(label=cost_step, **t["normal_path"]) >> n_core_br
            n_core_br >> n_lan_br

        with Cluster(failover_title, graph_attr=t["cluster"]):
            f_lan_hq = Switch("LAN HQ\n10.10.0.0/24")
            f_core_hq = Router("hq-core-01")
            f_core_br = Router("branch-core-01")
            f_lan_br = Switch("LAN Branch\n10.30.0.0/24")

            f_lan_hq >> f_core_hq
            f_core_hq >> Edge(label=standby_lbl, style="bold", **t["standby_edge"]) >> f_core_br
            f_core_br >> f_lan_br

if __name__ == "__main__":
    for theme in ["light", "dark"]:
        print(f"[*] Generando diagramas para tema: {theme}...")
        build_topology("es", theme)
        build_topology("en", theme)
        build_failover("es", theme)
        build_failover("en", theme)
    print("[+] Todos los diagramas (light y dark) generados con éxito en docs/img/.")
