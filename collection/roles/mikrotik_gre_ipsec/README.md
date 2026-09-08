# Rol: mikrotik_gre_ipsec

Crea y gestiona de forma idempotente túneles GRE asegurados mediante IPsec en MikroTik RouterOS sin provocar fallos por colisión de nombres.

## Variables
- `gre_tunnels`: Lista de túneles (`name`, `local_address`, `remote_address`, `ipsec_secret`, `allow_fast_path`, `comment`).
