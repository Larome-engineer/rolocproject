from data.messages import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def user_menu_kb():
    return (InlineKeyboardBuilder()
            .row(InlineKeyboardButton(text=usermenu1, callback_data='usermenu1'), width=1)
            .row(InlineKeyboardButton(text=usermenu3, callback_data='usermenu3'), width=1)
            .row(InlineKeyboardButton(text=usermenu6, callback_data='usermenu6'), width=1)
            .row(
        InlineKeyboardButton(text=usermenu4, callback_data='usermenu4'),
                 InlineKeyboardButton(text=usermenu5, callback_data='usermenu5'), width=2)
            .row(InlineKeyboardButton(text=usermenu2, callback_data='usermenu2'), width=1)
            .row(InlineKeyboardButton(text=usermenu7, callback_data='link_otziv', url=link_otziv), width=1)
            )

def user_adv_button():
    return (InlineKeyboardBuilder()
            .row(InlineKeyboardButton(text=usermenu1, callback_data='usermenu1'), width=1)
            )

# InlineKeyboardButton(text=menu_w, web_app=WebAppInfo(url=link_wa))

def user_service_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=serv_1, callback_data='serv_1'),
        InlineKeyboardButton(text=serv_2, callback_data='serv_2'),
        InlineKeyboardButton(text=serv_3, callback_data='serv_3'),
        InlineKeyboardButton(text=serv_4, callback_data='serv_4'),
        InlineKeyboardButton(text=serv_5, callback_data='serv_5'),
        InlineKeyboardButton(text=serv_6, callback_data='serv_6'),
        InlineKeyboardButton(text=serv_7, callback_data='serv_7'),
        InlineKeyboardButton(text=serv_8, callback_data='serv_8'),
        InlineKeyboardButton(text=serv_9, callback_data='serv_9'),
        InlineKeyboardButton(text=serv_10, callback_data='serv_0'),
        width=1
    )


# Special questions START
def user_sides_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=oneside, callback_data='side_1'),
        InlineKeyboardButton(text=twoside, callback_data='side_2'),
        width=1
    )


def user_production_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=yes, callback_data='prod_yes'),
        InlineKeyboardButton(text=no, callback_data='prod_no'),
        width=1
    )


# Special questions END


def user_price_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=price_1, callback_data='price_1'),
        InlineKeyboardButton(text=price_2, callback_data='price_2'),
        InlineKeyboardButton(text=price_3, callback_data='price_3'),
        width=1
    )


def user_speed_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=speed_1, callback_data='speed_1'),
        InlineKeyboardButton(text=speed_2, callback_data='speed_2'),
        InlineKeyboardButton(text=speed_3, callback_data='speed_3'),
        width=1
    )


def user_complete_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=finish, callback_data="finish"),
        width=1
    )


def user_approve_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=approve, callback_data="approve"),
        width=1
    )


def user_brief_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text=brief_1, callback_data="brief_1"),
        InlineKeyboardButton(text=brief_2, callback_data="brief_2"),
        InlineKeyboardButton(text=brief_3, callback_data="brief_3"),
        InlineKeyboardButton(text=brief_4, callback_data="brief_4"),
        width=1
    )


def user_about_us_kb():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="VK", callback_data='link_vk', url=link_vk),
        InlineKeyboardButton(text='Telegram', callback_data='link_telegram', url=link_tg),
        InlineKeyboardButton(text='Сайт', callback_data='link_site', url=link_st),
        InlineKeyboardButton(text=back, callback_data='back'),
        width=1
    )
