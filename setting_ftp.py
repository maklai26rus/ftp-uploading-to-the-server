import json
import os

setting_server = 'ftp_server.json'
setting_folder = "folder_save.json"
log_txt = "log.txt"


def path_normal(path):
    """Модюль преобразующий в правильный путь """
    _pn = os.path.normpath(os.path.join(path))

    return _pn


def read_json_file(file):
    """
    Читаем json file
    :param file:
    :return: возращает словарь из json
    """
    # на сервере 2012 нормально работает кодировка utf-8 на сервере 2019 пришлось добавить utf-8-sig
    # with open(file, 'r', encoding='utf-8') as ff:
    with open(file, 'r', encoding='utf-8-sig') as ff:
        j = json.load(ff)
    return j


def pn_ss():
    """
    Нормализованый путь к файлу setting_server
    """
    return path_normal(setting_server)


def pn_sf():
    """
    Нормализованый путь к файлу setting_folder
    """
    return path_normal(setting_folder)


def ftp_setting_json() -> json:
    """Возращает json  c настройками setting_server"""
    return read_json_file(pn_ss())


def folder_json() -> json:
    """Возращает json  c настройками setting_folder"""
    return read_json_file(pn_sf())
