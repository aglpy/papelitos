import os
width = os.get_terminal_size().columns - 1
print("PAPELITOS".center(width))
print("Iniciando...", end='\r')
from funcs import fprint
import threading
import time
import boto3
global stop_ot

print("Conectando con el servidor...", end='\r')
ACCESS_KEY = 'XXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
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

def output_thread():
    global stop_ot
    while True:
        time.sleep(1)
        if not stop_ot:
            output = read_ddb('output')
            os.system('cls')
            fprint(output)
ot = threading.Thread(target=output_thread)

def input_thread():
    global stop_ot
    while True:
        input()
        stop_ot = True
        user_input = input()
        stop_ot = False
        allowed = bool(int(read_ddb('input_allowed')))
        if allowed:
            write_ddb('input', user_input)
it = threading.Thread(target=input_thread)

stop_ot = False
it.start()
ot.start()
