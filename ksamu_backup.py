import os
import json
from ftplib import FTP
from datetime import date


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


setting_folder = "folder_save.json"
setting_server = 'ftp_server.json'

j_sf = read_json_file(setting_folder)
ftp_setting_json = read_json_file(setting_server)


def run():
    """Вызгрузка файлов на сервер FTP"""
    with FTP(host=ftp_setting_json['ftp']['host']) as ftp:
        ftp.login(user=ftp_setting_json['ftp']['user'], passwd=ftp_setting_json['ftp']['password'])
        if ftp_setting_json['ftp']['catalog'] is not None:
            ftp.cwd(ftp_setting_json['ftp']['catalog'])

        path = j_sf['folder']['path']

        files_list = os.listdir(path)
        files = list(map(path_normal, [os.path.join(path, i) for i in files_list]))
        files = [file for file in files if os.path.isfile(file)]
        try:
            file_save = max(files, key=os.path.getmtime)
        except ValueError:
            pass

        pf = os.listdir(path)
        print(path)
        print(file_save)

        try:
            ftp.cwd(j_sf['folder']['catalog'])
        except:
            ftp.mkd(j_sf['folder']['catalog'])
            ftp.cwd(j_sf['folder']['catalog'])

        try:
            ftp.cwd(j_sf['folder']['new_archive_folder'] + "_" + str(date.today()))
        except:
            ftp.mkd(j_sf['folder']['new_archive_folder'] + "_" + str(date.today()))
            ftp.cwd(j_sf['folder']['new_archive_folder'] + "_" + str(date.today()))

        try:
            # print(file_save)
            with open(file_save, 'rb') as f:
                ftp.storbinary('STOR ' + "main.py", f)
        except:
            print('Ошибка')
            pass
        # data = ftp.retrlines('LIST')
        ftp.quit()


if __name__ == '__main__':
    run()
