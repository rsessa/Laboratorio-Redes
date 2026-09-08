# Colección Ansible: rsessa.routeros_ops

Colección modular, declarativa e **idempotente** para la provisión, configuración y ciclo de vida de routers **MikroTik RouterOS**.

---

## 📦 Estructura de la Colección

```
collection/
├── galaxy.yml                  # Manifiesto de empaquetado de la colección
├── README.md                   # Documentación general
├── playbooks/                  # Playbooks orquestadores
│   ├── deploy_site.yaml        # Despliegue de nodos de red (Bridges, IPs, GRE, OSPF)
│   ├── setup_bastion.yaml      # Configuración de Bastión OOB y Firewall/NAT
│   ├── backup.yaml             # Respaldo centralizado (.rsc y .backup)
│   ├── restore.yaml            # Restauración controlada de snapshots
│   ├── upgrade.yaml            # Actualización de ROS y bootloader RouterBOARD
│   └── audit.yaml              # Auditoría completa de configuración y estado
└── roles/                      # Roles independientes y reusables
    ├── mikrotik_common         # Identidad, hardening de servicios y claves SSH
    ├── mikrotik_interfaces     # Bridges, puertos y estado de interfaces
    ├── mikrotik_ip             # Direccionamiento IP y rutas
    ├── mikrotik_gre_ipsec      # Túneles GRE con aceleración IPsec
    ├── mikrotik_ospf           # Enrutamiento dinámico OSPFv2
    ├── mikrotik_firewall       # Cortafuegos (Filter) y reglas NAT idempotentes
    ├── mikrotik_backup         # Extracción segura de copias de seguridad
    ├── mikrotik_restore        # Restauración y comprobación de uptime
    └── mikrotik_upgrade        # Actualización condicional basada en hechos
```

---

## 🚀 Cómo usar los Roles y Playbooks

### 1. Ejecutar Playbooks Orquestadores
```bash
# Desplegar la topología de red completa
ansible-playbook -i hosts.yaml collection/playbooks/deploy_site.yaml

# Configurar el bastión de gestión OOB
ansible-playbook -i hosts.yaml collection/playbooks/setup_bastion.yaml

# Extraer copias de seguridad de todos los nodos
ansible-playbook -i hosts.yaml collection/playbooks/backup.yaml

# Actualizar el sistema operativo a la versión objetivo
ansible-playbook -i hosts.yaml collection/playbooks/upgrade.yaml -e "target_version=7.18"
```

### 2. Incluir Roles en tus propios Playbooks
```yaml
- name: Aprovisionar Router de Sucursal
  hosts: branch_routers
  roles:
    - role: rsessa.routeros_ops.mikrotik_common
    - role: rsessa.routeros_ops.mikrotik_interfaces
    - role: rsessa.routeros_ops.mikrotik_ip
    - role: rsessa.routeros_ops.mikrotik_ospf
```
