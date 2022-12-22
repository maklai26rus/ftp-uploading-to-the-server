from ftplib import FTP
import json
import os
from datetime import date

setting_server = 'ftp_server.json'
setting_folder = "folder_save.json"


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


pn_ss = path_normal(setting_server)
pn_sf = path_normal(setting_folder)

ftp_setting_json = read_json_file(pn_ss)
folder_json = read_json_file(pn_sf)

path_file = folder_json['folder']['path']


def run():
    """Вызгрузка файлов на сервер FTP"""
    with FTP(host=ftp_setting_json['ftp']['host']) as ftp:
        ftp.login(user=ftp_setting_json['ftp']['user'], passwd=ftp_setting_json['ftp']['password'])
        if ftp_setting_json['ftp']['catalog'] is not None:
            ftp.cwd(ftp_setting_json['ftp']['catalog'])

        pf = os.listdir(path_file)

        try:
            ftp.cwd(folder_json['folder']['catalog'])
        except:
            ftp.mkd(folder_json['folder']['catalog'])
            ftp.cwd(folder_json['folder']['catalog'])

        try:
            ftp.cwd(folder_json['folder']['new_archive_folder'] + "_" + str(date.today()))
        except:
            ftp.mkd(folder_json['folder']['new_archive_folder'] + "_" + str(date.today()))
            ftp.cwd(folder_json['folder']['new_archive_folder'] + "_" + str(date.today()))

        for i in range(len(pf)):

            try:
                with open(path_file + '\\' + pf[i], 'rb') as f:
                    ftp.storbinary('STOR ' + pf[i], f)
            except PermissionError:
                ftp.mkd(pf[i])

        # data = ftp.retrlines('LIST')
        ftp.quit()


if __name__ == '__main__':
    run()
