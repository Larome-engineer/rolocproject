from aiogram import Router, F

from keyboards.admin_kb import *
from services.app_form_service import *
from utils.limitignore import get_result
from aiogram.fsm.context import FSMContext
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

appls_router = Router()


class AdminDataApplsSearch(StatesGroup):
    appls_search_id = State()
    appls_search_date = State()
    appls_search_phone = State()


class AdminDataApplsForChange(StatesGroup):
    appls_change_id_prce = State()
    appls_change_id_comm = State()
    appls_change_id_stus = State()

    appls_change_price = State()
    appls_change_comment = State()
    appls_change_status = State()


""" /////////////////// SEARCH OPTIONS //////////////////"""


@appls_router.callback_query(F.data.startswith('admsearch#appls'))
async def appls_search_menu_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(msg_search_option, reply_markup=adm_appls_search_kb().as_markup())


@appls_router.callback_query(F.data.startswith('search'))
async def appls_search_options_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        call_data = callback.data.split('_')[1]
        await callback.answer()
        if call_data == 'id':
            await state.set_state(AdminDataApplsSearch.appls_search_id)
            await callback.message.edit_text(msg_search_number)

        elif call_data == 'sr':
            await callback.message.edit_text(
                msg_search_srvice,
                reply_markup=adm_check_service_kb().as_markup()
            )

        elif call_data == 'dt':
            await state.set_state(AdminDataApplsSearch.appls_search_date)
            await callback.message.edit_text(msg_search_chdate)

        elif call_data == 'st':
            await callback.message.edit_text(
                msg_search_status,
                reply_markup=adm_check_appls_status_kb().as_markup()
            )

        elif call_data == 'pn':
            await state.set_state(AdminDataApplsSearch.appls_search_phone)
            await callback.message.edit_text(msg_search_uphone)


