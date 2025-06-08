import json

# Ruta al archivo JSON original
input_file_path = 'd:/user.json'
# Ruta al archivo JSON procesado
output_file_path = 'd:/user_processed.json'

# Leer el archivo JSON original
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Convertir todos los correos electrónicos a minúsculas
for user in data:
    if 'email' in user:
        user['email'] = user['email'].lower()

# Escribir los datos procesados en un nuevo archivo JSON
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f'Processed data saved to {output_file_path}')
