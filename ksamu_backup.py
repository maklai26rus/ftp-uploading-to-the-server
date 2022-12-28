import os
# import json
from ftplib import FTP
from datetime import date
from setting_ftp import log_txt, ftp_setting_json, folder_json, path_normal

fs = folder_json()
fsj = ftp_setting_json()


def run():
    """Вызгрузка файлов на сервер FTP"""
    with FTP(host=fsj['ftp']['host']) as ftp:
        ftp.login(user=fsj['ftp']['user'], passwd=fsj['ftp']['password'])
        if fsj['ftp']['catalog'] is not None:
            ftp.cwd(fsj['ftp']['catalog'])

        path = fs['folder']['path']

        files_list = os.listdir(path)
        files = list(map(path_normal, [os.path.join(path, i) for i in files_list]))
        files = [file for file in files if os.path.isfile(file)]
        try:
            file_save = max(files, key=os.path.getmtime)
        except ValueError:
            pass

        split_path = file_save.split('\\')

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

        arh = fs['folder']['new_name_file'] + '.' + split_path[-1].split('.')[-1]

        try:
            with open(file_save, 'rb') as f:
                ftp.storbinary('STOR ' + arh, f)
        except:
            print('Ошибка')
        # data = ftp.retrlines('LIST')
        with open(log_txt, 'a', encoding='utf-8') as f:
            f.write(f'Копирование {str(arh)} сделано в {str(date.today())} \n')

        ftp.quit()


if __name__ == '__main__':
    run()
