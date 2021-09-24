""" Caravan for Three Players
To-Do:
-Define game state
-Define rules
-Define game flow
-Define "server"
"""

import pprint
from net import Network
import sys

# This is just information, not actually used
state_definition = {"pid" : "name",
                    "Posts" :
                        {"Post ID" : ("Post Name", "Score", "Cards", "Direction Flag")}
                    }

## If Direction Flag is None, allow any numeric card to be played. Otherwise, only allow cards that go in said direction or letters. Reverse on Q.

## This is the game state that is actually used
GAME_STATE = {1 : "Player 1",
              "player1" :
                  {1: ["1: The Hub",0,[], None],
                   2 : ["2: Junktown",0,[], None]}
              ,
              2 : "Player 2",
              "player2" :
                  {1 : ["1: Shady Sands",0,[], None],
                   2 : ["2: The Strip",0,[], None]}
              ,
              3 : "Player 3",
              "player3" :
                  {1 : ["1: Goodsprings",0, [], None],
                   2 : ["2: NCRCF",0, [], None]},
              "winning_round" : False
              }


net = Network()

def get_winning_player():
    playerwin = {'player1': 0,
                 'player2': 0,
                 'player3': 0}
    for player in GAME_STATE:
        if player != 'winning_round' and player not in [1,2,3]:
            print(player)
            for post in GAME_STATE[player]:
                score = GAME_STATE[player][post][1]
                if score >= 19 and score <= 25:
                    playerwin[player] += 1

    for wins in playerwin:
        if playerwin[wins] == 2:
            return (True, playerwin)

    return (False, 0) 

def calc_post_score(postcards):
    score = 0
    is_double = False
    ## Sum every card
    for i in range(len(postcards)):
        score += postcards[i] if postcards[i] != "A" else 1
    return score

def play_card(player, post, card):
    if GAME_STATE[player][post][3] is None:
        #add card to post    
        ##If it's the second card, determine direction, if it's the first, ignore
        if len(GAME_STATE[player][post][2]) == 2:
            print(GAME_STATE[player][post][2][-1], card)
            if GAME_STATE[player][post][2][-1] == card:
                
                print("Played card is the same as last card in this post. Card has to be different.")
            print("I am doing direction!!!")
            direction = True if GAME_STATE[player][post][2][0] < GAME_STATE[player][post][2][1] else False
            GAME_STATE[player][post][3] = direction
            GAME_STATE[player][post][2].append(card)
        else:
            GAME_STATE[player][post][2].append(card)

        print(type(GAME_STATE[player][post][1]))
        GAME_STATE[player][post][1] = calc_post_score(GAME_STATE[player][post][2])
        #pprint.pprint(GAME_STATE)
        
    elif GAME_STATE[player][post][3]:
        if GAME_STATE[player][post][2][-1] == card:
            print("Played card is the same as last card in this post. Card has to be different.")
        #Allow any card higher than the currently placed
            if card <= GAME_STATE[player][post][2][-1]:
                print("Post is going in increasing direction, card is decreasing")
            else:
                GAME_STATE[player][post][2].append(card)
                GAME_STATE[player][post][1] = calc_post_score(GAME_STATE[player][post][2])
                #pprint.pprint(GAME_STATE)
            
    elif not GAME_STATE[player][post][3]:
        if GAME_STATE[player][post][2][-1] == card:
            print("Played card is the same as last card in this post. Card has to be different.")
        #Allow any card higher than the currently placed
            if card >= GAME_STATE[player][post][2][-1]:
                print("Post is going in increasing direction, card is decreasing")
            else:
                GAME_STATE[player][post][2].append(card)
                GAME_STATE[player][post][1] = calc_post_score(GAME_STATE[player][post][2])
                #pprint.pprint(GAME_STATE)
def send_data(target, post, card):
    data = str(net.id) + ":" + str(target) + "," + str(post) + "," + str(card)


    reply = net.send(data)

    return reply

def send_message(msg):

    res = net.send(msg)
    if res == "0:,,...0:,,":
        print("Mensaje Enviado")
    else:
        print("Error al mandar mensaje")

def parse_data(data):
    try:
        data = data.split("...")
        d1= data[0].split(":")[1].split(",")
        d2 = data[1].split(":")[1].split(",")
        return d1[0], int(d1[1]), int(d1[2]), d2[0], int(d2[1]), int(d2[2])

    except:
        return "", 0, "", "", 0, ""

## Send initial state to three players
## Give player 1 their turn, wait for input while checking for chat.
## Input form: {input_player, target_player, post, card}
while True:
    menu = True
    usrName = input("Ingrese su nombre de usuario: \n")
    player = net.id
    print("Bienvenido, "  + usrName + ": jugador " + str((int(player) + 1)))
    
    while menu:
        
        print("*//\\//\\//\\//\\//\\//\\//\\//\\//\\  CARAVAN //\\ //\\//\\//\\//\\//\\//\\//\\//\\//\\//\\")
        print(" ")
        opcion = input("1 para jugar.\n2 para chatear con la sala.\n3 para salir.\n")

        if opcion == "1":
            print("Existen 3 jugadores, cada jugador tiene 2 puestos")
            print("Objetivo: Cada jugador debe de llevar cada puesto a los niveles entre 19 y 25.")
            print("  ")
            print("Cada jugador empieza desde 0 en sus puestos y pone una carta por turno sobre cada puesto")
            print("Las cartas empiezan con la carta “A” que vale 1 y la “10” que vale 10.")
            print("Una vez que se coloca una carta, solo se pueden colocar cartas mayores si la siguiente es mayor, o menores si la siguiente es menor.")
            print("El jugador gana si tiene un valor entre 19 y 25 para ambos puestos.")
            print("  ")
            pprint.pprint(GAME_STATE)
            player_input = input("Post, Card (Separated by spaces)\n")
            #player_input = "1,2,1,5"
            ##Get input
            ## Replace with get input from socket
            player_input = player_input.split(",")
            
            post,card = player_input[0], player_input[1]


            ##Convert card to int if not 'A'
            card = int(card) if card != 'A' else card
            post = int(post)
            target= 'player'+ str(player)
            #print(type(target))
            
            player = int(player)
            #print(target,post)
            #print(GAME_STATE[target][post])
            
            ## Verify if card is playable, else tell player to try another card. This should be defined on client side so it shouldn't happen.
            play_card(target,post,card)

            #Sending data to network
            tN1, pN1, cN1, tN2, pN2, cN2 = parse_data(send_data(target,post,card))

            if "player" not in tN1:
                tN1 = "player" + tN1

            if "player" not in tN2:
                tN2 = "player" + tN2

            if tN1 != "" and pN1 != 0 and cN1 != "":
                play_card(tN1 , pN1, cN1)

            if tN2 != "" and pN2 != 0 and cN2 != "":
                play_card(tN2 , pN2, cN2)
        if get_winning_player()[0] == True:
            msg = "Message from" + usrName + ": " + usrName + " won the game!\n"
            send_message(msg)
        if opcion == "2":
            msg = input("Ingrese el mensaje:\n")
            
            msg = "Message from " + usrName + ": " + msg
            send_message(msg)
        
        if opcion == "3":
            sys.exit()

    


