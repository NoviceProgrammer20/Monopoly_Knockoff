"""
File:    pyopoly.py
Author:  Justin Quedit
Date:    11/02/20
Section: 15
E-mail:  jquedit1@umbc.edu
Description: This program will run a modified monopoly game between two players.
"""

from sys import argv
from random import randint, seed
from board_methods import load_map, display_board

if len(argv) >= 2:
    seed(argv[1])

START_POS = 0
STARTING_MONEY = 1500
PASS_GO_MONEY = 200

# constants for choices
CHOICE_1 = "1"
CHOICE_2 = "2"
CHOICE_3 = "3"
CHOICE_4 = "4"
CHOICE_5 = "5"

"""
    I recommend looking at the part of the play game function before the while
    loop before looking at the following functions
"""


# buy property option
# parameters: is it player 1's turn, player info dictionary, property dictionary
def buy_property(player_info, player1_turn, the_map):
    # player will be player1 unless it is not player 1's turn
    player = 'Player1'
    if not player1_turn:
        player = 'Player2'

    # finds the property player landed on
    for i in range(len(the_map)):
        if i == player_info[player]['Position']:

            # if the property isn't up for purchase
            if the_map[i]['Price'] == '-1':
                print("You cannot buy this property. It cannot be purchased"
                      " or sold.")

            # if the property is already owned
            elif the_map[i]['Owner'] != "BANK":
                print(the_map[i]['Owner'] + " owns this property. It is not up"
                                            " for purchase.")

            # player can buy property
            else:
                # asks player if they want to buy the property
                choice = input("You have landed on " + the_map[i]['Place']
                               + ". Do you want to purchase it? ")
                if choice.lower() == "yes" or choice.lower() == "y":
                    # adds to the player's properties
                    player_info[player]['Properties'].append(the_map[i]['Place'])
                    # makes the player the owner of the property in
                    # property dictionary
                    the_map[i]['Owner'] = player_info[player]['Name']
                    # deducts the cost amount from player's balance
                    player_info[player]['Balance'] -= int(the_map[i]['Price'])
                    print("You have successfully purchased " + the_map[i]['Place']
                          + ". Your remaining balance is "
                          + str(player_info[player]['Balance']))

                # if player doesn't buy the property
                elif choice.lower() == "no" or choice.lower() == "n":
                    print("You have decided not to buy " + the_map[i]['Place'])


# get property info option
# parameter: property dictionary
def get_property(the_map):
    the_property = input("Which property do you want the information of? ")
    # finds property a player wants info on
    for place in the_map:
        # accepts both abbreviation and property name
        if the_property.lower() == place['Abbrev'].lower() \
                or the_property.lower() == place['Place'].lower():
            # prints out property name, price, owner, if there's a building,
            # rent, and cost to build a building
            print('\n' + place['Place'] + '\n' +
                  "Price: " + place['Price'] + '\n' +
                  "Owner: " + place['Owner'] + '\n' +
                  "Building: " + place['Building'] + '\n' +
                  "Rent: " + place['Rent'] + ", "
                  + place['BuildingRent'] + "(with building)"
                  + '\n' + "Building Cost: " + place['BuildingCost']
                  )


# get player info option
# parameter: player info dictionary
def get_player(player_info):
    # prints out the players in the game first
    print("The players are: " + '\n'
          + player_info['Player1']['Name'] + '\n'
          + player_info['Player2']['Name'])

    # gets player they want info on
    choice = input("Which player do you wish to know about? ")
    # finds the player they want by looping through the player dictionary
    for player in player_info:
        if player_info[player]['Name'] == choice:
            # prints out player info
            print("\n" + "Player Name: " + str(player_info[player]['Name'])
                  + "\n" +
                  "Player Symbol: " + str(player_info[player]['Symbol'])
                  + "\n" +
                  "Current Money: " + str(player_info[player]['Balance'])
                  + "\n")
            # if player owns no properties
            if not player_info[player]['Properties']:
                print("Properties Owned: No Properties Yet")
            # if player owns properties, prints their properties' names
            else:
                print("Properties Owned: ")
                for property in player_info[player]['Properties']:
                    print(property)


