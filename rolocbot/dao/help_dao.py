import logging
import datetime

from psycopg2.errors import *
from data.config import LOG_FILE
from psycopg2.pool import SimpleConnectionPool
from roloc_create import DBNAME, HOST, USERNAME, PASSWORD

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w')
module_name = 'help_dao'

try:
    pool = SimpleConnectionPool(1, 10, dbname=DBNAME, user=USERNAME, password=PASSWORD, host=HOST)
except OperationalError:
    logging.log(
        level=logging.INFO,
        msg=f"{datetime.datetime.now().ctime()} | Ошибка соединения с базой | {module_name}")


def create_help(help_text: str, help_uid: int):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""insert into helps(help_text, help_uid)
                values(%s, %s)""", (help_text, help_uid))
            conn.commit()

        pool.putconn(conn)
        return True

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_help")
        return False


def get_all_helps():
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select help_id, help_text, help_status, user_phone, user_tg_username from helps 
                left join users on user_id = help_uid;""")
            res = curs.fetchall()
        pool.putconn(conn)
        return res
    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_all_helps")
        return False


def get_help_by_id(help_id: int):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select help_id, help_text, help_status, 
                user_name, user_tg_username, user_phone 
                from helps left join users on user_id = help_uid where help_id = %s;""", (help_id,))
            res = curs.fetchone()
        pool.putconn(conn)
        return res
    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_help_by_id")
        return False


def get_helps_by_status(help_status: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select help_id, help_text, user_name, user_tg_username, user_phone 
                from helps left join users on user_id = help_uid where help_status = %s;""", (help_status,))
            res = curs.fetchall()
        pool.putconn(conn)
        return res
    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_helps_by_status")
        return False

def get_help_by_user_phone(user_phone: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select help_id, help_text, help_status, 
                user_name, user_tg_username, user_phone 
                from helps left join users on user_id = help_uid where user_phone = %s;""", (user_phone,))
            res = curs.fetchall()
        pool.putconn(conn)
        return res
    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_help_by_user_phone")
        return False

def get_helps_by_user_tg_id(tg_id: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute(
                """select help_id, help_status, help_text from helps 
                left join users on user_id = help_uid 
                where user_tg_id = %s;""", (tg_id,))
            res = curs.fetchall()
        pool.putconn(conn)
        return res
    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_helps_by_user_tg_id")
        return False

def change_help_status(help_id: int, new_status: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                update Helps set help_status = %s where help_id = %s;""", (new_status, help_id))
            conn.commit()
            res = True

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.INFO,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: change_help_status")
        return False
