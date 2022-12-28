import os
import json
from ftplib import FTP
from datetime import date
from setting_ftp import setting_server, log_txt, setting_folder, path_normal, read_json_file

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

        split_path = file_save.split('\\')

        try:
            ftp.cwd(j_sf['folder']['catalog'])
        except:
            ftp.mkd(j_sf['folder']['catalog'])
            ftp.cwd(j_sf['folder']['catalog'])

        try:
            ftp.cwd(j_sf['folder']['new_archive_folder'])
        except:
            ftp.mkd(j_sf['folder']['new_archive_folder'])
            ftp.cwd(j_sf['folder']['new_archive_folder'])

        arh = 'arhiv' + '.' + split_path[-1].split('.')[-1]

        try:
            with open(file_save, 'rb') as f:
                # ftp.storbinary('STOR ' + split_path[-1], f)
                ftp.storbinary('STOR ' + arh, f)
        except:
            print('Ошибка')
        # data = ftp.retrlines('LIST')
        with open(log_txt, 'a', encoding='utf-8') as f:
            f.write(f'Копирование {str(arh)} сделано в {str(date.today())} \n')

        ftp.quit()


if __name__ == '__main__':
    run()
