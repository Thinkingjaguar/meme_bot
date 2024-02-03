from aiogram.utils.keyboard import InlineKeyboardBuilder


def for_admins():
    kb = InlineKeyboardBuilder()
    kb.button(text='Для программистов', callback_data='add_prog')
    kb.button(text='Для музыкантов', callback_data='add_music')
    kb.button(text='Для студентов', callback_data='add_study')
    kb.button(text='Остальные', callback_data='add_neprog')
    kb.adjust(1)
    return kb.as_markup()


def get_choose_tag():
    kb = InlineKeyboardBuilder()
    kb.button(text='Ты програмист?', callback_data='tag_prog')
    kb.button(text='А может, музыкант?', callback_data='tag_music')
    kb.button(text='Или студент?', callback_data='tag_study')
    kb.button(text='Нет? Соболезную.', callback_data='tag_neprog')
    kb.adjust(1)
    return kb.as_markup()
