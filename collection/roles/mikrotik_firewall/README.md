# Rol: mikrotik_firewall

Implementa reglas de Firewall Filter y NAT (DNAT y SNAT/Masquerade) de forma no destructiva utilizando reconciliación mediante comentarios ancla (`comment="..."`).

## Variables
- `dnat_rules`: Reglas de reenvío de puertos.
- `snat_rules`: Reglas de enmascaramiento y traducción de origen.
- `firewall_input_rules`: Reglas de filtrado para el tráfico hacia el router.
- `firewall_forward_rules`: Reglas de filtrado para el tráfico en tránsito.
