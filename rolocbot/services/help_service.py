from data.config import LOG_FILE
from dao.help_dao import *
from utils.check_status import *
from services.user_service import *

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w+')
module_name = 'help_service'

'''-----------------------------CREATE FUNCTIONS-----------------------------'''


def create_help_service(data: dict):
    try:
        tg_id = data['user_tg_id']
        user_id = id_by_tg_id_service(tg_id)
        if user_id is None:
            user_id = create_user_service(tg_id, data['name'], data['username'], data['contacts'])
            create_help(data['helptext'], user_id)

        elif user_id is not None:
            create_help(data['helptext'], user_id)

        user = check_on_exists(tg_id)
        return True, user

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_help_service")
        return False


'''----------------------------- GET FUNCTIONS ------------------------------'''


def all_helps():
    try:
        helps = get_all_helps()
        if not helps and type(helps) is list:
            return None
        elif not helps:
            return False
        else:
            result_list = []
            for i in helps:
                if i[4] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[4]}'
                result_list.append(
                    [f"🆔 • {i[0]}",
                     f"♻️ • {convert_help_to_value(i[2])}",
                     f"💻 • {tg_username}",
                     f"👨‍💻 • {i[3]}",
                     f"✏️ • {i[1]}"
                    ]
                )
            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3] + '\n' + i[4]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: all_helps")
        return False

def help_by_id(help_id: str):
    try:
        help_id = int(help_id)
        help_info = get_help_by_id(help_id)
        if help_info is None:
            return None

        elif not help_info:
            return False

        else:
            info_dict = [{
                '🆔': f'<strong>{help_info[0]}</strong>',
                '♻️': convert_help_to_value(help_info[2]),
                '👨‍💻': help_info[3].capitalize(),
                '💻': help_info[4],
                '📞': f"<code>{help_info[5]}</code>",
                '✏️': help_info[1],

            }]
            result = '\n'.join([f'{key} • {value}' if value is not None else f'{key} • -'
                                for key, value in info_dict[0].items()])
            return result
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: help_by_id")
        return False


def helps_by_status(help_status: str):
    try:
        help_info = get_helps_by_status(convert_help_to_name(help_status))
        if not help_info and type(help_info) is list:
            return None

        elif not help_info:
            return False
        else:
            result_list = []
            for i in help_info:
                if i[3] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[3]}'

                result_list.append([f"🆔 • {i[0]}",
                                    f"👨‍💻 • {i[2].capitalize()} (<code>{i[4]}</code>)",
                                    f"💻 • {tg_username}",
                                    f"✏️ • {i[1]}"
                                    ]
                                   )
            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: helps_by_status")
        return False


def help_by_user_phone(user_phone: str):
    try:
        help_info = get_help_by_user_phone(user_phone)
        if not help_info and type(help_info) is list:
            return None

        elif not help_info:
            return False
        else:
            result_list = []
            for i in help_info:
                if i[4] is None:
                    tg_username = 'Скрыт'
                else:
                    tg_username = f'@{i[4]}'

                result_list.append(
                    [f"🆔 • {i[0]}",
                     f"♻️ • {convert_help_to_value(i[2])}",
                     f"👨‍💻 • {i[3].capitalize()} (<code>{i[5]}</code>)",
                     f"💻 • {tg_username}",
                     f"✏️ • {i[1]}"
                     ]
                )

            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2] + '\n' + i[3] + '\n' + i[4]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: help_by_user_phone")
        return False

def helps_by_tg_id(tg_id: int):
    try:
        help_info = get_helps_by_user_tg_id(str(tg_id))
        if not help_info and type(help_info) is list:
            return None

        elif not help_info:
            return False
        else:
            result_list = []
            for i in help_info:
                result_list.append(
                    [f"🆔 • {i[0]}",
                     f"♻️ • {convert_help_to_value(i[1])}",
                     f"✏️ • {i[2]}"
                     ]
                )

            info = ''
            for i in result_list:
                info += i[0] + '\n' + i[1] + '\n' + i[2]
                if len(result_list) > 1:
                    info += '\n\n'

            return info.strip()
    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: helps_by_tg_id")
        return False

'''-----------------------------UPDATE FUNCTIONS-----------------------------'''


def update_help_status(help_id: str, new_status: str):
    try:
        help_id = int(help_id)
        help_info = get_help_by_id(help_id)
        if help_info is None:
            return None

        elif not help_info:
            return False

        else:
            if change_help_status(help_id, convert_help_to_name(new_status)):
                return True
            else:
                return False

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_help_status")
        return False
