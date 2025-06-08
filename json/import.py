from django.contrib.auth.hashers import make_password
import json

# Ruta al archivo JSON original
input_file_path = 'd:/user.json'
# Ruta al archivo JSON procesado
output_file_path = 'd:/user_processed.json'

# Leer el archivo JSON original
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Actualizar el campo `password` con un hash generado
for user in data:
    if 'username' in user and 'password' in user:
        user['password'] = make_password(user['password'])

# Escribir los datos modificados en un nuevo archivo JSON
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f'Processed data saved to {output_file_path}')
