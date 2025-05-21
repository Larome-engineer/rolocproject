from data.messages import *
from aiogram.types import Message
from keyboards.user_kb import user_menu_kb
from roloc_create import roloc_bot, ADMIN_IDS
from aiogram.utils.media_group import MediaGroupBuilder


async def media_processor(msg: Message, caption: str, album: list = None):
    if msg.photo:
        await photo_processor(caption, msg, album)
    else:
        if msg.voice:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_voice(
                    chat_id=admin_id,
                    voice=msg.voice.file_id,
                    caption=caption
                )

        elif msg.document:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_document(
                    chat_id=admin_id,
                    document=msg.document.file_id,
                    caption=caption
                )

        elif msg.video:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_video(
                    chat_id=admin_id,
                    video=msg.video.file_id,
                    caption=caption
                )

        elif msg.video_note:
            for admin_id in ADMIN_IDS:
                await roloc_bot.send_video_note(
                    chat_id=admin_id,
                    video_note=msg.video_note.file_id
                )
                await roloc_bot.send_message(admin_id, caption)

        await roloc_bot.send_message(
            chat_id=msg.from_user.id,
            text=msg_procd, reply_markup=user_menu_kb().as_markup()
        )


async def photo_processor(caption: str, msg: Message, album: list = None):
    try:
        photo_ids = []
        media_group = MediaGroupBuilder(caption=caption)

        for msg in album:
            photo_ids.append(msg.photo[-1].file_id)

        for photo_id in photo_ids:
            try:
                media_group.add_photo(media=photo_id)
            except ValueError:
                await roloc_bot.send_message(msg.from_user.id, msg_faild,
                                             reply_markup=user_menu_kb().as_markup())

        for admin_id in ADMIN_IDS:
            await roloc_bot.send_media_group(
                chat_id=admin_id,
                media=media_group.build(),
            )

        await roloc_bot.send_message(
            chat_id=msg.from_user.id,
            text=msg_procd, reply_markup=user_menu_kb().as_markup())

    except TypeError:
        for admin_id in ADMIN_IDS:
            await roloc_bot.send_photo(
                chat_id=admin_id,
                photo=msg.photo[-1].file_id,
                caption=caption
            )

        await roloc_bot.send_message(
            chat_id=msg.from_user.id,
            text=msg_procd, reply_markup=user_menu_kb().as_markup()
        )