# buy building option
# parameters: is it player 1's turn, player info dictionary, property dictionary
def buy_building(player_info, the_map, player1_turn):
    player = 'Player1'
    if not player1_turn:
        player = 'Player2'

    # prints out player's properties first
    for place in the_map:
        if place['Place'] in player_info[player]['Properties']:
            print(place['Place'], place['Abbrev'], place['BuildingCost'])

    # prompts a user for the property they want a building on
    building = input("Which property do you want to build a building on?")
    # checks if they own the property
    if building in player_info[player]['Properties']:
        for place in the_map:
            # builds a building if it doesn't have a building yet
            if place['Place'] == building and place['Building'] == "No":
                player_info[player]['Balance'] -= int(place['BuildingCost'])
                place['Building'] = "Yes"
                print("You have built the building for " + building)
    # input error
    else:
        print("The property either doesn't exist, has a building, or isn't "
              "yours")


# displays board
# parameters: property dictionary, player symbols, player positions
def format_display(the_map, player1, pos1, player2, pos2):
    # list of every property on board
    places = []

    # names of properties each player lands on
    spot1 = ""
    spot2 = ""

    # loops through each index of list of properties
    for i in range(len(the_map)):
        # if position of first and second players = i
        if i == pos1 and i == pos2:
            places.append(the_map[i]['Abbrev'].ljust(5) + '\n' + player1
                          + " " + player2)
            spot1 = the_map[i]['Place']
            spot2 = the_map[i]['Place']
        # if position of first player = i
        elif i == pos1:
            places.append(the_map[i]['Abbrev'].ljust(5) + '\n' + player1)
            spot1 = the_map[i]['Place']
        # if position of second player = i
        elif i == pos2:
            places.append(the_map[i]['Abbrev'].ljust(5) + '\n' + player2)
            spot2 = the_map[i]['Place']
        # any other place on the board that has no player on it
        else:
            places.append(the_map[i]['Abbrev'].ljust(5) + '\n')
    # will display board
    the_board = display_board(places)
    print(the_board)
    return spot1, spot2


# will roll for the current player
# parameters: is it player 1's turn, player info dictionary, property dictionary
def take_turn(player1_turn, player_info, the_map):
    turn = True
    roll = randint(1, 6) + randint(1, 6)
    # if player1_turn == True, will roll for player1
    if player1_turn:
        player_info['Player1']['Roll Count'] += roll
        turn = False
    # if not, will roll for player2
    elif not player1_turn:
        player_info['Player2']['Roll Count'] += roll
        turn = True
    # updates position on the board for each player
    player_info['Player1']['Position'] = player_info['Player1']['Roll Count'] \
                                         % len(the_map)
    player_info['Player2']['Position'] = player_info['Player2']['Roll Count'] \
                                         % len(the_map)
    return turn, roll


