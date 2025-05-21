from aiogram import Router, F
from keyboards.admin_kb import *

from roloc_create import ADMIN_IDS
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.user_kb import user_menu_kb


adm_main_menu_router = Router()

@adm_main_menu_router.callback_query(F.data.startswith("mainmenuadm"))
async def admin_main_menu(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_IDS:
        await state.clear()
        await callback.answer()
        call_data = callback.data.split("#")[1]
        if call_data == 'appls':
            await callback.message.edit_text(msg_apps_menu, reply_markup=adm_appls_menu_kb().as_markup())
        elif call_data == 'helps':
            await callback.message.edit_text(msg_help_menu, reply_markup=adm_helps_menu_kb().as_markup())
        elif call_data == 'switch_user':
            await callback.message.edit_text(msg_umenu, reply_markup=user_menu_kb().as_markup())
