from data.config import LOG_FILE
from dao.app_form_dao import *
from utils.check_status import *
from services.user_service import *

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w+')
module_name = 'app_form_service'

'''-----------------------------CREATE FUNCTIONS-----------------------------'''


def app_performer(data: dict) -> str:
    try:
        app_id = data['id']
    except KeyError:
        app_id = 'БЕЗ НОМЕРА'

    main_info = [f"📄 <strong>ЗАЯВКА</strong>: {app_id}\n"
                 f"| Тип заявки: {data['type']}\n"
                 f"| Пожелания: {data['wishes']}"]

    tg_username = data['user_tg_username']
    if tg_username is None:
        tg_username = 'Скрыт'

    user_info = [f"👨‍💻 <strong>ЗАКАЗЧИК</strong>\n"
                 f"| Имя: {data['username']}\n"
                 f"| Телефон: {data['user_phn']} ({data['user_cnt']})\n"
                 f"| Telegram: {tg_username} (ID: {data['user_tg_id']})"]

    def perform_additional():
        add_info = ''
        matcher = {
            'brief': 'Откуда узнали',
            'sides': 'Стороны печати',
            'need_prod': 'Изготовление',
            'page_size': 'Кол-во страниц',
            'banner_size': 'Размер баннера'
        }

        for i in data:
            if i in ['need_prod', 'page_size', 'sides', 'brief', 'banner_size']:
                add_info = add_info + f'| {matcher[i]}: {data[i]}\n'

        return add_info.strip()

    if len(data) > 8 and 'Комплекс' not in main_info[0]:
        return f'{main_info[0]}\n\n{user_info[0]}\n\n📝 <strong>ДОПОЛНИТЕЛЬНО</strong>\n{perform_additional()}'

    else:
        res = f'{main_info[0]}\n\n{user_info[0]}'
        if 'brief' in data:
            res = res + f"\n\n📝 <strong>ДОПОЛНИТЕЛЬНО</strong>\n| Откуда узнали: {data['brief']}"

        return res


def create_app(data: dict) -> None | bool | str | tuple:
    try:
        tg_id = data['user_tg_id']
        user_id = id_by_tg_id_service(tg_id)

        if user_id is None:
            if data['user_tg_username'] is None:
                tg_username = None
            else:
                tg_username = data['user_tg_username'].lower()

            user_id = create_user_service(
                tg_id,
                data['username'].lower(),
                tg_username,
                data['user_phn']
            )
        if 'comp' in data:
            comp = ', '.join(data['comp'])
            data['type'] = f"{data['type']}: {comp}"

        create = create_application(datetime.datetime.now().strftime("%Y-%m-%d"), data['type'].lower(), user_id)

        if create[1]:
            return create[0][0], True
        else:
            return None

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_app")
        return False


'''-----------------------------GET FUNCTIONS-----------------------------'''


def app_info_by_number(number: str) -> None | bool | str:  # get app by NUMBER
    try:
        number = int(number)
        app_info = get_app_info_by_number(number)
        if app_info is None:
            return None

        elif not app_info:
            return False

        else:
            info_dict = [{
                '<strong>ТИП ЗАЯВКИ</strong>': f'{app_info[0].capitalize()}\n',
                '📆': f"<code>{app_info[1]}</code>",
                '♻️': convert_to_enum_value(app_info[2]),
                '💵': app_info[3],
                '💬': app_info[4],
                '\n👨‍💻': app_info[5].capitalize(),
                '💻': app_info[6],
                '📞': f"<code>{app_info[7]}</code>",
            }]
            result = '\n'.join([f'{key} • {value}' if value is not None else f'{key} • -'
                                for key, value in info_dict[0].items()])
            return result
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: app_info_by_number")
        return False


def all_apps_by_service(service: str) -> None | bool | str:  # get all apps by SERVICE
    try:
        app_info = get_all_apps_by_service(service.lower())
        if not app_info and type(app_info) is list:
            return None

        elif not app_info:
            return False

        else:
            result_list = []
            for i in app_info:
                if i[4] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[4]}'
                result_list.append(
                    [f"🆔 • {i[0]} ({i[1].capitalize()})",
                     f"♻️ • {convert_to_enum_value(i[2])}",
                     f"👨‍💻 • {i[3].capitalize()}",
                     f"💻 • {tg_username}"]
                )
            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: all_apps_by_service")
        return False


