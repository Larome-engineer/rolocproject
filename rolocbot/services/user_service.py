from dao.user_dao import *
from data.config import LOG_FILE

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w+')

module_name = 'user_service'


def create_user_service(tg_id: int, username: str, tg_username: str, phone: str):
    try:
        created = create_user(str(tg_id), username, tg_username, phone)
        if created[1]:  # if created True: return user_id
            return created[0]
        else:
            return False

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_user_service")


def id_by_tg_id_service(tg_id: int):
    try:
        user_id = get_user_id_by_user_tg_id(str(tg_id))
        if user_id is not None:
            return user_id[0]
        else:
            return None

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: id_by_tg_id_service")


def check_on_exists(tg_id: int):
    try:
        user_data = get_user_data_by_user_tg_id(str(tg_id))
        if user_data is None or not user_data:
            return None
        else:
            return {
                'name': user_data[0],
                'tg_username': user_data[1],
                'phone': user_data[2]
            }

    except Exception as e:
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: check_on_exists")
        return False
