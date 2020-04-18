import os
import time
import boto3
import threading
import random
from screens import *

ACCESS_KEY = 'AKIAQBCG2Q3XDJOAESHV'
SECRET_KEY = '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'
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
    write_ddb('output', user, get_words.format(nwords=nwords))
    write_ddb('input_allowed', user, '1')
    
words = []
users_ready = []
while len(users_ready) < len(users):
    time.sleep(2)
    users_temp = []
    left = list(set(users) - set(users_ready))
    for user in left:
        user_words = read_ddb('input', user).split(',')
        user_words = list(map(lambda x: x.strip(), user_words))
        if len(user_words) > nwords:
            user_words = random.sample(user_words, nwords)
        if len(user_words) == nwords:
            words += user_words
            users_temp.append(user)
            write_ddb('output', user, waiting_other_users_words.format(tardones=left))
            write_ddb('input_allowed', user, '0')
    users_ready += users_temp
    print(f"Users ready: {users_ready}")

random.shuffle(users)
pairs = list(zip(users[:int(len(users)/2)], users[int(len(users)/2):]))

pairs_str = ', '.join(str(x) for x in pairs).replace("'", "")
order = ', '.join(f"{i+1}º: {x}" for i, x in enumerate(users))

n_players = len(users)

points_table = {}
for pair in pairs:
    points_table[f'{pair[0]}-{pair[1]}'] = 0

for user in users:
    write_ddb('output', user, random_users.format(pairs=pairs_str, order=order))

input('Enter para empezar')





players = users
turn = 0
for step in steps.keys():
    reading_words = []
    end_round = False
    while len(words) > 0:
        last_word = ""
        player_playing = players[turn%n_players]
        player_playing_mate = players[int((turn%n_players + n_players/2)%n_players)]
        rest = list(filter(lambda x: x != player_playing and x != player_playing_mate, players))

        write_ddb('output', player_playing, turn_of_screen_taking.format(step=step, turn=turn))
        write_ddb('input_allowed', player_playing, '1')
        write_ddb('output', player_playing_mate, mate_screen_taking.format(step=step, turn=turn))
        
        for player in rest:
            write_ddb('output', player, rest_screen_taking.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate))

        while True:
            time.sleep(1)
            is_ready = read_ddb('input', player_playing)
            if is_ready == "coger papel":
                write_ddb('input', player_playing, 'null')
                break
        write_ddb('input_allowed', player_playing, '0')
        random.shuffle(words)
        word = words.pop()

        write_ddb('input', player_playing_mate, 'null')

        write_ddb('output', player_playing_mate, mate_screen.format(step=step, turn=turn))
        time.sleep(1)
        write_ddb('input_allowed', player_playing_mate, '1')
        for t in range(steps.get(step), 0, -1):
            time.sleep(1)
            write_ddb('output', player_playing, turn_of_screen.format(step=step, turn=turn, t=t, word=word))
            
            for player in rest:
                write_ddb('output', player, rest_screen.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t))

            possible_word = read_ddb('input', player_playing_mate)

            fail = None
            if possible_word != "null":
                if possible_word == word:
                    reading_words.append(word)
                    last_word = word
                    fail = False
                    
                    write_ddb('output', player_playing, turn_of_screen_correct.format(step=step, turn=turn, t=t, word=word))
                    write_ddb('output', player_playing_mate, mate_screen_correct.format(step=step, turn=turn, t=t, word=word))
                    
                    for player in rest:
                        write_ddb('output', player, rest_screen_correct.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t, last_word=last_word))
                    write_ddb('input_allowed', player_playing_mate, '0')
                    time.sleep(3)
                    write_ddb('input', player_playing_mate, 'null')
                    for group in points_table.keys():
                        if player_playing in group:
                            points_table[group] += 1
                    random.shuffle(words)
                    if not len(words):
                        end_round = True
                        break
                    word = words.pop()
                    write_ddb('input_allowed', player_playing_mate, '1')
                else:
                    fail = True
                    break
        
        if end_round:
            turn += 1
            break
        if fail == None:
            write_ddb('output', player_playing, turn_of_screen_endtime.format(step=step, turn=turn, t=t, word=word))
            write_ddb('output', player_playing_mate, mate_screen_endtime.format(step=step, turn=turn, t=t))
            
            for player in rest:
                write_ddb('output', player, rest_screen_endtime.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t, last_word=last_word))
            words.append(word)

        elif fail == False:
            write_ddb('output', player_playing, turn_of_screen_correct_endtime.format(step=step, turn=turn, t=t))
            write_ddb('output', player_playing_mate, mate_screen_correct_endtime.format(step=step, turn=turn, t=t))
            
            for player in rest:
                write_ddb('output', player, rest_screen_correct_endtime.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t, last_word=last_word))

        elif fail == True:
            write_ddb('output', player_playing, turn_of_screen_wrong.format(step=step, turn=turn, t=t, word=word, possible_word=possible_word))
            write_ddb('output', player_playing_mate, mate_screen_wrong.format(step=step, turn=turn, t=t, word=word, possible_word=possible_word))
            
            for player in rest:
                write_ddb('output', player, rest_screen_wrong.format(step=step, turn=turn, player_playing=player_playing, player_playing_mate=player_playing_mate, t=t, possible_word=possible_word, last_word=last_word))
            words.append(word)
        
        write_ddb('input_allowed', player_playing_mate, '0')
        time.sleep(3)
        turn += 1
    
    points_table_str = "\n".join(f"{pair}: {points}" for pair, points in points_table.items())
         
    for player in users:
        write_ddb('output', player, points_screen.format(table=points_table_str, step=step))
    input('Continuar siguiente ronda, enter...')
           
    words = reading_words