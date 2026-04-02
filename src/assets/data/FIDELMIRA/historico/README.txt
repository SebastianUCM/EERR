EEFF — acercamiento (snapshots locales)

- index.json: lista de periodos visibles en el dashboard (se actualiza al generar snapshots).
- Cada snapshot *.json contiene { "meta", "cuentas" } generado solo con SELECT en SQL Server.

Generar un snapshot (solo lectura en BD):
  python script/extract_contabilidad_snapshot.py FIDELMIRA --desde 2025-01-01 --hasta 2025-01-31 --id 2025-01 --modo movimiento
  python script/extract_contabilidad_snapshot.py FIDELMIRA --desde 2025-01-01 --hasta 2025-01-31 --id 2025-01 --modo cierre

Batch mensual (desde año inicial hasta hoy), desde la raíz del repo:
  powershell -ExecutionPolicy Bypass -File .\script\snapshot_mensual_softland.ps1 -Empresa FIDELMIRA -AnioDesde 2020

Variables: SOFTLAND_SQL_SERVER, SOFTLAND_SQL_USER, SOFTLAND_SQL_PASSWORD
