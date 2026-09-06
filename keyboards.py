from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import Config


class Keyboards:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="О нас", callback_data="about")],
                [InlineKeyboardButton(text="Записаться", callback_data="make_an")],
            ]
        )

    @staticmethod
    def services() -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=service, callback_data=f"service:{service}")]
            for service in Config.SERVICES
        ]
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_start")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def dates() -> InlineKeyboardMarkup:
        buttons = []
        today = datetime.now()
        for i in range(Config.DAYS_AHEAD):
            day = today + timedelta(days=i)
            label = day.strftime("%d.%m")
            value = day.strftime("%d.%m.%Y")
            buttons.append([InlineKeyboardButton(text=label, callback_data=f"date:{value}")])
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="make_an")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def slots(available_slots: list[str]) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=slot, callback_data=f"slot:{slot}")]
            for slot in available_slots
        ]
        if not buttons:
            buttons.append([InlineKeyboardButton(text="Нет свободных слотов", callback_data="no_slots")])
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_dates")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def admin_dates(dates: list[str]) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=date, callback_data=f"admin_date:{date}")]
            for date in dates
        ]
        if not buttons:
            buttons.append([InlineKeyboardButton(text="Записей нет", callback_data="no_entries")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)