@appls_router.callback_query(F.data.startswith('appstatus'))
async def search_by_status_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()

        status = app_status_dict[callback.data]
        result = all_apps_by_status(status)

        if result is None:
            await callback.message.edit_text(
                msg_noexs_status,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        elif not result:
            await callback.message.edit_text(
                msg_error,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        else:
            await get_result(callback, result, 'appls', roloc_bot)


@appls_router.callback_query(F.data.startswith('service'))
async def search_by_service_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()

        data = callback.data
        service = c_match[f"{data[0:4:1]}_{data[-1]}"]
        result = all_apps_by_service(service)

        if result is None:
            await callback.message.edit_text(
                msg_noexs_srvice,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        elif not result:
            await callback.message.edit_text(
                msg_error,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        else:
            await get_result(callback, result, 'appls', roloc_bot)


@appls_router.message(AdminDataApplsSearch.appls_search_id)
async def search_by_id_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsSearch:appls_search_id':
        await state.clear()
        admin_id = msg.from_user.id
        result = app_info_by_number(msg.text)

        if result is None:
            await roloc_bot.send_message(
                admin_id,
                msg_noexs_number,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        elif not result:
            await roloc_bot.send_message(
                admin_id,
                msg_error,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        else:
            await get_result(msg, result, 'appls', roloc_bot)


@appls_router.message(AdminDataApplsSearch.appls_search_date)
async def search_by_app_date_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsSearch:appls_search_date':
        await state.clear()
        admin_id = msg.from_user.id
        result = all_apps_by_date(msg.text)

        if result is None:
            await roloc_bot.send_message(
                admin_id,
                msg_noexs_sldate,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        elif not result:
            await roloc_bot.send_message(
                admin_id,
                msg_error,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        else:
            await get_result(msg, result, 'appls', roloc_bot)


@appls_router.message(AdminDataApplsSearch.appls_search_phone)
async def search_by_app_usr_phone_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsSearch:appls_search_phone':
        await state.clear()
        admin_id = msg.from_user.id
        result = all_apps_by_usr_phone(msg.text)

        if result is None:
            await roloc_bot.send_message(
                admin_id,
                msg_noexs_uphone,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        elif not result:
            await roloc_bot.send_message(
                admin_id,
                msg_error,
                reply_markup=adm_appls_search_kb().as_markup()
            )

        else:
            await get_result(msg, result, 'appls', roloc_bot)


""" /////////////////// CHANGE OPTIONS //////////////////"""


@appls_router.callback_query(F.data.startswith('admchange#appls'))
async def appls_change_menu_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(
            msg_change_param,
            reply_markup=adm_appls_change_kb().as_markup()
        )


@appls_router.callback_query(F.data.startswith('change'))
async def admin_change_options_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        call_data = callback.data.split('_')[1]
        await callback.answer()
        if call_data == 'stus':
            await state.set_state(AdminDataApplsForChange.appls_change_id_stus)
            await callback.message.edit_text(msg_search_number)

        elif call_data == 'prce':
            await state.set_state(AdminDataApplsForChange.appls_change_id_prce)
            await callback.message.edit_text(msg_search_number)

        elif call_data == 'comm':
            await state.set_state(AdminDataApplsForChange.appls_change_id_comm)
            await callback.message.edit_text(msg_search_number)


''' CHANGE STATUS '''

@appls_router.message(AdminDataApplsForChange.appls_change_id_stus)
async def change_status1_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsForChange:appls_change_id_stus':
        app = app_info_by_number(msg.text)
        if app is None:
            await state.set_state(AdminDataApplsForChange.appls_change_id_stus)
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_noexs_number
            )
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_search_number
            )
        elif not app:
            await state.clear()
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_change_failed_stats,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        else:
            await state.update_data(app_status_id=msg.text)
            await state.set_state(AdminDataApplsForChange.appls_change_status)
            await roloc_bot.send_message(
                msg.from_user.id,
                f"{app}\n\n{msg_search_status}",
                reply_markup=adm_change_appls_status_kb().as_markup()
            )


@appls_router.callback_query(F.data.startswith('ch'), AdminDataApplsForChange.appls_change_status)
async def change_status2_handler(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        state_data = await state.get_data()
        await state.clear()
        await callback.answer()

        app_id = state_data['app_status_id']
        status = app_status_dict[callback.data.split('#')[1]]

        result = update_status(status, app_id)

        if result is None:
            return callback.message.edit_text(
                msg_noexs_number,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        if not result:
            await callback.message.edit_text(
                msg_change_failed_stats,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        else:
            await callback.message.edit_text(
                msg_change_success_stats,
                reply_markup=adm_appls_change_kb().as_markup()
            )


''' CHANGE PRICE '''
@appls_router.message(AdminDataApplsForChange.appls_change_id_prce)
async def change_price1_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsForChange:appls_change_id_prce':
        app = app_info_by_number(msg.text)
        if app is None:
            await state.set_state(AdminDataApplsForChange.appls_change_id_prce)
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_noexs_number
            )
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_search_number
            )
        elif not app:
            await state.clear()
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_change_failed_stats,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        else:
            await state.update_data(app_price_id=msg.text)
            await state.set_state(AdminDataApplsForChange.appls_change_price)
            await roloc_bot.send_message(msg.from_user.id, f"{app}\n\n{msg_change_price}")


@appls_router.message(AdminDataApplsForChange.appls_change_price)
async def change_price2_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsForChange:appls_change_price':
        await state.update_data(price=msg.text)
        state_data = await state.get_data()
        await state.clear()

        admin_id = msg.from_user.id
        result = update_price(state_data['price'], state_data['app_price_id'])
        if result is None:
            await roloc_bot.send_message(
                admin_id,
                msg_noexs_number,
                reply_markup=adm_appls_change_kb().as_markup()
            )

        elif not result:
            await roloc_bot.send_message(
                admin_id,
                msg_change_failed_price,
                reply_markup=adm_appls_change_kb().as_markup()
            )

        else:
            await roloc_bot.send_message(
                admin_id,
                msg_change_success_price,
                reply_markup=adm_appls_change_kb().as_markup()
            )

''' CHANGE COMMENT '''
@appls_router.message(AdminDataApplsForChange.appls_change_id_comm)
async def change_comm1_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsForChange:appls_change_id_comm':
        app = app_info_by_number(msg.text)
        if app is None:
            await state.set_state(AdminDataApplsForChange.appls_change_id_comm)
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_noexs_number
            )
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_search_number
            )
        elif not app:
            await state.clear()
            await roloc_bot.send_message(
                msg.from_user.id,
                msg_change_failed_stats,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        else:
            await state.update_data(app_comment_id=msg.text)
            await state.set_state(AdminDataApplsForChange.appls_change_comment)
            await roloc_bot.send_message(msg.from_user.id, f"{app}\n\n{msg_change_commt}")


@appls_router.message(AdminDataApplsForChange.appls_change_comment)
async def change_comm2_handler(msg: Message, state: FSMContext):
    ste = await state.get_state()
    if msg.from_user.id in ADMIN_IDS and ste == 'AdminDataApplsForChange:appls_change_comment':
        await state.update_data(comment=msg.text)
        state_data = await state.get_data()
        await state.clear()

        admin_id = msg.from_user.id
        result = update_comment(state_data['comment'], state_data['app_comment_id'])
        if result is None:
            await roloc_bot.send_message(
                admin_id,
                msg_noexs_number,
                reply_markup=adm_appls_change_kb().as_markup()
            )

        if not result:
            await roloc_bot.send_message(
                admin_id,
                msg_change_failed_commt,
                reply_markup=adm_appls_change_kb().as_markup()
            )
        else:
            await roloc_bot.send_message(
                admin_id,
                msg_change_success_commt,
                reply_markup=adm_appls_change_kb().as_markup()
            )
