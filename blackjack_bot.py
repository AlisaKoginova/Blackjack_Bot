import telebot
import emoji
import blackjack_engine

bot = telebot.TeleBot("824642016:AAGdqfBwDRzesEdl0-efH_0emqETDwNyT78")

SUIT = {
    'S': ':spade_suit:',
    'C': ':club_suit:',
    'H': ':heart_suit:',
    'D': ':diamond_suit:'
}

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row(emoji.emojize(':game_die:') + ' Начать игру',
              emoji.emojize(':blue_book:') + ' Правила')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Взять карту', 'Оставить')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row()

deck = blackjack_engine.Deck()
user = blackjack_engine.Player()
dealer = blackjack_engine.Dealer()

def show_player_cards(cards):
    cards_info = 'Ваши карты:  '
    for i in cards:
        cards_info += f' {i[0][0]}' + emoji.emojize(SUIT[i[0][1]])
    return cards_info

def show_dealer_cards(cards):
    cards_info = 'Карты дилера:  '
    for i in cards:
        cards_info += f' {i[0][0]}' + emoji.emojize(SUIT[i[0][1]])
    return cards_info

def show_player_sum(player_sum):
    return emoji.emojize(':red_circle:') + f' Сумма ваших карт:  {player_sum}'

def show_dealer_sum(dealer_sum):
    return emoji.emojize(':red_circle:') + f' Сумма карт дилера:  {dealer_sum}'

def show_player_drawen_card(cards):
    drawen_player_card = 'Вы получаете: '
    drawen_player_card += f'{ cards[-1][0][0]}' + emoji.emojize(SUIT[cards[-1][0][1]])
    return drawen_player_card

def show_dealer_drawen_card(cards):
    drawen_dealer_card = 'Диллер получает: '
    drawen_dealer_card += f'{ cards[-1][0][0]}' + emoji.emojize(SUIT[cards[-1][0][1]])
    return drawen_dealer_card

def player_loose():
    return emoji.emojize(':skull_and_crossbones:') +\
           'Перебор!\n Вы проиграли. Победа диллера.'

def dealer_loose():
    return  f'У диллера перебор!\n' + emoji.emojize(':trophy:') + \
            ' Поздравляем, Вы выиграли!'

def player_victory():
    return emoji.emojize(':trophy:') + ' Поздравляем, Вы выиграли!'

