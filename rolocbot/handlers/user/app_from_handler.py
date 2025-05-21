from aiogram import Router, F

from data.config import ADV_FILE
from keyboards.user_kb import *

from utils.limitignore import get_result_for_user
from data.messages import complex_options
from aiogram.fsm.context import FSMContext
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.fsm.state import StatesGroup, State
from utils.media_processor import media_processor
from middleware.album_middleware import AlbumMiddleware

from services.user_service import check_on_exists
from services.app_form_service import create_app, app_performer, apps_by_user_tg_id

from aiogram.types import Message, CallbackQuery, ContentType as Ct, PollAnswer, FSInputFile

app_form_router = Router()


class AppFromState(StatesGroup):
    type = State()
    comp = State()

    sides = State()
    pages_size = State()
    banner_size = State()
    need_prod = State()

    username = State()
    user_phn = State()
    user_cnt = State()
    wishes = State()
    brief = State()
    files = State()


@app_form_router.poll_answer(AppFromState.comp)
async def user_app_form_complex(poll_answer: PollAnswer, state: FSMContext):
    now_state = await state.get_state()
    if now_state == "AppFromState:comp":
        options = []
        opt_index = poll_answer.option_ids

        for option in opt_index:
            if option in complex_options:
                options.append(complex_options.get(option))

        await state.update_data(comp=options)

        user = check_on_exists(poll_answer.user.id)
        if user is None or not user:
            await state.set_state(AppFromState.username)
            await roloc_bot.send_message(poll_answer.user.id, msg_uname)

        else:
            await state.update_data(username=user['name'],
                                    user_phn=user['phone'],
                                    user_tg_username=user['tg_username'],
                                    user_tg_id=poll_answer.user.id
                                    )
            await state.set_state(AppFromState.user_cnt)
            await roloc_bot.send_message(poll_answer.user.id, msg_commt)

@app_form_router.callback_query(F.data.startswith('usermenu1'))
async def user_app_form_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await state.set_state(AppFromState.type)
    try:
        await callback.message.edit_text(msg_servs, reply_markup=user_service_kb().as_markup())
    except Exception as e:
        await callback.message.answer(msg_servs, reply_markup=user_service_kb().as_markup())


