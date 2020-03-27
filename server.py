import os
import time
import boto3
import threading
import random
from screens import *

ACCESS_KEY = 'XXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ddb = boto3.client('dynamodb', region_name='eu-west-3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def write_ddb(table, name, value):
    ddb.put_item(TableName=table, Item={'user':{'S':name}, 'text':{'S':value}})

def read_ddb(table, name):
    return ddb.get_item(TableName=table, Key={'user':{'S':name}}).get('Item').get('text').get('S')

def get_users():
    items = ddb.scan(TableName='input').get('Items')
    users = list(map(lambda x: x.get('user').get('S'), items))
    return users




global stop_waiting
global users
stop_waiting = False
def waiting_users():
    global stop_waiting
    global users
    while True:
        time.sleep(1)
        if stop_waiting:
            break
        users = get_users()
        for user in users:
            write_ddb('output', user, welcome.format(users=', '.join(users)))
wu = threading.Thread(target=waiting_users)

wu.start()
input('Enter para dejar de esperar e iniciar juego')
stop_waiting = True

for user in users:
    write_ddb('output', user, get_words)
    write_ddb('input_allowed', user, '1')
    
words = []
users_ready = []
while len(users_ready) < len(users):
    time.sleep(2)
    users_temp = []
    left = list(set(users) - set(users_ready))
    for user in left:
        user_words = read_ddb('input', user).split(',')
        if len(user_words) > 3:
            user_words = random.sample(user_words, 4)
        if len(user_words) == 3:
            words.append(user_words)
            users_temp.append(user)
            write_ddb('output', user, waiting_other_users_words.format(tardones=left))
            write_ddb('input_allowed', user, '0')
    users_ready += users_temp
    print(f"Users ready: {users_ready}")

random.shuffle(users)
pairs = list(zip(users[:int(len(users)/2)], users[len(int(users)/2):]))

pairs_str = ', '.join(str(x) for x in pairs)
order = ', '.join(f"{i}º: {x}" for i, x in enumerate(users))

n_players = len(users)

points_table = {}
for pair in pairs:
    points_table[f'{pair[0]}-{pair[1]}'] = 0

for user in users:
    write_ddb('output', user, random_users.format(pairs=pairs_str, order=order))

input('Enter para empezar')





players = users
for step in steps.keys():
    reading_words = []
    turn = 0
    while len(words) > 0:
        player_playing = players[turn%n_players]
        player_playing_mate = players[(turn%n_players + n_players/2)%n_players]
        rest = list(filter(lambda x: x != player_playing and x != player_playing_mate, players))

        write_ddb('output', player_playing, turn_of_screen_taking.format(step=step, turn=turn))
        write_ddb('output', player_playing_mate, mate_screen_taking.format(step=step, turn=turn))
        
        for player in rest:
            write_ddb('output', player, rest_screen_taking.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate))

        while True:
            time.sleep(1)
            is_ready = read_ddb('input', player_playing)
            if is_ready == "coger papel":
                break
        random.shuffle(words)
        word = words.pop()

        for t in range(steps.get(step), 0):
            time.sleep(1)
            write_ddb('output', player_playing, turn_of_screen.format(step=step, turn=turn, t=t, word=word))
            write_ddb('output', player_playing_mate, mate_screen.format(step=step, turn=turn, t=t))
            
            for player in rest:
                write_ddb('output', player, rest_screen.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t))




        turn += 1