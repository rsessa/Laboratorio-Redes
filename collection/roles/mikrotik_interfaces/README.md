# Rol: mikrotik_interfaces

Administra de forma declarativa e idempotente los puentes (*bridges*), puertos asociados y el estado encendido/apagado de las interfaces físicas en MikroTik RouterOS.

## Variables
- `bridges`: Lista de bridges con nombres, comentarios y lista de interfaces miembro.
- `disabled_interfaces`: Puertos Ethernet a deshabilitar.
- `enabled_interfaces`: Puertos Ethernet a habilitar.
