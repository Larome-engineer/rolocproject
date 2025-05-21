import logging
import datetime

from typing import Any
from psycopg2.errors import *
from data.config import LOG_FILE
from psycopg2.pool import SimpleConnectionPool
from roloc_create import DBNAME, HOST, USERNAME, PASSWORD

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w')
module_name = 'app_form_dao'

try:
    pool = SimpleConnectionPool(1, 10, dbname=DBNAME, user=USERNAME, password=PASSWORD, host=HOST)
except OperationalError:
    logging.log(
        level=logging.INFO,
        msg=f"{datetime.datetime.now().ctime()} | Ошибка соединения с базой | {module_name}")


def create_application(app_date: str, app_type: str, app_user_id: int) -> tuple[Any, bool] | bool:
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""insert into applications(app_date, app_type, app_user_id)
                values(%s, %s, %s) returning app_id""", (app_date, app_type, app_user_id))
            conn.commit()
            res = curs.fetchone()

        pool.putconn(conn)
        return res, True

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_application")
        return False


'''-----------------------------GET FUNCTIONS-----------------------------'''


def get_app_info_by_number(number: int) -> tuple | bool:  # get app by NUMBER
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select
                app_type,
                app_date,
                app_status,
                app_price,
                app_comment,
                user_name,
                user_tg_username,
                user_phone from Applications
                right join Users on app_user_id = user_id where app_id=%s;""", (number,))
            res = curs.fetchone()
        pool.putconn(conn)

        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_app_info_by_number")
        return False


def get_all_apps_by_service(service: str) -> list | bool:  # get all apps by SERVICE
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            if service == 'комплекс услуг':
                curs.execute("""
                    select app_id, app_type, app_status, user_name, user_tg_username from Applications 
                    left join Users on app_user_id = user_id where app_type like 'комплекс услуг%';""")
                res = curs.fetchall()
            else:
                curs.execute("""
                    select app_id, app_type, app_status, user_name, user_tg_username from Applications 
                    left join Users on app_user_id = user_id where app_type = %s;""", (service,))
                res = curs.fetchall()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_all_apps_info_by_service")
        return False


def get_all_apps_by_date(date: str) -> list | bool:  # get all apps by DATE
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                select app_id, app_type, app_status, user_name, user_tg_username from Applications 
                left join Users on app_user_id = user_id where app_date = %s;""", (date,))
            res = curs.fetchall()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_all_apps_info_by_date")
        return False


def get_all_apps_by_status(status: str) -> list | bool:  # get all apps by STATUS
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                select app_id, app_type, user_name, user_tg_username from Applications 
                left join Users on app_user_id = user_id where app_status = %s;""", (status,))
            res = curs.fetchall()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | app_form_dao: get_all_apps_info_by_status")
        return False


def get_all_apps_by_usr_phone(usr_phone: str) -> list | bool:  # get all apps by USER_PHONE
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                select app_id, app_type, app_status, user_name, user_tg_username from Applications 
                left join Users on Users.user_id = Applications.app_user_id where user_phone=%s""", (usr_phone,))
            res = curs.fetchall()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_all_apps_info_by_usr_phone")
        return False


def get_apps_by_user_tg_id(tg_id: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""select app_id, app_type, app_date, app_status, user_name, user_phone 
            from applications left join users on user_id = app_user_id where user_tg_id = %s;""", (tg_id,))
            res = curs.fetchall()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_all_apps_info_by_usr_phone")
        return False

'''-----------------------------UPDATE FUNCTIONS-----------------------------'''


def update_app_status(new_status: str, app_id: int) -> bool:  # update app STATUS
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                update Applications set app_status = %s where app_id = %s;""", (new_status, app_id,))
            conn.commit()
            res = True

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_app_status")
        return False


def update_app_comment(app_comment: str, app_id: int) -> bool:  # update app COMMENT
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                update Applications set app_comment = %s where app_id = %s;""", (app_comment, app_id,))
            conn.commit()
            res = True

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_app_comment")
        return False


def update_app_price(app_price: str, app_id: int) -> bool:  # update app PRICE
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                update Applications set app_price = %s where app_id = %s;""", (app_price, app_id,))
            conn.commit()
            res = True

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: update_app_price")
        return False
