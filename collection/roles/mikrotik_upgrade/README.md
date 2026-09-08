# Rol: mikrotik_upgrade

Realiza actualizaciones condicionales e idempotentes de RouterOS y bootloader RouterBOARD. Omite descargas, transferencias y reinicios si el dispositivo ya está al día.

## Variables
- `target_version`: Versión objetivo de RouterOS (por defecto `7.18`).
- `download_base_dir`: Ruta local de descarga para paquetes `.npk`.
- `reboot_timeout`: Tiempo de espera tras el reinicio en segundos.
