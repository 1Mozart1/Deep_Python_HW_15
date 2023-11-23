import argparse
import logging
import os
from collections import namedtuple
from datetime import datetime, date

logging.basicConfig(filename="log.log", encoding="utf8", level=logging.INFO)
logger = logging.getLogger("log")

MONTH = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}
WEEKDAYS = {
    'понедельник': 0,
    'вторник': 1,
    'среда': 2,
    'четверг': 3,
    'пятница': 4,
    'суббота': 5,
    'воскресенье': 6
}
DATE = namedtuple("DATE", "day month year")
FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_dir', 'parent', 'full_path'])


def get_date(text):
    num_week, week_day, month = text.split()
    num_week = int(num_week.split("-")[0])
    week_day = WEEKDAYS[week_day]
    count_week = 0
    for day in range(1, 31 + 1):
        d = date(year=datetime.now().year, month=MONTH[month], day=day)
        if d.weekday() == week_day:
            count_week += 1
        if count_week == num_week:
            logger.info(DATE(d.day, d.month, d.year))
            return d


def get_file_info(filepath):
    name = os.path.basename(filepath)
    extension = os.path.splitext(name)[1]
    is_dir = os.path.isdir(filepath)
    parent = os.path.dirname(filepath)

    return FileInfo(name, extension, is_dir, parent, filepath)


def scan_directory(path):
    try:
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                file_info = get_file_info(os.path.join(root, dir))
                logging.info(file_info)

            for file in files:
                file_info = get_file_info(os.path.join(root, file))
                logging.info(file_info)

    except OSError as err:
        print(f"Ошибка доступа к директории: {err}")


parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Text with date')
parser.add_argument('--dir', help='Directory path')
args = parser.parse_args()

if __name__ == "__main__":
    try:
        if args.date:
            date = get_date(args.date)
            print(date)

        if args.dir:
            scan_directory(args.dir)

        date = get_date(input("Введите текст с датой вида 1-й четверг ноября: "))
        print(date)

    except Exception as err:
        logger.exception("Произошла ошибка")
        print(f"Ошибка: {err}")