# everything is run here
def play_game(starting_money, pass_go_money, board_file):
    # the_map = board_file as a dictionary
    the_map = load_map(board_file)
    # set to True before the while loop
    player1_turn = True

    # adds new keys owner and building to the property dictionaries
    for place in the_map:
        place['Owner'] = "BANK"
        place['Building'] = "No"

    # creates a dictionary of dictionaries of player info
    # roll count adds up the number of rolls for a person
    player_info = {
        'Player1': {
            'Name': input("Player 1, what is your name? "),
            'Symbol': input("Player 1, what symbol do you want to use? "),
            'Balance': starting_money,
            'Roll Count': START_POS,
            'Position': START_POS,
            'Properties': []
        },
        'Player2': {
            'Name': input("Player 2, what is your name? "),
            'Symbol': input("Player 2, what symbol do you want to use? "),
            'Balance': starting_money,
            'Roll Count': START_POS,
            'Position': START_POS,
            'Properties': []
        }
    }

    # game starts here and loop will end
    # once someone's value is negative or 0
    while player_info['Player1']['Balance'] > 0 \
            and player_info['Player2']['Balance'] > 0:
        current_roll_count1 = player_info['Player1']['Roll Count']
        current_roll_count2 = player_info['Player2']['Roll Count']
        current_position1 = player_info['Player1']['Position']
        current_position2 = player_info['Player2']['Position']

        # calls take turn function
        turn, roll = take_turn(player1_turn, player_info, the_map)

        # calls format display function
        spot1, spot2 = format_display(the_map, player_info['Player1']['Symbol'],
                        player_info['Player1']['Position'],
                        player_info['Player2']['Symbol'],
                        player_info['Player2']['Position'])

        # adds pass go money when players pass location 0 (starting point)
        # if their position is less than current_position, they've passed go
        if player_info['Player1']['Position'] < current_position1:
            player_info['Player1']['Balance'] += pass_go_money
        if player_info['Player2']['Position'] < current_position2:
            player_info['Player2']['Balance'] += pass_go_money

        # prints out where the player landed and their roll
        if current_roll_count1 < player_info['Player1']['Roll Count']:
            print(player_info['Player1']['Name'] + " has rolled a " + str(roll))
            print(player_info['Player1']['Name'] + " has landed on " + spot1)
            # if a player lands on someone else's property
            if the_map[player_info['Player1']['Position']]['Place'] \
                    in player_info['Player2']['Properties']:
                # rent = property's rent depending on if there's a building there
                rent = the_map[player_info['Player1']['Position']]['Rent']
                if the_map[player_info['Player1']['Position']]['Building']\
                        == "Yes":
                    rent = \
                        the_map[player_info['Player1']['Position']]['BuildingRent']
                # subtracts rent from player's balance
                player_info['Player1']['Balance'] -= int(rent)
                # adds rent to player's balance
                player_info['Player2']['Balance'] += int(rent)
                print(player_info['Player2']['Name'] + " owns " + spot1
                      + ". You pay " + rent + " to them")

        # same code but i was lazy
        elif current_roll_count2 < player_info['Player2']['Roll Count']:
            print(player_info['Player2']['Name'] + " has rolled a " + str(roll))
            print(player_info['Player2']['Name'] + " has landed on " + spot2)
            if the_map[player_info['Player2']['Position']]['Place'] \
                    in player_info['Player1']['Properties']:
                rent = the_map[player_info['Player2']['Position']]['Rent']
                if the_map[player_info['Player2']['Position']]['Building'] \
                        == "Yes":
                    rent = \
                        the_map[player_info['Player2']['Position']]['BuildingRent']
                player_info['Player2']['Balance'] -= int(rent)
                player_info['Player1']['Balance'] += int(rent)
                print(player_info['Player1']['Name'] + " owns " + spot1
                      + ". You pay " + rent + " ducats to them")

        # prints player options and asks them what they want to do
        print("\n\t" + "1) Buy Property" +
              "\n\t" + "2) Get Property Info" +
              "\n\t" + "3) Get Player Info" +
              "\n\t" + "4) Build a Building" +
              "\n\t" + "5) End Turn")
        choice = input("\tWhat do you want to do? ")

        # loop ends when they decide to end their turn
        while choice.lower() != CHOICE_5 and choice.lower() != "end turn":
            # player options and calls corresponding function
            if choice.lower() == CHOICE_1 or choice.lower() == "buy property":
                buy_property(player_info, player1_turn, the_map)
            if choice.lower() == CHOICE_2 or choice.lower() == "get property info":
                get_property(the_map)
            if choice.lower() == CHOICE_3 or choice.lower() == "get player info":
                get_player(player_info)
            if choice.lower() == CHOICE_4 or choice.lower() == "build a building":
                buy_building(player_info, the_map, player1_turn)
            print("\n\t" + "1) Buy Property" +
                  "\n\t" + "2) Get Property Info" +
                  "\n\t" + "3) Get Player Info" +
                  "\n\t" + "4) Build a Building" +
                  "\n\t" + "5) End Turn")
            choice = input("\tWhat do you want to do? ")

        # sets player1_turn to turn from take_turn function
        player1_turn = turn

    # game over display message
    print("\nGAME OVER")
    for player in player_info:
        if player_info[player]['Balance'] > 0:
            print(player_info[player]['Name'] + " has won")
        else:
            print("Tie")


if __name__ == '__main__':
    # not sure what I was supposed to write as the board file parameter
    play_game(STARTING_MONEY, PASS_GO_MONEY, 'proj1_board1.csv')