def all_apps_by_date(app_date: str) -> None | bool | str:  # get all apps by DATE
    try:
        app_info = get_all_apps_by_date(app_date)
        if not app_info and type(app_info) is list:
            return None

        elif not app_info:
            return False
        else:
            result_list = []
            for i in app_info:
                if i[4] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[4]}'

                result_list.append(
                    [f"🆔 • {i[0]} ({i[1].capitalize()})",
                     f"♻️ • {convert_to_enum_value(i[2])}",
                     f"👨‍💻 • {i[3].capitalize()}",
                     f"💻 • {tg_username}"]
                )
            info = ''

            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: all_apps_by_date")
        return False


def all_apps_by_status(status: str) -> None | bool | str:  # get all apps by STATUS
    try:
        app_info = get_all_apps_by_status(convert_to_enum_name(status))
        if not app_info and type(app_info) is list:
            return None

        elif not app_info:
            return False
        else:
            result_list = []
            for i in app_info:
                if i[3] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[3]}'

                result_list.append([f"🆔 • {i[0]} ({i[1].capitalize()})",
                                    f"👨‍💻 • {i[2].capitalize()}",
                                    f"💻 • {tg_username}"]
                                   )
            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: all_apps_by_status")
        return False

def all_apps_by_usr_phone(usr_phone: str) -> None | bool | str:  # get all apps by USER_PHONE
    try:
        app_info = get_all_apps_by_usr_phone(usr_phone)
        if not app_info and type(app_info) is list:
            return None

        elif not app_info:
            return False
        else:
            result_list = []
            for i in app_info:
                if i[4] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[4]}'

                result_list.append(
                    [f"🆔 • {i[0]} ({i[1].capitalize()})",
                     f"♻️ • {convert_to_enum_value(i[2])}",
                     f"👨‍💻 • {i[3].capitalize()}",
                     f"💻 • {tg_username}"]
                )

            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: all_apps_by_usr_phone")
        return False


def apps_by_user_tg_id(tg_id: int):
    try:
        app_info = get_apps_by_user_tg_id(str(tg_id))
        if not app_info and type(app_info) is list:
            return None

        elif not app_info:
            return False
        else:
            result_list = []
            for i in app_info:
                result_list.append(
                    [f"🆔 • {i[0]} ({i[1].capitalize()})",
                     f"📆 • {i[2]}",
                     f"♻️ • {convert_to_enum_value(i[3])}",
                     f"👨‍💻 • {i[4].capitalize()}",
                     f"📞 • <code>{i[5]}</code>"]
                )

            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3] + '\n' + i[4]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: app_info_by_user_tg_id ")
        return False

'''-----------------------------UPDATE FUNCTIONS-----------------------------'''


def update_status(new_status: str, app_id: str) -> None | bool:  # update app STATUS
    try:
        app_id = int(app_id)
        app_info = get_app_info_by_number(app_id)
        if app_info is None:
            return None

        elif not app_info:
            return False

        else:
            if update_app_status(convert_to_enum_name(new_status), app_id):
                return True
            else:
                return False

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_status")
        return False


def update_comment(app_comment: str, app_id: str) -> None | bool:  # update app COMMENT
    try:
        app_id = int(app_id)
        app_info = get_app_info_by_number(app_id)
        if app_info is None:
            return None

        elif not app_info:
            return False

        else:
            if update_app_comment(app_comment, app_id):
                return True
            else:
                return False

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_comment")
        return False


def update_price(app_price: str, app_id: str) -> None | bool:  # update app PRICE
    try:
        app_id = int(app_id)
        app_info = get_app_info_by_number(app_id)
        if app_info is None:
            return None

        elif not app_info:
            return False

        else:
            if update_app_price(app_price, app_id):
                return True
            else:
                return False

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_price")
        return False
