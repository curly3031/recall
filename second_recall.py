from mysql.connector import connect, Error
from datetime import datetime


def second_recall():
    try:
        with connect(
                host="127.0.0.1",
                user="asteruser",
                password="12345678",
                database="asteriskcdrdb",
        ) as connection:
            time = datetime.today().date()
            with connection.cursor() as cursor:
                query = f"SELECT calldate, clid, src, dst, disposition, uniqueid, processed, is_second, is_third FROM " \
                        f"cdr WHERE LENGTH(src) <= 4 and disposition !='ANSWERED' and processed=0 and is_second=0 and calldate LIKE " \
                        f"'%{time}%' ORDER BY calldate DESC LIMIT 1 "
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    uniqueid = row[5][:-6]
                    orig_uniqueid = row[5]
                    dst = row[3]
                    # date = row[0]
                    # print(row, time, uniqueid)
                    if uniqueid:
                        update_query = f"UPDATE cdr set processed=1 WHERE uniqueid LIKE'%{orig_uniqueid}%' "
                        cursor.execute(update_query)
                        connection.commit()
                        print('update successful')
                with open('log_first_recall.txt', mode='a', encoding='utf-8') as f:
                    f.write(f"'selected' {dst} - {datetime.now()}\n")
            return dst

    except Error as e:
        with open('log_first_recall.txt', mode='a', encoding='utf-8') as f:
            f.write(f"{e} - {datetime.now()}\n")
