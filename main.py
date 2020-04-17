import os
import random
from itertools import combinations

class Card():
    def __init__(self, color, value, points=0):
        self.value = value
        self.color = color
        self.points = points

class CardGame():
    def_card_game = {"spade": list(range(1, 10)),
             "club" : list(range(1,10)),
             "heart": list(range(1,10)),
             "diamond": list(range(1,10))
}
    def __init__(self):
        self.card_game = []
        for color,values in self.def_card_game.items():
            for value in values:
                if color == "diamond" and value == 7:
                    self.card_game.append(Card(color, value, 1))
                else:
                    self.card_game.append(Card(color, value))

class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.won_cards = []
        self.board_game = None
    
    def ask_what_to_play(self):
        print(f"Player {self.name}: Your cards are:")
        i = 0
        for card in self.cards:
            print(f"\tCard {i}: {card.value} {card.color}")
            i += 1
        val = input("Enter index of card you wish to play:\n")
        played_card = self.cards[int(val)]
        return played_card
    
    def play_card(self):
        self.board_game.print_board_game()
        card = self.ask_what_to_play()
        won_cards = self.board_game.play_card(card)
        if won_cards:
            self.won_cards.extend(won_cards)
        self.remove_card(card)
    
    def remove_card(self, card):
        for index,c in enumerate(self.cards):
            if c.value == card.value and c.color == card.color:
                del(self.cards[index])
                break

class BoardGame():
    def __init__(self, card_game):
        self.cards = {}
        self.card_game = card_game

    def print_board_game(self):
        print("Board game cards are:")
        for i,card in self.cards.items():
            print(f"\tCard {i}: {card.value} {card.color}")
    
    def play_card(self, card):
        same_value = [c for i,c in self.cards.items() if c.value == card.value]
        if len(same_value) == 1:
            self.remove_card_from_card_game(same_value[0])
            return [same_value[0], card]
        elif same_value:
            index = input("Enter index of the card you want to get")
            chosen_card = self.cards[index]
            del(self.cards[index])
            self.remove_card_from_card_game(chosen_card)
            return [chosen_card, card]
        else:
            combinations,cards_combinations = self.find_combination(card)
            if not combinations:
                self.add_card_to_board(card)
            else:
                if len(combinations) > 2:
                    valid_combination = False
                    chosen_cards = []
                    while not valid_combination:
                        message = "Cards that can be taken are:\n"
                        for i,c in cards_combinations.items():
                            message += f"\tCard {i}: {c.value} {c.color}\n"
                        print(message)
                        val = input("Select index of card you wish to take, separated by a comma:")
                        indexes = val.split(",")
                        for i in indexes:
                            chosen_cards.append(self.cards[int(i)])
                        value_list = sorted([c.value for c in chosen_cards])
                        if value_list in combinations:
                            valid_combination = True
                        else:
                            print("The combination chosen is not valid!")
                            chosen_cards = []
                    chosen_cards.append(card)
                    for c in chosen_cards:
                        self.remove_card_from_card_game(c)
                    return chosen_cards
                else:
                    chosen_cards = set([])
                    for value in combinations[0]:
                        for i,c in self.cards.items():
                            if c.value == value and c not in chosen_cards:
                                chosen_cards.add(c)
                    chosen_cards = list(chosen_cards)            
                    chosen_cards.append(card)
                    for c in chosen_cards:
                        self.remove_card_from_card_game(c)
                    return chosen_cards
                        
    def add_card_to_board(self, card):
        for i in range(40):
            if not i in self.cards:
                self.cards[i] = card
                break

    def find_combination(self, card):
        value = card.value
        #sorted_dict = {k: v for k, v in sorted(self.cards.items(), key=lambda item: item[1].value}
        target = card.value
        lis = [c.value for i,c in self.cards.items()]

        diffs = []
        for n in range(1, len(lis)+1):
            numbers = combinations(lis, n)
            # list the combinations and their absolute difference to target
            for combi in numbers:
                diffs.append([combi, abs(target - sum(combi))])
        diffs.sort(key=lambda x: x[1])
        possible_values = [list(d) for d,t in diffs if t == 0]
        possible_dict = {}
        if possible_values:
            for i,c in self.cards.items():
                for values in possible_values:
                    for p in values:
                        if p == c.value:
                            possible_dict[i] = c
        return [possible_values, possible_dict]
        

    def remove_card_from_card_game(self, card):
        for index,c in enumerate(self.card_game.card_game):
            if c.value == card.value and c.color == card.color:
                del(self.card_game.card_game[index])
                break
        for index,c in self.cards.items():
            if c.value == card.value and c.color == card.color:
                del(self.cards[index])
                break

class Game():
    def __init__(self, players):
        self.card_game = CardGame()
        self.players = players
        self.board_game = BoardGame(self.card_game)
        for player in self.players:
            player.board_game = self.board_game
    
    def init_game(self):
        for player in self.players:
            for i in range(3):
                index = random.randrange(len(self.card_game.card_game))
                player.cards.append(self.card_game.card_game[index])
                del(self.card_game.card_game[index])
        for i in range(4):
                index = random.randrange(len(self.card_game.card_game))
                # index = 0
                # for c in self.card_game.card_game:
                #     if c.value == 1:
                #         break
                #     index += 1
                self.board_game.cards[i] = self.card_game.card_game[index]
                del(self.card_game.card_game[index])

    def play(self):
        self.init_game()
        while len(self.card_game.card_game) > 0:
            for player in self.players:
                player.play_card()

        

if __name__ == "__main__":
    player1 = Player("player 1")
    player2 = Player("player 2")
    game = Game([player1, player2])
    game.play()

