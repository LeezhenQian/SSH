import paramiko
import datetime
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import openpyxl
import socket

# 获取交换机配置（只包含英文）
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


# 获取华为OLT交换机配置
def OLT_switch_config(ip, username, password, port=50, filename='Olt_{}.txt'):
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
            output = channel.recv(65535).decode("gb18030")
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



def use_info():
    print((' 1.邮箱反馈:370005209@qq.com '
           '\n 2.仅支持导入.xlsx格式的Excel表格 '
           '\n 3.使用display current-configuration进行配置备份 '
           '\n 4.仅支持华为、华三、华为OLT等部分型号的配置备份 '
           '\n 5.[1]交换机配置编码为utf-8, [2]华为OLT配置编码为gb18030 '
           '\n 6.如果OLT配置有中文字符则需要使用选项[2],否则使用选项[1]会自动省去中文 '
           '\n 7.默认线程为50 '
           '\n 8.OLT与AC的配置较多，导出时间可能较长'))


def g_quit():
    exit()


# 选择excel文件路径
def road_choose():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    path = filedialog.askopenfilename()  # 弹出文件选择对话框
    return path


if __name__ == '__main__':
    # 选择需要1交换机配置备份，2华为OLT配置备份，3使用说明，4退出程序。哪种功能
    while True:
        choice = int(input('请选择1、交换机配置备份，2、华为OLT配置备份，3、使用说明，4、退出程序。\n'))
        if choice == 1:
            normal_switch_config()
        elif choice == 2:
            OLT_switch_config()
        elif choice == 3:
            use_info()
        elif choice == 4:
            g_quit()
        else:
            print('您输入有误请重新输入')

