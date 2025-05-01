from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


mode_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Дружеский", callback_data="friendly")],
        [InlineKeyboardButton(text="Деловой", callback_data="Business")],
        [InlineKeyboardButton(text="Ироничный", callback_data="ironic")],
    ]
)
