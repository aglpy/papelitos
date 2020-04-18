import os
width = os.get_terminal_size().columns - 1
print("PAPELITOS".center(width))
print("Iniciando...", end='\r')
from funcs import fprint
import time
import boto3

print("Conectando con el servidor...", end='\r')
ACCESS_KEY = 'XXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
ddb = boto3.client('dynamodb', region_name='eu-west-3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
print(" "*width, end='\r')

def write_ddb(table, value):
    ddb.put_item(TableName=table, Item={'user':{'S':name}, 'text':{'S':value}})

def read_ddb(table):
    return ddb.get_item(TableName=table, Key={'user':{'S':name}}).get('Item').get('text').get('S')

name = input('Alias: ')

print('Registrando...')
write_ddb('input', 'OK')
write_ddb('output', 'Esperando a que empiece el juego...')
write_ddb('input_allowed', '0')
os.system('cls')

while True:
    time.sleep(1)
    output = read_ddb('output')
    os.system('cls')
    fprint(output)
    allowed = bool(int(read_ddb('input_allowed')))
    if allowed:
        user_input = input()
        if user_input != "":
            write_ddb('input', user_input)
            write_ddb('input_allowed', '0')
    