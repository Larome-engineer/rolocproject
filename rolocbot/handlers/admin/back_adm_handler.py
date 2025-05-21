from aiogram import Router, F
from keyboards.admin_kb import *
from aiogram.fsm.context import FSMContext
from roloc_create import ADMIN_IDS
from aiogram.types import CallbackQuery

back_adm_router = Router()

@back_adm_router.callback_query(F.data.startswith("backto"))
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        option = callback.data.split("#")[1]
        if option == 'adminmainmenu':
            await callback.message.edit_text(msg_main_menu, reply_markup=adm_main_menu_kb().as_markup())
        elif option == 'applmenu':
            await callback.message.edit_text(msg_apps_menu, reply_markup=adm_appls_menu_kb().as_markup())
        elif option == 'helpmenu':
            await callback.message.edit_text(msg_help_menu, reply_markup=adm_helps_menu_kb().as_markup())
