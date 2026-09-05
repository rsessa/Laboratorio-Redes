#!/usr/bin/env bash
set -euo pipefail

OOB_IP="192.168.1.210"
OOB_USER="admin"
ANSIBLE_USER="admin"
OUTPUT_FILE="hosts_discovered.yaml"

echo "[*] Querying MikroTik neighbors (MNDP/LLDP) from the OOB router..."

# Extract neighbors in structured key=value format
RAW_NEIGHBORS=$(ssh -o StrictHostKeyChecking=no "${OOB_USER}@${OOB_IP}" \
  "/ip neighbor print terse without-paging")

# Extract active DHCP leases in case any node does not advertise MNDP
RAW_LEASES=$(ssh -o StrictHostKeyChecking=no "${OOB_USER}@${OOB_IP}" \
  "/ip dhcp-server lease print terse without-paging")

echo "[*] Generating Ansible inventory: ${OUTPUT_FILE}..."

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

# Parse MNDP neighbors and inject into YAML
echo "${RAW_NEIGHBORS}" | while read -r line; do
  [ -z "$line" ] && continue
  
  # Extract fields
  IDENTITY=$(echo "$line" | grep -o 'identity="[^"]*"' | cut -d'"' -f2 || true)
  ADDRESS=$(echo "$line" | grep -o 'address=[^ ]*' | cut -d'=' -f2 || true)
  MAC=$(echo "$line" | grep -o 'mac-address=[^ ]*' | cut -d'=' -f2 || true)
  BOARD=$(echo "$line" | grep -o 'board=[^ ]*' | cut -d'=' -f2 || true)

  # Normalize hostname if no identity is defined
  [ -z "$IDENTITY" ] && IDENTITY="mtk_${MAC//:/}"
  # Replace invalid characters for Ansible hostnames
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

# Add the OOB-Master itself to the inventory
cat << EOF >> "${OUTPUT_FILE}"
        oob-master:
          ansible_host: ${OOB_IP}
          board_model: "RB750r2"
EOF

echo "[+] Inventory generated successfully."
cat "${OUTPUT_FILE}"