from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import Config
from database import Database
from keyboards import Keyboards

router = Router()
db = Database()


def is_admin(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID


@router.message(Command("calendar"))
async def show_calendar(message: Message):
    if not is_admin(message.from_user.id):
        return
    dates = db.get_dates_with_entries()
    await message.answer("Даты с записями:", reply_markup=Keyboards.admin_dates(dates))


@router.callback_query(F.data.startswith("admin_date:"))
async def show_entries(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    date = callback.data.split(":", 1)[1]
    entries = db.get_entries_by_date(date)
    if not entries:
        text = f"На {date} записей нет"
    else:
        lines = [f"Записи на {date}:"]
        for service, time, name, phone, telegram in entries:
            lines.append(f"{time} — {service} — {name} — {telegram} — {phone}")
        text = "\n".join(lines)
    await callback.message.answer(text)
    await callback.answer()
