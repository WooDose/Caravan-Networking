""" Caravan for Three Players
To-Do:
-Define game state
-Define rules
-Define game flow
-Define "server"
"""

import pprint
from net import Network

# This is just information, not actually used
state_definition = {"pid" : "name",
                    "Posts" :
                        {"Post ID" : ("Post Name", "Score", "Cards", "Direction Flag")}
                    }

## If Direction Flag is None, allow any numeric card to be played. Otherwise, only allow cards that go in said direction or letters. Reverse on Q.

## This is the game state that is actually used
game_state = {1 : "Player 1",
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



def calc_post_score(postcards):
    score = 0
    is_double = False
    ## Sum every card
    for i in range(len(postcards)):
        score += postcards[i] if postcards[i] != "A" else 1
    return score

def play_card(player, post, card):
    if game_state[player][post][3] is None:
        #add card to post    
        ##If it's the second card, determine direction, if it's the first, ignore
        if len(game_state[player][post][2]) == 2:
            print(game_state[player][post][2][-1], card)
            if game_state[player][post][2][-1] == card:
                
                print("Played card is the same as last card in this post. Card has to be different.")
            print("I am doing direction!!!")
            direction = True if game_state[player][post][2][0] < game_state[player][post][2][1] else False
            game_state[player][post][3] = direction
            game_state[player][post][2].append(card)
        else:
            game_state[player][post][2].append(card)

        print(type(game_state[player][post][1]))
        game_state[player][post][1] = calc_post_score(game_state[player][post][2])
        #pprint.pprint(game_state)
        
    elif game_state[player][post][3]:
        if game_state[player][post][2][-1] == card:
            print("Played card is the same as last card in this post. Card has to be different.")
        #Allow any card higher than the currently placed
            if card <= game_state[player][post][2][-1]:
                print("Post is going in increasing direction, card is decreasing")
            else:
                game_state[player][post][2].append(card)
                game_state[player][post][1] = calc_post_score(game_state[player][post][2])
                #pprint.pprint(game_state)
            
    elif not game_state[player][post][3]:
        if game_state[player][post][2][-1] == card:
            print("Played card is the same as last card in this post. Card has to be different.")
        #Allow any card higher than the currently placed
            if card >= game_state[player][post][2][-1]:
                print("Post is going in increasing direction, card is decreasing")
            else:
                game_state[player][post][2].append(card)
                game_state[player][post][1] = calc_post_score(game_state[player][post][2])
                #pprint.pprint(game_state)
def send_data(target, post, card):
    data = str(net.id) + ":" + str(target) + "," + str(post) + "," + str(card)


    reply = net.send(data)

    return reply

def send_message(msg):

    res = net.send(msg)
    print(res)

def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return d[0], int(d[1]), int(d[2])

    except:
        return "", 0, ""

## Send initial state to three players
## Give player 1 their turn, wait for input while checking for chat.
## Input form: {input_player, target_player, post, card}
while True:
    menu = True
    usrName = input("Ingrese su nombre de usuario: \n")
    while menu:

        opcion = input("1 para jugar.\n2 para chatear con la sala.\n3 para salir.\n")

        if opcion == "1":

            pprint.pprint(game_state)
            player_input = input("Player, Target Player, Post, Card (Separated by spaces)\n")
            #player_input = "1,2,1,5"
            ##Get input
            ## Replace with get input from socket
            player_input = player_input.split(",")
            player,post,card = player_input[0], player_input[1],player_input[2]


            ##Convert card to int if not 'A'
            card = int(card) if card != 'A' else card
            post = int(post)
            target= 'player'+player
            #print(type(target))
            
            player = int(player)
            #print(target,post)
            #print(game_state[target][post])
            
            ## Verify if card is playable, else tell player to try another card. This should be defined on client side so it shouldn't happen.
            play_card(target,post,card)

            #Sending data to network
            tN, pN, cN = parse_data(send_data(target,post,card))

            if "player" not in tN:
                tN = "player" + tN

            play_card(tN , pN, cN)
        
        if opcion == "2":
            msg = input("Ingrese el mensaje:\n")
            
            msg = "From " + usrName + "\n" + msg
            send_message(msg)

    


