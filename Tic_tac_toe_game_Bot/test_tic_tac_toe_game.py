from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardButton

from tic_tac_toe_game import SIZE, get_default_state, \
    generate_keyboard, start, player_move, \
    CONTINUE_GAME, FINISH_GAME, \
    CROSS, FREE_SPACE, game, game_over


def test_size_default_state():
    assert len(get_default_state()) == SIZE  # кол-во строк
    for i in range(SIZE):
        assert len(get_default_state()[i]) == SIZE  # количество столбцов


def test_generate_keyboard():
    keyboard = generate_keyboard(get_default_state())
    for i in range(SIZE):
        for j in range(SIZE):
            assert isinstance(keyboard[i][j], InlineKeyboardButton)


pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_start():
    returned = []

    async def print_format(text, reply_markup=None):
        returned.append(text + str(reply_markup))

    context = AsyncMock()
    update = AsyncMock()
    update.message.reply_text = print_format
    update.message.from_user.first_name = "abc"
    assert await start(update, context) == 0
    assert len(returned) > 0 and ("abc" in returned[0])


@pytest.mark.asyncio
async def test_player_move():
    result = []

    async def some_editor(
        chat_id=None, message_id=None, reply_markup=None, text=None
    ):
        result.append(f"{chat_id}, {message_id}, {reply_markup}, {text}")

    context = AsyncMock()
    update = AsyncMock()
    query = AsyncMock()

    # FIRST TEST
    # test if double-click on an occupied cell
    query.data = "01"
    context.user_data = {"keyboard_state": [["."] * SIZE] * SIZE}
    context.user_data["keyboard_state"][0][1] = "a"
    update.callback_query.message.text = "blah occupied cell blah"
    assert (
        await player_move(update, context, query) == FINISH_GAME
    ), "Smth went wrong when double click on an occupied cell"

    # SECOND TEST
    # test if click on an occupied cell
    query.data = "01"
    update.callback_query.message.text = "blah blah"
    update.callback_query.message.chat.id = "1"
    update.callback_query.message.id = "2"
    query.message.reply_markup = "3"
    context.bot.edit_message_text = some_editor

    assert (
        await player_move(update, context, query) == FINISH_GAME
    ), "Smth went wrong after click on an occupied cell"

    assert (
        result[0] == "1, 2, 3,"
        " Вы сходили в занятую ячейку. Пожалуйста, выберите другую"
    ), "Smth went wrong after click on an occupied cell"

    # THIRD TEST
    # test if click on a free cell
    context.user_data["keyboard_state"][0][1] = FREE_SPACE
    assert (
        await player_move(update, context, query) == CONTINUE_GAME
    ), "smth went wrong after click on a free cell"
    assert (
        context.user_data["keyboard_state"][0][1] == CROSS
    ), "The cross was not placed"


@pytest.mark.asyncio
async def test_game_over():
    update = AsyncMock()
    context = AsyncMock()
    who = "a"
    with patch("tic_tac_toe_game.before_end") as mocked_bend, patch(
        "tic_tac_toe_game.end"
    ) as mocked_end:
        mocked_end.return_value = 0
        assert await game_over(update, context, who) == 0
        mocked_bend.assert_awaited_once()
        mocked_end.assert_awaited_once()


@pytest.mark.asyncio
async def test_game_1():
    async def get_answer():
        return True

    update = AsyncMock()
    context = AsyncMock()
    update.callback_query = AsyncMock()
    update.callback_query.answer = get_answer

    with patch("tic_tac_toe_game.player_move") as mocked:
        mocked.return_value = True
        assert await game(update, context) == CONTINUE_GAME
        mocked.assert_awaited_once()

    with patch("tic_tac_toe_game.player_move") as mocked, patch(
        "tic_tac_toe_game.continue_or_end"
    ) as cont_mocked:
        cont_mocked.return_value = 2
        mocked.return_value = False
        assert await game(update, context) == 2
        mocked.assert_awaited_once()


@pytest.mark.asyncio
async def test_game_2():
    async def get_answer():
        return False

    update = AsyncMock()
    context = AsyncMock()
    update.callback_query = AsyncMock()
    update.callback_query.answer = get_answer

    with patch("logging.info"):
        assert await game(update, context) == CONTINUE_GAME
