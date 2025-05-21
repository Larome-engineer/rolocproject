from data.messages import *
from aiogram import Router, F
from roloc_create import roloc_bot
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from keyboards.user_kb import user_about_us_kb
from aiogram.types import CallbackQuery, Message

about_router = Router()


@about_router.message(Command('about'))
async def user_about_command(msg: Message, state: FSMContext):
    await state.clear()
    await roloc_bot.send_message(msg.from_user.id, msg_about, reply_markup=user_about_us_kb().as_markup())


@about_router.callback_query(F.data.startswith('usermenu2'))
async def user_about_us(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(msg_about, reply_markup=user_about_us_kb().as_markup())
