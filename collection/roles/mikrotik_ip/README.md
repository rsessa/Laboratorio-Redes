# Rol: mikrotik_ip

Gestiona de forma idempotente las direcciones IPv4 en interfaces de red y las tablas de enrutamiento estático (incluyendo Gateway por defecto) sin provocar duplicados.

## Variables
- `ip_addresses`: Lista de diccionarios con `address`, `interface`, `comment`.
- `default_gateway`: Puerta de enlace por defecto (`0.0.0.0/0`).
- `static_routes`: Lista de rutas estáticas (`dst_address`, `gateway`, `comment`).
