# Rol: mikrotik_restore

Restaura de forma controlada una copia binaria (`.backup`), comprobando previamente la existencia del archivo en local y gestionando el reinicio del nodo.

## Variables
- `backup_source_file`: Ruta específica al archivo `.backup`.
- `backup_source_dir`: Directorio donde buscar el archivo `<inventory_hostname>.backup`.
- `reboot_timeout`: Tiempo de espera máximo para la recuperación tras el reinicio (segundos).
