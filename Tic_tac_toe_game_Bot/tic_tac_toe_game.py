#!/usr/bin/python3.12
"""
Бот для игры в крестики-нолики в Телеграм
"""
import datetime
import logging
import os
# from copy import deepcopy

import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

TOKEN = os.getenv("TG_TOKEN")

# SIZE = 4

WAITING_FOR_SIZE, CONTINUE_GAME, FINISH_GAME = range(3)

FREE_SPACE = "."
CROSS = "❎"
ZERO = "⭕"


# DEFAULT_STATE = [[FREE_SPACE for _ in range(SIZE)] for _ in range(SIZE)]


def get_fname():
    """Get filename for new log file"""
    return datetime.datetime.now().strftime("%d_%m_%Y__%H_%M_%S")


def get_default_state(size):
    """Вспомогательная функция для копирования исходного поля"""
    return [[FREE_SPACE for _ in range(size)] for _ in range(size)]


def generate_keyboard(state: list[list[str]], size: int) -> list[list[InlineKeyboardButton]]:
    """Генерирует клавиатуру для игры в крестики-нолики размером SIZExSIZE (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f"{r}{c}")
            for c in range(size)
        ]
        for r in range(size)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    keyboard = [
        [
            InlineKeyboardButton('3', callback_data='3'),
            InlineKeyboardButton('4', callback_data='4')
        ],
        [
            InlineKeyboardButton('5', callback_data='5'),
            InlineKeyboardButton('6', callback_data='6')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{update.message.from_user.first_name}, добро пожаловать в игру! "
        "Выберите размер игрового поля:",
        reply_markup=reply_markup,
    )

    return WAITING_FOR_SIZE


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('start_game_start')
    query = update.callback_query
    size = int(query.data)
    context.user_data["size"] = size
    print(context.user_data["size"])
    context.user_data["keyboard_state"] = get_default_state(size)
    keyboard = generate_keyboard(context.user_data["keyboard_state"], size)
    # print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Ваш ход! Поставьте X на любое свободное место",
        reply_markup=reply_markup,
    )
    # print(update.message.from_user.first_name)
    # print(context.user_data)
    print('start_game_end')
    return CONTINUE_GAME


async def player_move(update, context, query) -> int:
    """Function for handling inline keyboard presses"""
    keyboard = context.user_data["keyboard_state"]
    print(keyboard)
    # print(update.callback_query.message)
    r, c = map(int, query.data)
    print('player_move: ', r, c)
    if keyboard[r][c] != FREE_SPACE:
        # если тыкает в занятую клетку не первый раз подряд - больше ничего не меняем
        if "в занятую ячейку" in update.callback_query.message.text:
            return FINISH_GAME
        # если первый раз
        await context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.id,
            text="Вы сходили в занятую ячейку. Пожалуйста, выберите другую",
            reply_markup=query.message.reply_markup,
        )
        return FINISH_GAME

    new_val = CROSS
    keyboard[r][c] = new_val
    context.user_data["keyboard_state"] = keyboard
    print(context.user_data["keyboard_state"])
    print('end player move')
    return CONTINUE_GAME


async def game_over(update, context, who: str) -> int:
    """Function to end the game"""
    await before_end(update, context, who)
    return await end(update, context)


async def check_end(update, context) -> int:
    """Проверка, произошёл ли выигрыш/проигрыш/ничья"""
    print('1 check')
    if won(context.user_data["keyboard_state"], CROSS):
        # выиграл игрок
        logging.info("player won")
        return await game_over(update, context, "player")
    else:
        # Если бот сходил - проверяем, выиграл ли
        # Если бот не сходил (некуда) - ничья.
        if bot_move(context.user_data["keyboard_state"]):
            if won(context.user_data["keyboard_state"], ZERO):
                logging.info("bot won")
                return await game_over(update, context, "bot")
        else:
            logging.info("happy won")
            return await game_over(update, context, "happy")
    print('2 check')
    return CONTINUE_GAME


async def continue_or_end(update, context, query) -> int:
    """Если произошёл выигрыш/проигрыш/ничья, игра завершается.
    Иначе предыдущее сообщение удаляется и игра продолжается.
    """
    print('1 cont or end')
    if not await check_end(update, context):
        return FINISH_GAME
    print('1.5 cont or end')
    # удаление предыдущего сообщения
    await context.bot.delete_message(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.id,
    )

    size = context.user_data["size"]
    keyboard = generate_keyboard(context.user_data["keyboard_state"], size)
    reply_markup = InlineKeyboardMarkup(keyboard)
    print('2 cont_or_end')
    await context.application.bot.sendMessage(
        text=f"{query.from_user.first_name}, Ваш ход! "
        "Поставьте X на любое свободное место",
        chat_id=update.callback_query.message.chat.id,
        reply_markup=reply_markup,
    )
    print('end cont or end')
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    print('game!')
    # size = context.user_data["size"]
    query = update.callback_query
    # print(query)
    if await query.answer():
        print('query сработал ')
        if await player_move(update, context, query) != CONTINUE_GAME:
            print('ход сработал')
            return CONTINUE_GAME

        return await continue_or_end(update, context, query)
    else:
        logging.info("Problems")
    print('конец хода')
    return CONTINUE_GAME


def bot_move(fields: list[list[str]]) -> bool:
    """
    Случайно выбирает одну из свободных ячеек FREE_SPACE и ставит в неё ZERO
    Возвращает True, если удалось найти свободное место и False иначе.
    """
    free_cells = []
    for i in range(len(fields)):
        for j in range(len(fields)):
            if fields[i][j] == FREE_SPACE:
                free_cells.append(str(i) + str(j))
    if not free_cells:
        return False

    i, j = map(int, random.choice(free_cells))
    fields[i][j] = ZERO
    return True


def won_by_main_diag(fields: list[list[str]], who: str) -> bool:
    "Проверка, есть ли выигрышная комбинация на главной диагонали"
    win = True
    for i in range(len(fields)):
        if fields[i][i] != who:
            win = False
            break
    return win


def won_by_side_diag(fields: list[list[str]], who: str) -> bool:
    "Проверка, есть ли выигрышная комбинация на побочной диагонали"
    win = True
    for i in range(len(fields)):
        if fields[i][-1-i] != who:
            win = False
            break
    return win


def won_by_rows(fields: list[list[str]], who: str) -> bool:
    "Проверка, есть ли выигрышная комбинация хотя бы в одной строке"
    for i in range(len(fields)):
        win = True
        for j in range(len(fields)):
            if fields[i][j] != who:
                win = False
                break
        if win is True:
            return True
    return False


def won_by_columns(fields: list[list[str]], who: str) -> bool:
    "Проверка, есть ли выигрышная комбинация хотя бы в одном столбце"
    for i in range(len(fields)):
        win = True
        for j in range(len(fields)):
            if fields[j][i] != who:
                win = False
                break
        if win is True:
            return True
    return False


def won(fields: list[list[str]], who: str) -> bool:
    """Проверка выигрыша для игрока who"""
    return (won_by_main_diag(fields, who) or
            won_by_side_diag(fields, who) or
            won_by_rows(fields, who) or
            won_by_columns(fields, who))


async def before_end(update: Update, context: ContextTypes.DEFAULT_TYPE, who: str) -> None:
    """При завершении игры:
    остаётся последнее отправленное сообщение,
    остаётся клавиатура с последним ходом,
    снизу отправляется ещё одно сообщение с результатом партии
    и приглашением сыграть снова
    """
    keyboard = generate_keyboard(context.user_data["keyboard_state"], context.user_data["size"])
    reply_markup = InlineKeyboardMarkup(keyboard)
    play_again = "Чтобы начать новую игру, нажмите /start"
    await context.bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.id,
        reply_markup=reply_markup,
    )
    if who == "player":
        text = "Поздравляем, Вы победили!\n"
    elif who == "bot":
        text = "К сожалению, Вы проиграли 😔\n"
    elif who == "happy":
        text = "Вы сыграли вничью!\n"
    await context.application.bot.sendMessage(
        text=text + play_again,
        chat_id=update.callback_query.message.chat.id,
    )


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data["keyboard_state"] = get_default_state()
    return ConversationHandler.END


# def get_size(context: ContextTypes.DEFAULT_TYPE) -> int:
#     return context.user_data["size"]

def main() -> None:
    """Run the bot"""

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        filename=f"logs/{get_fname()}.log",
        filemode="a",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_SIZE: [
                CallbackQueryHandler(start_game, pattern="^" + f"{i}" + "$")
                for i in range(3, 7)
            ],
            CONTINUE_GAME: [
                CallbackQueryHandler(game)
                # , pattern="^" + f"{r}{c}" + "$")
                # for r in range(get_size(ContextTypes.DEFAULT_TYPE))
                # for c in range(get_size(ContextTypes.DEFAULT_TYPE))
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end)
                # , pattern="^" + f"{r}{c}" + "$")
                # for r in range(get_size(ContextTypes.DEFAULT_TYPE))
                # for c in range(get_size(ContextTypes.DEFAULT_TYPE))
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application
    # that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
