from ftplib import FTP
import json
import os

file_date = 'ftp_server.json'
path = "folder_save.json"


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
    with open(file, 'r', encoding='utf-8') as ff:
        j = json.load(ff)
    return j


path_normal_fd = path_normal(file_date)
path_normal_pf = path_normal(path)

ftp_setting = read_json_file(path_normal_fd)
path_folder = read_json_file(path_normal_pf)

path_file = path_folder['folder']['path_1']


def run():
    """Вызгрузка файлов на сервер FTP"""
    with FTP(host=ftp_setting['ftp']['host']) as ftp:
        ftp.login(user=ftp_setting['ftp']['user'], passwd=ftp_setting['ftp']['password'])
        ftp.cwd('/1')
        tt = os.listdir(path_file)
        for i in range(len(tt)):
            with open(path_file + '\\' + tt[i], 'rb') as f:
                ftp.storbinary('STOR ' + tt[i], f)

        # data = ftp.retrlines('LIST')
        ftp.quit()


if __name__ == '__main__':
    run()
