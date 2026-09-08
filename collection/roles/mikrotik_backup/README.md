# Rol: mikrotik_backup

Genera y descarga copias de seguridad en texto plano (`.rsc`) y binario (`.backup`) hacia el controlador local, eliminando de forma segura los archivos temporales remotos.

## Variables
- `backup_base_dir`: Directorio base local (por defecto `backups`).
- `custom_backup_dir`: Directorio específico opcional.
- `ssh_private_key`: Clave privada SSH local para la transferencia SCP.
