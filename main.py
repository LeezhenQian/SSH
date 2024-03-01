import paramiko
import datetime
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import openpyxl
import socket



def normal_switch_config(port=50, filename='test_{}.txt'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    # 读取excel文件路径
    excel_path = road_choose()
    print("你选择的文件是:", excel_path)
    # 读取excel文件中的内容
    df = pd.read_excel(excel_path)
    # 创建txt保存的文件夹
    print('请输入公司名：')
    # backup_folder = input() + '_交换机'+datetime.datetime.now().strftime("%Y%m%d")
    backup_folder = os.path.splitext(excel_path)[0] + '交换机' + input()
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    for index, row in df.iterrows():
        ip = row['IP']
        username = row['username']
        password = row['password']
        print(ip, username, password)
        # normal_switch_config(path=backup_folder,ip=ip,username=username,password=password,)

        socket.setdefaulttimeout(5.0)  # 5秒超时
        try:
            # 连接交换机
            client.connect(ip, port=port, username=username, password=password)
            # 创建命令会话
            channel = client.invoke_shell()
            # 发送命令，查看config
            channel.send("show running-config\n")
            # 等待命令执行完成
            while not channel.recv_ready():
                pass
            # 读取输出的config
            output = channel.recv(65535).decode("utf-8")
            client.close()

            # 创建备份的文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = filename.format(timestamp)+ip
            # back_file = filename.format(ip)
            with open(backup_file, 'w') as file:
                file.write(output)
            print(f"Backup is completed,saved to {backup_file}")
        except socket.timeout:
            print("Connection timed out.")
        except Exception as e:
            print(f"we meet error called:{e}")
        finally:
            client.close()
