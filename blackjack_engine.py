import random

class Player:
    def __init__(self):
        self.balance = 1000
        self.cards = []

    def get_balance(self):
        return str(self.balance)

    def get_sum(self):
        sum = 0
        for i in self.cards:
            sum += i[1]
        return sum

    def get_start_hand(self, DeckObj):
        self.cards.append(DeckObj.give_card())
        self.cards.append(DeckObj.give_card())
        return self.cards

    def blackjack(self):
        if self.get_sum() == 21:
            return True

    def is_alive(self):
        sum = self.get_sum()
        if sum <= 21:
            return True
        else:
            return False

    def draw_more(self, DeckObj):
        self.cards.append(DeckObj.give_card())
        return self.cards

    def leave_cards(self):
        self.cards = []

class Dealer(Player):
    def draw_dealer_cards(self):
        if self.get_sum() < 17:
            return True
        else:
            return False

class Deck:
    def __init__(self):
        # H = heart, D = diamond, C = club, S = spade
        self.deck = {
            '2H': 2, '2D': 2, '2C': 2, '2S': 2,
            '3H': 3, '3D': 3, '3C': 3, '3S': 3,
            '4H': 4, '4D': 4, '4C': 4, '4S': 4,
            '5H': 5, '5D': 5, '5C': 5, '5S': 5,
            '6H': 6, '6D': 6, '6C': 6, '6S': 6,
            '7H': 7, '7D': 7, '7C': 7, '7S': 7,
            '8H': 8, '8D': 8, '8C': 8, '8S': 8,
            '9H': 9, '9D': 9, '9C': 9, '9S': 9,
            'JH': 10, 'JD': 10, 'JC': 10, 'JS': 10,
            'QH': 10, 'QD': 10, 'QC': 10, 'QS': 10,
            'KH': 10, 'KD': 10, 'KC': 10, 'KS': 10,
        }

    def give_card(self):
        card1 = random.choice(list(self.deck.items()))
        self.deck.pop(card1[0])
        return card1

