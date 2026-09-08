# Rol: mikrotik_ospf

Configura el protocolo de enrutamiento dinámico OSPFv2 (instancia, Router ID, áreas, redes e interfaces) evitando duplicados en la base de datos de adyacencias.

## Variables
- `ospf`: Diccionario con `router_id`, `instance`, `networks` (red y área) e `interfaces` (coste, tipo de red, pasiva).