@app_form_router.callback_query(F.data.startswith('usermenu4'))
async def get_all_user_apps(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    app_forms = apps_by_user_tg_id(callback.from_user.id)
    if app_forms is None:
        await callback.message.edit_text(msg_userappls_noexs, reply_markup=user_menu_kb().as_markup())
    elif not app_forms:
        await callback.message.edit_text(msg_userappls_failed, reply_markup=user_menu_kb().as_markup())
    elif app_forms is not None:
        await get_result_for_user(callback, app_forms, roloc_bot)

@app_form_router.callback_query(F.data.startswith('usermenu6'))
async def adv_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer_document(
        FSInputFile(ADV_FILE, f"{usermenu6}.pdf"), caption=msg_adv, reply_markup=user_adv_button().as_markup()
    )

@app_form_router.callback_query(F.data.startswith('serv_'), AppFromState.type)
async def user_app_form_distribute(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    call = callback.message
    now_state = await state.get_state()

    if call.photo or call.voice or call.document or call.audio or call.video or call.story or call.video_note:
        await call.edit_text(msg_media, reply_markup=user_service_kb().as_markup())
        await state.set_state(AppFromState.type)

    elif now_state == 'AppFromState:type':
        c_data = callback.data.split("_")[1]

        await state.update_data(type=c_match[callback.data])

        if c_data in ["1", "2", "3", "9"]:
            user = check_on_exists(callback.from_user.id)
            if user is None or not user:
                await state.set_state(AppFromState.username)
                await callback.message.edit_text(msg_uname)

            else:
                await state.update_data(username=user['name'],
                                        user_phn=user['phone'],
                                        user_tg_username=user['tg_username'],
                                        user_tg_id=callback.from_user.id
                                        )

                await state.set_state(AppFromState.user_cnt)
                await callback.message.edit_text(msg_commt)

        elif c_data in ["4", "7", "8"]:
            await state.set_state(AppFromState.sides)
            await callback.message.edit_text(msg_numsd, reply_markup=user_sides_kb().as_markup())

        elif c_data == "5":
            await state.set_state(AppFromState.banner_size)
            await callback.message.edit_text(msg_sizze)

        elif c_data == "6":
            await state.set_state(AppFromState.pages_size)
            await callback.message.edit_text(msg_numpg)

        elif c_data == "0":
            await roloc_bot.send_poll(
                chat_id=callback.from_user.id,
                question=msg_quest,
                options=list(complex_options.values()),
                is_anonymous=False,
                allows_multiple_answers=True
            )
            await state.set_state(AppFromState.comp)


@app_form_router.message(AppFromState.banner_size)
async def user_app_form_page_size(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == "AppFromState:banner_size":
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.banner_size)
            await roloc_bot.send_message(msg.from_user.id, msg_sizze)

        else:
            await state.update_data(banner_size=msg.text)
            await state.set_state(AppFromState.need_prod)
            await roloc_bot.send_message(msg.from_user.id, msg_produ, reply_markup=user_production_kb().as_markup())


@app_form_router.message(AppFromState.pages_size)
async def user_app_form_page_size(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == "AppFromState:pages_size":
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.pages_size)
            await roloc_bot.send_message(msg.from_user.id, msg_numpg)

        else:
            await state.update_data(page_size=msg.text)
            await state.set_state(AppFromState.need_prod)
            await roloc_bot.send_message(msg.from_user.id, msg_produ, reply_markup=user_production_kb().as_markup())


@app_form_router.callback_query(F.data.startswith('side_'), AppFromState.sides)
async def user_app_form_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(sides=c_match[callback.data])

    await state.set_state(AppFromState.need_prod)
    await callback.message.edit_text(msg_produ, reply_markup=user_production_kb().as_markup())


@app_form_router.callback_query(F.data.startswith('prod_'), AppFromState.need_prod)
async def user_app_form_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(need_prod=c_match[callback.data])
    user = check_on_exists(callback.from_user.id)
    if user is None or not user:
        await state.set_state(AppFromState.username)
        await callback.message.edit_text(msg_uname)
    else:
        await state.update_data(username=user['name'],
                                user_phn=user['phone'],
                                user_tg_username=user['tg_username'],
                                user_tg_id=callback.from_user.id
                                )

        await state.set_state(AppFromState.user_cnt)
        await callback.message.edit_text(msg_commt)


@app_form_router.message(AppFromState.username)
async def user_app_form_contacts_phone(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == "AppFromState:username":
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.username)
            await roloc_bot.send_message(msg.from_user.id, msg_uname)

        else:
            await state.update_data(username=msg.text)
            await state.set_state(AppFromState.user_phn)
            await roloc_bot.send_message(msg.from_user.id, msg_numbr)


@app_form_router.message(AppFromState.user_phn)
async def user_app_form_contacts_name(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == 'AppFromState:user_phn':
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.user_phn)
            await roloc_bot.send_message(msg.from_user.id, msg_numbr)

        else:
            await state.update_data(user_phn=msg.text)
            await state.set_state(AppFromState.user_cnt)
            await roloc_bot.send_message(msg.from_user.id, msg_commt)


@app_form_router.message(AppFromState.user_cnt)
async def user_app_form_contacts_communicate(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == 'AppFromState:user_cnt':
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.user_cnt)
            await roloc_bot.send_message(msg.from_user.id, msg_commt)

        else:
            await state.update_data(user_cnt=msg.text)
            await state.set_state(AppFromState.wishes)
            await roloc_bot.send_message(msg.from_user.id, msg_wishs)


@app_form_router.message(AppFromState.wishes)
async def user_app_form_wishes(msg: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state == 'AppFromState:wishes':
        if not msg.text:
            await roloc_bot.send_message(msg.from_user.id, msg_media)
            await state.set_state(AppFromState.wishes)
            await roloc_bot.send_message(msg.from_user.id, msg_wishs)

        else:
            await state.update_data(wishes=msg.text)
            check_on_user = await state.get_data()

            if 'user_tg_username' not in check_on_user:
                await state.set_state(AppFromState.brief)
                await roloc_bot.send_message(msg.from_user.id, msg_brief, reply_markup=user_brief_kb().as_markup())

            else:
                await state.set_state(AppFromState.files)
                await roloc_bot.send_message(msg.from_user.id, msg_files, reply_markup=user_complete_kb().as_markup())


@app_form_router.callback_query(F.data.startswith('brief_'), AppFromState.brief)
async def user_app_form_contacts_name(callback: CallbackQuery, state: FSMContext):
    now_state = await state.get_state()
    if now_state == 'AppFromState:brief':
        await state.update_data(brief=c_match[callback.data])

        await state.set_state(AppFromState.files)
        await callback.message.edit_text(msg_files, reply_markup=user_complete_kb().as_markup())


app_form_router.message.middleware(AlbumMiddleware())


@app_form_router.message(AppFromState.files)
@app_form_router.message(F.сontent_type.in_([Ct.PHOTO, Ct.VOICE, Ct.DOCUMENT, Ct.VIDEO_NOTE, Ct.VIDEO]))
async def user_app_form_wishes(msg: Message, state: FSMContext, album: list = None):
    now_state = await state.get_state()
    if now_state == 'AppFromState:files':
        user_data = await state.get_data()

        await state.clear()

        if 'user_tg_username' not in user_data or 'user_tg_id' not in user_data:
            user_data['user_tg_username'] = msg.from_user.username
            user_data['user_tg_id'] = msg.from_user.id

        app_created_info = create_app(user_data)

        if type(app_created_info) is tuple and app_created_info[1]:
            app_id = str(app_created_info[0])
            user_data['id'] = app_id

            await media_processor(msg, app_performer(user_data), album)
        else:
            await media_processor(msg, app_performer(user_data), album)


@app_form_router.callback_query(F.data.contains("finish"), AppFromState.files)
async def none_files_state(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    now_state = await state.get_state()

    if now_state == 'AppFromState:files':
        user_data = await state.get_data()
        await state.clear()

        if 'user_tg_username' not in user_data or 'user_tg_id' not in user_data:
            user_data['user_tg_username'] = callback.from_user.username
            user_data['user_tg_id'] = callback.from_user.id

        app_created_info = create_app(user_data)

        if type(app_created_info) is tuple and app_created_info[1]:
            app_id = str(app_created_info[0])
            user_data['id'] = app_id

            application = app_performer(user_data)

            for admin_id in ADMIN_IDS:
                await roloc_bot.send_message(admin_id, application)
            await callback.message.edit_text(msg_procd, reply_markup=user_menu_kb().as_markup())

        else:
            perform_message = f"{msg_dberr}\n\n{app_performer(user_data)}"
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_message(admin_id, perform_message)
            await callback.message.edit_text(msg_procd, reply_markup=user_menu_kb().as_markup())
