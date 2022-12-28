from ftplib import FTP
# import json
import os
from datetime import date

from setting_ftp import log_txt, ftp_setting_json, folder_json

fs = folder_json()
fsj = ftp_setting_json()
path_file = fs['folder']['path']


def run():
    """Вызгрузка файлов на сервер FTP"""
    with FTP(host=fsj['ftp']['host']) as ftp:
        ftp.login(user=fsj['ftp']['user'], passwd=fsj['ftp']['password'])
        if fsj['ftp']['catalog'] is not None:
            try:
                ftp.cwd(fsj['ftp']['catalog'])
            except:
                ftp.mkd(fsj['ftp']['catalog'])
                ftp.cwd(fsj['ftp']['catalog'])

        pf = os.listdir(path_file)

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

        for i in range(len(pf)):

            try:
                with open(path_file + '\\' + pf[i], 'rb') as f:
                    ftp.storbinary('STOR ' + pf[i], f)

                with open(log_txt, 'a', encoding='utf-8') as f:
                    f.write(f"Копирование {str(pf[i])} сделано в {str(date.today())} \n")
            except:
                pass
        # data = ftp.retrlines('LIST')
        ftp.quit()


if __name__ == '__main__':
    run()
