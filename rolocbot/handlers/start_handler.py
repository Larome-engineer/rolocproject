from data.messages import *
from aiogram import Router, F
from keyboards.user_kb import user_menu_kb
from keyboards.admin_kb import adm_main_menu_kb
from aiogram.fsm.context import FSMContext
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.filters.command import CommandStart
from services.user_service import check_on_exists
from aiogram.types import Message, CallbackQuery, BotCommand, BotCommandScopeDefault

start_router = Router()


async def set_commands(bot: roloc_bot):
    return await roloc_bot.set_my_commands(
        commands=[
            BotCommand(command='start', description=command_start),
            BotCommand(command='about', description=command_about),
            BotCommand(command='help', description=command_helps)
        ], scope=BotCommandScopeDefault()
    )


@start_router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    if msg.from_user.id in ADMIN_IDS:
        await roloc_bot.send_message(msg.from_user.id, adm_hello, reply_markup=adm_main_menu_kb().as_markup())
    else:
        user = check_on_exists(msg.from_user.id)
        if user is False:
            await roloc_bot.send_message(msg.from_user.id, msg_hello, reply_markup=user_menu_kb().as_markup())
        elif user is not None:
            await roloc_bot.send_message(msg.from_user.id, f"{msg_hello_exists}, {user['name']}",
                                         reply_markup=user_menu_kb().as_markup())
        else:
            await roloc_bot.send_message(msg.from_user.id, msg_hello, reply_markup=user_menu_kb().as_markup())

    await set_commands(roloc_bot)


@start_router.callback_query(F.data.startswith("back"))
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    if callback.from_user.id in ADMIN_IDS:
        await callback.message.edit_text(adm_hello, reply_markup=adm_main_menu_kb().as_markup())
    else:
        await callback.message.edit_text(msg_hello, reply_markup=user_menu_kb().as_markup())
