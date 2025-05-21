from aiogram.filters import Command

from utils.limitignore import get_result_for_user
from data.messages import *
from aiogram import Router, F

from keyboards.user_kb import user_menu_kb
from aiogram.fsm.context import FSMContext

from services.help_service import create_help_service, helps_by_tg_id
from services.user_service import id_by_tg_id_service
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

help_router = Router()


class HelpState(StatesGroup):
    name = State()
    helptext = State()
    contacts = State()


@help_router.message(Command('help'))
async def user_help_command(msg: Message, state: FSMContext):
    await state.clear()
    user_id = id_by_tg_id_service(msg.from_user.id)
    if user_id is None:
        await state.set_state(HelpState.name)
        await roloc_bot.send_message(msg.from_user.id, f'<strong>📝 Оформление заявки о помощи\n\n</strong>')
        await roloc_bot.send_message(msg.from_user.id, msg_uname)
    elif not user_id:
        await roloc_bot.send_message(msg.from_user.id, msg_help_error, reply_markup=user_menu_kb().as_markup())
    elif user_id is not None:
        await state.set_state(HelpState.helptext)
        await state.update_data(user_tg_id=msg.from_user.id)
        await roloc_bot.send_message(msg.from_user.id, msg_uprbl)


@help_router.callback_query(F.data.startswith('usermenu3'))
async def user_help_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    user_id = id_by_tg_id_service(callback.from_user.id)
    if user_id is None:
        await state.set_state(HelpState.name)
        await callback.message.edit_text(msg_uname)
    elif not user_id:
        await callback.message.edit_text(msg_help_error, reply_markup=user_menu_kb().as_markup())
    elif user_id is not None:
        await state.set_state(HelpState.helptext)
        await state.update_data(user_tg_id=callback.from_user.id)
        await callback.message.edit_text(msg_uprbl)

@help_router.callback_query(F.data.startswith('usermenu5'))
async def get_all_user_helps(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    helps = helps_by_tg_id(callback.from_user.id)
    if helps is None:
        await callback.message.edit_text(msg_userhelps_noexs, reply_markup=user_menu_kb().as_markup())
    elif not helps:
        await callback.message.edit_text(msg_userhelps_failed, reply_markup=user_menu_kb().as_markup())
    elif helps is not None:
        await get_result_for_user(callback, helps, roloc_bot)


@help_router.message(HelpState.name)
async def user_help_name(msg: Message, state: FSMContext):
    if not msg.text:
        await roloc_bot.send_message(msg.from_user.id, msg_media)
        await state.set_state(HelpState.name)
        await roloc_bot.send_message(msg.from_user.id, msg_uname)
    else:
        await state.update_data(name=msg.text)
        await state.set_state(HelpState.helptext)
        await roloc_bot.send_message(msg.from_user.id, msg_uprbl)


@help_router.message(HelpState.helptext)
async def user_help_text(msg: Message, state: FSMContext):
    if not msg.text:
        await roloc_bot.send_message(msg.from_user.id, msg_media)
        await state.set_state(HelpState.helptext)
        await roloc_bot.send_message(msg.from_user.id, msg_uprbl)
    else:
        await state.update_data(helptext=msg.text)
        help_data = await state.get_data()

        if msg.from_user.id in help_data.values():
            await state.clear()
            created = create_help_service(help_data)
            if created[0]:
                help_data['name'] = created[1]['name']
                help_data['username'] = created[1]['tg_username']
                help_data['contacts'] = created[1]['phone']
                text = text_perform(help_data)
                for admin_id in ADMIN_IDS:
                    await roloc_bot.send_message(admin_id, text)
                await roloc_bot.send_message(msg.from_user.id, msg_procd, reply_markup=user_menu_kb().as_markup())
            elif not created[0]:
                await roloc_bot.send_message(msg.from_user.id, msg_help_error, reply_markup=user_menu_kb().as_markup())
        else:
            await state.update_data(helptext=msg.text)
            await state.set_state(HelpState.contacts)
            await roloc_bot.send_message(msg.from_user.id, msg_contc)


@help_router.message(HelpState.contacts)
async def user_help_contact(msg: Message, state: FSMContext):
    if not msg.text:
        await roloc_bot.send_message(msg.from_user.id, msg_media)
        await state.set_state(HelpState.contacts)
        await roloc_bot.send_message(msg.from_user.id, msg_contc)
    else:
        await state.update_data(contacts=msg.text)
        user_help_data = await state.get_data()
        user_help_data['user_tg_id'] = msg.from_user.id
        user_help_data['username'] = msg.from_user.username
        await state.clear()

        text = text_perform(user_help_data)
        created = create_help_service(user_help_data)
        if not created:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_message(admin_id, f"{msg_dberr_help}\n\n{text}")
            await roloc_bot.send_message(msg.from_user.id, msg_procd, reply_markup=user_menu_kb().as_markup())

        elif created[0]:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_message(admin_id, text)
            await roloc_bot.send_message(msg.from_user.id, msg_procd, reply_markup=user_menu_kb().as_markup())


def text_perform(help_data: dict):
    user_id = help_data['user_tg_id']
    username = help_data['username']
    name = help_data['name']
    help_text = help_data['helptext']
    contacts = help_data['contacts']

    if username is None:
        username = "-"

    return (f"🆘 <strong>ПОМОЩЬ</strong>\n\n"
            f"👨‍💻 Пользователь:\n"
            f"• ID: <code>{user_id}</code>\n"
            f"• Username: <code>@{username}</code>\n"
            f"• Имя: {name}\n"
            f"• Контакты: <code>{contacts}</code>\n\n"
            f"✏️<strong>:</strong> {help_text}"
            )
