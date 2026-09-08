# Rol: mikrotik_common

Aprovisiona la identidad del router, securiza los servicios IP (deshabilitando los inseguros y activando SSH/Winbox) y gestiona de manera estrictamente idempotente las claves públicas SSH autorizadas.

## Variables
Consulte `defaults/main.yaml` para ver las variables disponibles (`node_identity`, `enabled_services`, `disabled_services`, `manage_ssh_keys`, etc.).
