import pyodbc
import json
from datetime import datetime

# Configuración de conexión
server = '172.27.1.117'
database = 'devcode'
username = 'angel'
password = 'Starwar1'

# Cargar datos desde el archivo JSON
try:
    with open('datatata.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
    print("Datos JSON cargados correctamente")
except Exception as e:
    print(f"Error al cargar el archivo JSON: {e}")
    exit()

# Establecer conexión con SQL Server
try:
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )
    cursor = conn.cursor()
    print("Conexión a SQL Server exitosa")

    # Procesar cada registro del JSON
    for item in datos:
        # Convertir la fecha al formato adecuado
        fecha = datetime.strptime(item['fecha'], '%d/%m/%Y %H:%M') if 'fecha' in item else None
        
        # Preparar el query SQL con columnas escapadas
        query = """
INSERT INTO [DEVCODE].[dbo].[informatica_informatica]
([fecha], [codigo], [inv_2023], [cod_sbn], [descripcion], [marca], [modelo], [serie], [piso], 
[usuario], [user], [condicion], [dependencia], [area], [responsable], [user_res], [condicion1], 
[dependencia1], [area1], [observacion], [antiguedad], [estado])
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
        
        # Ejecutar el query con los parámetros
        cursor.execute(query, 
            fecha,
            item.get('codigo'),
            item.get('inv_2023'),
            item.get('cod_sbn'),
            item.get('descripcion'),
            item.get('marca'),
            item.get('modelo'),
            item.get('serie'),
            item.get('piso'),
            f"{item.get('nom_user', '')} {item.get('ape_user', '')}".strip(),  # usuario
            item.get('user'),
            item.get('condicion'),
            item.get('dependencia'),
            item.get('area'),
            f"{item.get('nom_res', '')} {item.get('ape-res', '')}".strip(),  # responsable
            item.get('user_res'),
            item.get('condicion1'),
            item.get('dependencia1'),
            item.get('area1'),
            item.get('observacion'),
            item.get('antiguedad'),
            item.get('estado')
        )
    
    # Confirmar los cambios
    conn.commit()
    print(f"Se insertaron {len(datos)} registros correctamente")

except pyodbc.Error as e:
    print(f"Error en la conexión o inserción: {e}")
    if 'conn' in locals():
        conn.rollback()
    # Imprimir información detallada del error
    print("Detalle del error:", e.args)

except Exception as e:
    print(f"Error inesperado: {e}")

finally:
    # Cerrar la conexión si existe
    if 'conn' in locals():
        conn.close()