from aiogram import Router, F

from keyboards.admin_kb import *
from services.help_service import *
from utils.limitignore import get_result
from aiogram.fsm.context import FSMContext
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

helps_router = Router()


class AdminDataHelpSearch(StatesGroup):
    help_search_id = State()
    help_search_phone = State()


class HelpChangeState(StatesGroup):
    help_id = State()
    help_status = State()


""" /////////////////// SEARCH OPTIONS //////////////////"""


@helps_router.callback_query(F.data.startswith('admsearch#help'))
async def helps_search_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(msg_search_option, reply_markup=adm_helps_search_kb().as_markup())


@helps_router.callback_query(F.data.startswith("hsearch"))
async def search_options_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await callback.answer()
        option = callback.data.split("_")[1]
        if option == 'all':
            result = all_helps()
            if result is None:
                await callback.message.edit_text(
                    msg_allhelp_noexs,
                    reply_markup=adm_helps_search_kb().as_markup()
                )
            elif not result:
                await callback.message.edit_text(
                    msg_error,
                    reply_markup=adm_helps_search_kb().as_markup()
                )
            elif result is not None:
                await get_result(callback, result, 'help', roloc_bot)

        elif option == 'hid':
            await state.set_state(AdminDataHelpSearch.help_search_id)
            await callback.message.edit_text(msg_search_helpid)
        elif option == 'sts':
            await callback.message.edit_text(
                msg_search_status,
                reply_markup=adm_check_helps_status_kb().as_markup()
            )
        elif option == 'uph':
            await state.set_state(AdminDataHelpSearch.help_search_phone)
            await callback.message.edit_text(msg_search_uphone)


@helps_router.message(AdminDataHelpSearch.help_search_id)
async def search_by_id(message: Message, state: FSMContext):
    ste = await state.get_state()
    user_id = message.from_user.id
    if user_id in ADMIN_IDS and ste == 'AdminDataHelpSearch:help_search_id':
        help_info = help_by_id(message.text)
        if help_info is None:
            await state.set_state(AdminDataHelpSearch.help_search_id)
            await roloc_bot.send_message(user_id, msg_noexs_help)
            await roloc_bot.send_message(user_id, msg_search_helpid)
        elif not help_info:
            await state.clear()
            await roloc_bot.send_message(user_id, msg_error, reply_markup=adm_helps_search_kb().as_markup())
        elif help_info is not None:
            await state.clear()
            await roloc_bot.send_message(user_id, help_info, reply_markup=adm_helps_search_kb().as_markup())


@helps_router.callback_query(F.data.startswith('opthelpsearch'))
async def search_by_status(callback: CallbackQuery):
    if callback.from_user.id in ADMIN_IDS:
        await callback.answer()
        status = help_status_dict[callback.data.split("#")[1]]
        helps = helps_by_status(status)
        if helps is None:
            await callback.message.edit_text(
                help_noexs_status,
                reply_markup=adm_helps_search_kb().as_markup()
            )
        elif not helps:
            await callback.message.edit_text(
                msg_error,
                reply_markup=adm_helps_search_kb().as_markup()
            )
        elif helps is not None:
            await get_result(callback, helps, 'help', roloc_bot)


@helps_router.message(AdminDataHelpSearch.help_search_phone)
async def search_by_phone(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        phone = message.text
        user_id = message.from_user.id
        await state.clear()
        helps = help_by_user_phone(phone)

        if helps is None:
            await roloc_bot.send_message(
                user_id,
                help_noexs_uphone,
                reply_markup=adm_helps_search_kb().as_markup()
            )
        elif not helps:
            await roloc_bot.send_message(
                user_id,
                msg_error,
                reply_markup=adm_helps_search_kb().as_markup()
            )
        elif helps is not None:
            await get_result(message, helps, 'help', roloc_bot)


""" /////////////////// CHANGE OPTIONS //////////////////"""


@helps_router.callback_query(F.data.startswith('admchange#help'))
async def helps_change_menu_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        await state.set_state(HelpChangeState.help_id)
        await callback.message.edit_text(msg_search_helpid)


@helps_router.message(HelpChangeState.help_id)
async def admin_helps_change_status1(message: Message, state: FSMContext):
    ste = await state.get_state()
    if message.from_user.id in ADMIN_IDS and ste == 'HelpChangeState:help_id':
        help_info = help_by_id(message.text)

        if help_info is None:
            await state.set_state(HelpChangeState.help_id)
            await roloc_bot.send_message(
                message.from_user.id,
                msg_noexs_help
            )
            await roloc_bot.send_message(
                message.from_user.id,
                msg_search_helpid
            )
        elif not help_info:
            await state.clear()
            await roloc_bot.send_message(
                message.from_user.id,
                msg_change_failed_stats,
                reply_markup=adm_helps_menu_kb().as_markup()
            )
        elif help_info is not None:
            await state.set_state(HelpChangeState.help_status)
            await state.update_data(help_id=message.text)
            await roloc_bot.send_message(message.from_user.id, help_info)

            await roloc_bot.send_message(
                message.from_user.id,
                msg_helps_select_param,
                reply_markup=adm_helps_change_kb().as_markup()
            )

@helps_router.callback_query(F.data.startswith("helpstatus"), HelpChangeState.help_status)
async def admin_helps_change_status_2(callback: CallbackQuery, state: FSMContext):
    ste = await state.get_state()
    if callback.from_user.id in ADMIN_IDS and ste == 'HelpChangeState:help_status':
        state_data = await state.get_data()
        await state.clear()

        help_id = state_data['help_id']
        status = help_status_dict[callback.data]

        result = update_help_status(help_id, status)

        if result is None:
            return callback.message.edit_text(
                msg_noexs_help,
                reply_markup=adm_helps_menu_kb().as_markup()
            )
        if not result:
            await callback.message.edit_text(
                msg_change_failed_stats,
                reply_markup=adm_helps_menu_kb().as_markup()
            )
        else:
            await callback.message.edit_text(
                msg_help_change_success,
                reply_markup=adm_helps_menu_kb().as_markup()
            )
