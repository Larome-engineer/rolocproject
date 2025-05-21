from aiogram import Bot
from keyboards.admin_kb import adm_appls_search_kb, adm_helps_search_kb
from aiogram.types import Message, CallbackQuery

from keyboards.user_kb import user_menu_kb


async def get_result(message: Message | CallbackQuery, result: str, menu: str, bot: Bot):
    if type(message) is CallbackQuery:
        count = len(result) // 4090

        if len(result) > 4090:
            for it in range(0, len(result), 4090):
                if it // 4090 == count:
                    if menu == 'appls':
                        await bot.send_message(
                            message.from_user.id,
                            result[it:it + 4090],
                            reply_markup=adm_appls_search_kb().as_markup())
                    elif menu == 'help':
                        await bot.send_message(
                            message.from_user.id,
                            result[it:it + 4090],
                            reply_markup=adm_helps_search_kb().as_markup())
                else:
                    await bot.send_message(message.from_user.id, result[it:it + 4090])
        else:
            if menu == 'appls':
                await message.message.edit_text(result, reply_markup=adm_appls_search_kb().as_markup())
            elif menu == 'help':
                await message.message.edit_text(result, reply_markup=adm_helps_search_kb().as_markup())
    else:
        count = len(result) // 4090

        if len(result) > 4090:
            for it in range(0, len(result), 4090):
                if it // 4090 == count:
                    if menu == 'appls':
                        await bot.send_message(
                            message.from_user.id,
                            result[it:it + 4090],
                            reply_markup=adm_appls_search_kb().as_markup())
                    elif menu == 'help':
                        await bot.send_message(
                            message.from_user.id,
                            result[it:it + 4090],
                            reply_markup=adm_helps_search_kb().as_markup())
                else:
                    await bot.send_message(message.from_user.id, result[it:it + 4090])
        else:
            if menu == 'appls':
                await bot.send_message(message.from_user.id, result, reply_markup=adm_appls_search_kb().as_markup())
            elif menu == 'help':
                await bot.send_message(message.from_user.id, result, reply_markup=adm_helps_search_kb().as_markup())


#################### FOR USER #####################
async def get_result_for_user(message: Message | CallbackQuery, result: str, bot: Bot):
    if type(message) is CallbackQuery:
        count = len(result) // 4090

        if len(result) > 4090:
            for it in range(0, len(result), 4090):
                if it // 4090 == count:

                    await bot.send_message(
                        message.from_user.id,
                        result[it:it + 4090],
                        reply_markup=user_menu_kb().as_markup())
                else:
                    await bot.send_message(message.from_user.id, result[it:it + 4090])
        else:
            await message.message.edit_text(result, reply_markup=user_menu_kb().as_markup())
    else:
        count = len(result) // 4090

        if len(result) > 4090:
            for it in range(0, len(result), 4090):
                if it // 4090 == count:
                    await bot.send_message(
                        message.from_user.id,
                        result[it:it + 4090],
                        reply_markup=user_menu_kb().as_markup()
                    )
                else:
                    await bot.send_message(message.from_user.id, result[it:it + 4090])
        else:
            await bot.send_message(message.from_user.id, result, reply_markup=user_menu_kb().as_markup())
