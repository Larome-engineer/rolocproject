import logging
import datetime

from psycopg2.errors import *
from data.config import LOG_FILE
from psycopg2.pool import SimpleConnectionPool
from roloc_create import DBNAME, HOST, USERNAME, PASSWORD

logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='w')
module_name = 'user_dao'

try:
    pool = SimpleConnectionPool(1, 10, dbname=DBNAME, user=USERNAME, password=PASSWORD, host=HOST)
except OperationalError:
    logging.log(
        level=logging.INFO,
        msg=f"{datetime.datetime.now().ctime()} | Ошибка соединения с базой | {module_name}")


def create_user(user_tg_id: str, user_name: str, user_tg_username: str, user_phone: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""insert into users(user_tg_id, user_name, user_tg_username, user_phone)
            values(%s, %s, %s, %s) returning user_id""", (user_tg_id, user_name, user_tg_username, user_phone))

            conn.commit()
            res = curs.fetchone()

        pool.putconn(conn)
        return res, True

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.DEBUG,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: create_user")
        return False


def get_user_id_by_user_tg_id(tg_id: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""select user_id from Users where user_tg_id = %s""", (tg_id,))
            res = curs.fetchone()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.DEBUG,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_user_id_by_user_tg_id")
        return False


def get_user_data_by_user_tg_id(tg_id: str):
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("""select user_name, user_tg_username, user_phone 
            from Users where user_tg_id = %s""", (tg_id,))

            res = curs.fetchone()

        pool.putconn(conn)
        return res

    except (Error, NameError) as e:
        pool.putconn(conn)
        logging.log(level=logging.DEBUG,
                    msg=f"{datetime.datetime.now().ctime()} | {e} | {module_name}: get_user_data_by_user_tg_id")
        return False
