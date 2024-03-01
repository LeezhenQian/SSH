# def function1():
#     print("执行功能1")
#
#
# def function2():
#     print("执行功能2")
#
#
# def function3():
#     print("执行功能3")
#
#
# def exit_program():
#     print("退出程序")
#     exit()
#
#
# function_dict = {
#     1: function1,
#     2: function2,
#     3: function3,
#     4: exit_program
# }
#
# while True:
#     choice = int(input("请输入功能序号（1-3）或退出序号（4）："))
#     if choice in function_dict:
#         function_dict[choice]()
#     else:
#         print("输入有误，请重新输入。")

def quit():
    exit()

func_list = {
    1: quit,
}
while True:
    choice = int(input('请输入：'))
    if choice in func_list:
        func_list[choice]()
    else:
        print('111')