def dealer_victory():
    return emoji.emojize(':skull_and_crossbones:') + ' Проигрыш, победа диллера.'

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}'
                     + emoji.emojize(':military_medal:')
                     + '\n' + 'Ваш баланс: ' + emoji.emojize(':dollar_banknote:')
                     + user.get_balance(),
                     reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def answer_message(message):
    if message.text == emoji.emojize(':game_die:') + ' Начать игру':
        bot.send_message(message.chat.id, 'Игра началась!' + emoji.emojize(':fire:'),
                         reply_markup=keyboard2)
        user.get_start_hand(deck) # [(qh, 4)] spade_suit heart_suit diamond_suit club_suit

        bot.send_message(message.chat.id, show_player_cards(user.cards),
                         reply_markup=keyboard2)

        bot.send_message(message.chat.id, show_player_sum(user.get_sum()),
                         reply_markup=keyboard2)

        if user.blackjack():
            bot.send_message(message.chat.id, f'Поздравляем, блэкджек!',
                             reply_markup=keyboard2)

        bot.send_message(message.chat.id, 'Диллер берет карты...', reply_markup=keyboard2)
        dealer.get_start_hand(deck)
        bot.send_message(message.chat.id, show_dealer_cards(dealer.cards),
                         reply_markup=keyboard2)
        bot.send_message(message.chat.id, emoji.emojize(':red_circle:') +
                         f' Сумма карт диллера:  {dealer.get_sum()}',
                         reply_markup=keyboard2)

        if dealer.blackjack():
            bot.send_message(message.chat.id, f'У диллера блэкджек!',
                             reply_markup=keyboard2)

        if dealer.blackjack() and user.blackjack():
            bot.send_message(message.chat.id, f'Ничья \nНачать следующую игру?',
                             reply_markup=keyboard1)
        elif not dealer.blackjack() and user.blackjack():
            bot.send_message(message.chat.id, emoji.emojize(':trophy:') +
                             f'Вы выиграли! \nНачать следующую игру?',
                             reply_markup=keyboard1)
        elif dealer.blackjack() and not user.blackjack():
            bot.send_message(message.chat.id, emoji.emojize(':skull_and_crossbones:') +
                             f'Вы проиграли! \nНачать следующую игру?',
                             reply_markup=keyboard1)

    if message.text == 'Взять карту':
        user.draw_more(deck)
        bot.send_message(message.chat.id, show_player_drawen_card(user.cards),
                         reply_markup=keyboard2)
        bot.send_message(message.chat.id, show_player_cards(user.cards),
                         reply_markup=keyboard2)
        bot.send_message(message.chat.id, show_player_sum(user.get_sum()),
                         reply_markup=keyboard2)

        if not user.is_alive():
            user.leave_cards()
            dealer.leave_cards()
            deck.__init__()
            bot.send_message(message.chat.id, player_loose(),
                         reply_markup=keyboard1)
        elif user.blackjack():
            user.leave_cards()
            dealer.leave_cards()
            deck.__init__()
            bot.send_message(message.chat.id, emoji.emojize(':trophy:') +
                             ' Поздравляем! У вас блэкджек!', reply_markup=keyboard1)

    if message.text == 'Оставить':
        print('ko')
        while dealer.get_sum() < 17:
            dealer.draw_more(deck)
            bot.send_message(message.chat.id, show_dealer_drawen_card(dealer.cards),
                             reply_markup=keyboard3)
            bot.send_message(message.chat.id, show_dealer_cards(dealer.cards),
                             reply_markup=keyboard3)
            bot.send_message(message.chat.id, show_dealer_sum(dealer.get_sum()),
                             reply_markup=keyboard3)

            if not dealer.is_alive():
                user.leave_cards()
                dealer.leave_cards()
                deck.__init__()
                bot.send_message(message.chat.id, dealer_loose(),
                             reply_markup=keyboard1)
                break

            elif dealer.blackjack():
                user.leave_cards()
                dealer.leave_cards()
                deck.__init__()
                bot.send_message(message.chat.id, emoji.emojize(':skull_and_crossbones:') +
                        ' У диллера блэкджек!\nВы проиграли.',
                        reply_markup=keyboard1)
                break

        if user.is_alive() and dealer.is_alive():
            if user.get_sum() == dealer.get_sum():
                user.leave_cards()
                dealer.leave_cards()
                deck.__init__()
                bot.send_message(message.chat.id, f'Начать следующую игру?',
                                 reply_markup=keyboard1)
            elif user.get_sum() > dealer.get_sum():
                user.leave_cards()
                dealer.leave_cards()
                deck.__init__()
                bot.send_message(message.chat.id, player_victory(),
                                 reply_markup=keyboard1)
                bot.send_message(message.chat.id, 'Начать следующую игру?',
                                 reply_markup=keyboard1)
            elif user.get_sum() < dealer.get_sum():
                user.leave_cards()
                dealer.leave_cards()
                deck.__init__()
                bot.send_message(message.chat.id, dealer_victory(),
                                 reply_markup=keyboard1)
                bot.send_message(message.chat.id, 'Начать следующую игру?',
                                 reply_markup=keyboard1)

    if message.text == emoji.emojize(':blue_book:') + ' Правила':
        bot.send_message(message.chat.id, 'Ошибочно считается, что цель заключается в том,'
                'чтобы набрать как можно больше очков, но не более 21. '
                'На самом деле цель — обыграть дилера (крупье). Значения очков '
                'каждой карты: от двойки до десятки — от 2 до 10 соответственно, '
                'у туза — 1 или 11 (11 пока общая сумма не больше 21, далее 1), '
                'у т. н. картинок (король, дама, валет) — 10. Изначально и диллер'
                ' и игрок получает 2 карты. Далее игрок имеет право добирать карты '
                'или оставить. После того, как все '
                'игрок завершил брать карты, дилер говорит «себе» и раздаёт карты себе. '
                 'Выигравшим считается тот, у кого больше очков, но не более 21.',
                         reply_markup=keyboard1)
# for getting sticker id
# @bot.message_handler(content_types=['sticker'])
# def get_sticker_id(message):
# 	print(message)

bot.polling()
