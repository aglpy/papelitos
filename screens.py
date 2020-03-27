# 80*24
steps = {"Descripcion":30, "Password":20, "Mimica":20, "Sonidos":20}

# Pantalla inicial tras registro, claves:
# users: usuarios conectados separados por coma
welcome = '''
                                  PAPELITOS
Usuarios conectados: {users}
'''[1:-1]

# Esta pantalla se muestra para introducir palabras
get_words = '''
                                  PAPELITOS
Introduce 4 palabras separadas por comas
Si se introducen mas se tomarán 4 aleatorias
'''[1:-1]

# Esperado a que los demas acaben, claves:
# tardones: los que aun quedan por poner palabras
waiting_other_users_words = '''
                                  PAPELITOS
Esperando a que los demas acaben, quedan: {tardones}
'''[1:-1]

# Pantalla que muestra las parejas y el orden, claves:
# pairs: parejas, entre parentesis separadas por coma: "(a, b), (c, d), (e, f), ..."
# order: lista en orden, con el caso anterior seria: "1º: a, 2º: c, 3º:e, 4º:b, 5º:d, 6º:f, ...", el primero es el que coje papel
random_users = '''
                                  PAPELITOS
Parejas: {pairs}
Orden: {order}
'''[1:-1]
















# Lo que ve al que le toca coger papel mientras coge papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
turn_of_screen_taking = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Te toca coger papel, introduce "coger papel" para cogerlo
'''[1:-1]

# Lo que ve el que adivina, mientras se coge el papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
mate_screen_taking = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Te toca adivinar, esperando a que tu compañero coja papel...
'''[1:-1]

# Lo que ve el resto, mientras se coge el papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
rest_screen_taking = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Está cogiendo papel: {player_playing}
Le toca adivinar a: {player_playing_mate}
'''[1:-1]















# Lo que ve al que le toca coger papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
# t: cuenta atrás
# word: palabra que ha cogido
turn_of_screen = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Tiempo: {t}
Palabra que has cogido: <s 3>{word}</s>
'''[1:-1]

# Lo que ve el que adivina, mientras se coge el papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
# t: cuenta atrás
mate_screen = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Tiempo: {t}
Introduce la palabra:
'''[1:-1]

# Lo que ve el resto, mientras se coge el papel
# Posibles claves:
# player_playing: el que coge papel
# player_playing_mate: el que adivina
# step: la ronda en la que estamos
# turn: el numero del turno dentro de la ronda en la que estamos
# t: cuenta atrás
rest_screen = '''
                                  PAPELITOS
Ronda: {step}
Turno: {turn}
Tiempo: {t}
Ha cogido papel: {player_playing}
Está adivinando: {player_playing_mate}
Ultima palabra que ha dicho: 
'''[1:-1]