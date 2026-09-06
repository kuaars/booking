from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from database import Database
from keyboards import Keyboards
from states import BookingStates

router = Router()
db = Database()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добро пожаловать!", reply_markup=Keyboards.start())


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Добро пожаловать!", reply_markup=Keyboards.start())
    await callback.answer()


@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    await callback.message.edit_text(Config.ABOUT_TEXT, reply_markup=Keyboards.start())
    await callback.answer()


@router.callback_query(F.data == "make_an")
async def choose_service(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.choosing_service)
    await callback.message.edit_text("Выберите услугу:", reply_markup=Keyboards.services())
    await callback.answer()


@router.callback_query(BookingStates.choosing_service, F.data.startswith("service:"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split(":", 1)[1]
    await state.update_data(service=service)
    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text("Выберите дату:", reply_markup=Keyboards.dates())
    await callback.answer()


@router.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text("Выберите дату:", reply_markup=Keyboards.dates())
    await callback.answer()


@router.callback_query(BookingStates.choosing_date, F.data.startswith("date:"))
async def choose_slot(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split(":", 1)[1]
    data = await state.get_data()
    service = data["service"]
    booked = db.get_booked_slots(service, date)
    available = Config.SLOTS if Config.ALLOW_MULTIPLE_BOOKINGS else [s for s in Config.SLOTS if s not in booked]
    await state.update_data(date=date)
    await state.set_state(BookingStates.choosing_slot)
    await callback.message.edit_text(
        f"Услуга: {service}\nДата: {date}\nВыберите время:",
        reply_markup=Keyboards.slots(available),
    )
    await callback.answer()


@router.callback_query(BookingStates.choosing_slot, F.data.startswith("slot:"))
async def enter_name(callback: CallbackQuery, state: FSMContext):
    slot = callback.data.split(":", 1)[1]
    await state.update_data(slot=slot)
    await state.set_state(BookingStates.entering_name)
    await callback.message.edit_text("Введите ваше имя:")
    await callback.answer()


@router.message(BookingStates.entering_name)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.entering_phone)
    await message.answer("Введите ваш номер телефона:")


@router.message(BookingStates.entering_phone)
async def finish_booking(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text
    username = f"@{message.from_user.username}" if message.from_user.username else str(message.from_user.id)

    db.add_entry(
        service=data["service"],
        date=data["date"],
        time=data["slot"],
        name=data["name"],
        phone=phone,
        telegram=username,
    )

    await message.answer(
        f"Вы записаны!\nУслуга: {data['service']}\nДата: {data['date']}\nВремя: {data['slot']}",
        reply_markup=Keyboards.start(),
    )

    await message.bot.send_message(
        Config.ADMIN_ID,
        f"{data['service']}\n{data['date']}, {data['slot']}\n{data['name']}\n{username}\n{phone}",
    )

    await state.clear()
