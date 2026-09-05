#!/usr/bin/env bash
set -euo pipefail

OOB_IP="192.168.1.210"
OOB_USER="admin"
ANSIBLE_USER="admin"
OUTPUT_FILE="hosts_discovered.yaml"

echo "[*] Consultando vecinos MikroTik (MNDP/LLDP) desde el router OOB..."

# Extraer vecinos en formato clave=valor estructurado
RAW_NEIGHBORS=$(ssh -o StrictHostKeyChecking=no "${OOB_USER}@${OOB_IP}" \
  "/ip neighbor print terse without-paging")

# Extraer leases DHCP activas por si algún nodo no anuncia MNDP
RAW_LEASES=$(ssh -o StrictHostKeyChecking=no "${OOB_USER}@${OOB_IP}" \
  "/ip dhcp-server lease print terse without-paging")

echo "[*] Generando inventario Ansible: ${OUTPUT_FILE}..."

cat << 'EOF' > "${OUTPUT_FILE}"
all:
  children:
    mikrotik_lab:
      vars:
        ansible_connection: network_cli
        ansible_network_os: community.routeros.routeros
        ansible_user: admin
      hosts:
EOF

# Parsear vecinos MNDP e inyectar al YAML
echo "${RAW_NEIGHBORS}" | while read -r line; do
  [ -z "$line" ] && continue
  
  # Extraer campos
  IDENTITY=$(echo "$line" | grep -o 'identity="[^"]*"' | cut -d'"' -f2 || true)
  ADDRESS=$(echo "$line" | grep -o 'address=[^ ]*' | cut -d'=' -f2 || true)
  MAC=$(echo "$line" | grep -o 'mac-address=[^ ]*' | cut -d'=' -f2 || true)
  BOARD=$(echo "$line" | grep -o 'board=[^ ]*' | cut -d'=' -f2 || true)

  # Normalizar hostname si no tiene identity definida
  [ -z "$IDENTITY" ] && IDENTITY="mtk_${MAC//:/}"
  # Reemplazar caracteres no válidos para hostnames de Ansible
  SAFE_HOST=$(echo "$IDENTITY" | tr ' ' '_' | tr -cd '[:alnum:]_-')

  if [ -n "$ADDRESS" ]; then
    cat << HOST_ENTRY >> "${OUTPUT_FILE}"
        ${SAFE_HOST}:
          ansible_host: ${ADDRESS}
          mac_address: "${MAC}"
          board_model: "${BOARD}"
HOST_ENTRY
  fi
done

# Añadir el propio OOB-Master al inventario
cat << EOF >> "${OUTPUT_FILE}"
        oob-master:
          ansible_host: ${OOB_IP}
          board_model: "RB750r2"
EOF

echo "[+] Inventario generado con éxito."
cat "${OUTPUT_FILE}"