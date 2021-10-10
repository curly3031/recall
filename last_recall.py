from mysql.connector import connect, Error
from datetime import datetime


def last_recall():
    try:
        with connect(
                host="127.0.0.1",
                user="asteruser",
                password="12345678",
                database="asteriskcdrdb",
        ) as connection:
            time = datetime.today().date()
            with connection.cursor() as cursor:
                query = f"SELECT calldate, clid, src, dst, disposition, uniqueid, processed, is_second, is_third FROM "\
                        f"`cdr` WHERE is_second=1 and is_third=0 and processed=1 and disposition !='ANSWERED' and LENGTH(src) <= 4 "\
                        f"and calldate LIKE '%{time}%' ORDER BY calldate DESC LIMIT 1 "
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    dst = row[3]
                with open('log_last_recall.txt', mode='a', encoding='utf-8') as f:
                    f.write(f"'selected' {dst} - {datetime.now()}\n")
            return dst

    except Error as e:
        with open('log_last_recall.txt', mode='a', encoding='utf-8') as f:
            f.write(f"{e} - {datetime.now()}\n")

