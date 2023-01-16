from ftplib import FTP
# import json
import os
from datetime import date
import shutil

from setting_ftp import log_txt, ftp_setting_json, folder_json, path_normal

fs = folder_json()
fsj = ftp_setting_json()
path_file = fs['folder']['path']
path_end = path_normal(fs['folder']['path_end'])


def run():
    """Вызгрузка файлов на сервер FTP
    Сначала открывает фтп сервер. потом проверяет есть ли там папки
    Да/нет Созадть /Нет
    Архивирует файл на сервере в указаную папку
    path_end


    """
    with FTP(host=fsj['ftp']['host']) as ftp:
        ftp.login(user=fsj['ftp']['user'], passwd=fsj['ftp']['password'])
        if fsj['ftp']['catalog'] is not None:
            try:
                ftp.cwd(fsj['ftp']['catalog'])
            except:
                ftp.mkd(fsj['ftp']['catalog'])
                ftp.cwd(fsj['ftp']['catalog'])

        # pf = os.listdir(path_file)
        pp = path_normal(path_end + '\\' + 'Arhiv')

        try:
            ftp.cwd(fs['folder']['catalog'])
        except:
            ftp.mkd(fs['folder']['catalog'])
            ftp.cwd(fs['folder']['catalog'])

        try:
            ftp.cwd(fs['folder']['new_archive_folder'])
        except:
            ftp.mkd(fs['folder']['new_archive_folder'])
            ftp.cwd(fs['folder']['new_archive_folder'])

        shutil.make_archive(pp, 'zip', path_file)
        pe = os.listdir(path_end)

        with open(path_end + '\\' + pe[0], 'rb') as f:
            ftp.storbinary('STOR ' + pe[0], f)

        with open(log_txt, 'a', encoding='utf-8') as f:
            f.write(f"Копирование {str(pp)} сделано в {str(date.today())} \n")

        # Нужна если цель копировать все файлы без архива
        # for i in range(len(pf)):
        #
        #     try:
        #         with open(path_file + '\\' + pf[i], 'rb') as f:
        #             ftp.storbinary('STOR ' + pf[i], f)
        #
        #         with open(log_txt, 'a', encoding='utf-8') as f:
        #             f.write(f"Копирование {str(pf[i])} сделано в {str(date.today())} \n")
        #     except:
        #         pass
        # data = ftp.retrlines('LIST')
        ftp.quit()


if __name__ == '__main__':
    run()
