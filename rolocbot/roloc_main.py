import asyncio
import logging
import sys

from aiohttp import web
from data.config import LOG_FILE

from handlers.start_handler import start_router
from handlers.user.help_handler import help_router
from handlers.user.about_handler import about_router
from handlers.user.app_from_handler import app_form_router

from handlers.admin.appls_handler import appls_router
from handlers.admin.helps_handler import helps_router
from handlers.admin.adm_main_menu import adm_main_menu_router
from handlers.admin.back_adm_handler import back_adm_router

from roloc_create import dp, roloc_bot, Bot, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

async def on_startup(bot: Bot) -> None: # WEBHOOK
    await bot.set_webhook(WEBHOOK_URL)


def main() -> None:
    dp.include_routers(
        start_router,
        about_router,
        help_router,
        adm_main_menu_router,
        back_adm_router,
        appls_router,
        helps_router,
        app_form_router,
    )

    dp.startup.register(on_startup)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=roloc_bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=roloc_bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='w')
    main()

# async def main() -> None: # POLLING
#     dp.include_routers(
#         start_router,
#         about_router,
#         help_router,
#         adm_main_menu_router,
#         back_adm_router,
#         appls_router,
#         helps_router,
#         app_form_router,
#     )
#
#     await dp.start_polling(roloc_bot)
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='w')
#     asyncio.run(main())
#


