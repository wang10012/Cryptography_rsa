import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, scrolledtext
import tkinter.font as tf

from wsj_rsa import *

file_path = ''
file_text = ''
p = 0
q = 0
n = 0
Euler_fun = 0
e = 65537
d = 0


class Window(object):

    def __init__(self):
        root = tk.Tk()
        root.minsize(675, 425)  # 窗口大小
        root.resizable(width=False, height=False)  # False窗口大小不可变

        root.title('RSA加密及解密系统')  # 窗口标题

        ft = tf.Font(family='Fixdsys', size=15)

        button_load_file = Button(text='载入文件', command=self.open_file)  # 载入文件按钮
        button_load_file.place(x=10, y=10, width=80, height=25)

        self.line_text_load_file = Entry(root)  # 单行文本输入
        self.line_text_load_file.place(x=100, y=10, width=535, height=25)

        button_generate_key = Button(text='生成密钥', command=self.generate_key)  # 生成密钥按钮
        button_generate_key.place(x=10, y=100, width=80, height=25)

        self.line_key = scrolledtext.ScrolledText(root, font=ft)  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        self.line_key.place(x=100, y=50, width=550, height=150)

        button_encrypt = Button(text='开始加密', command=self.rsa_encrypt)  # 加密按钮
        button_encrypt.place(x=100, y=220, width=535, height=25)

        label_encrypted = Label(text='加密后文件：')  # 标签
        label_encrypted.place(x=10, y=275, width=80, height=25)  # 确定位置

        self.line_encrypted_file = Entry(root)  # 单行文本输入
        self.line_encrypted_file.place(x=100, y=275, width=535, height=25)

        button_decrypt = Button(text='对此加密文件进行解密', command=self.rsa_decrypt)  # 加密按钮
        button_decrypt.place(x=100, y=320, width=535, height=25)

        label_decrypted = Label(text='解密后文件：')  # 标签
        label_decrypted.place(x=10, y=375, width=80, height=25)  # 确定位置

        self.line_decrypted_file = Entry(root)  # 单行文本输入
        self.line_decrypted_file.place(x=100, y=375, width=535, height=25)

        root.mainloop()  # 主循环

    def open_file(self):
        '''
        打开文件
        :return:
        '''
        self.line_text_load_file.delete(0, "end")
        global file_path
        global file_text
        file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('H:/')))
        print('打开文件：', file_path)
        if file_path is not '':
            with open(file=file_path, mode='r+', encoding='utf-8') as file:
                file_text = file.read()
            self.line_text_load_file.insert('insert', file_path)
        if file_path == '':
            print("未打开文件")
        print("file_path:" + file_path)

    def generate_key(self):
        self.line_key.delete('1.0', 'end')
        global p
        p = get_prime()
        global q
        q = get_prime()
        global n
        n = p * q
        global Euler_fun
        Euler_fun = euler(p, q)
        # e = generate_puk(Euler_fun)
        global e
        e = 65537  # 一般互联网中使用RSA加密均使用e=65537
        global d
        d = generate_prk(e, Euler_fun)
        self.line_key.insert('insert', "用到的大素数p:" + str(p) + '\n')
        self.line_key.insert('insert', "\n")
        self.line_key.insert('insert', "用到的大素数q:" + str(q) + '\n')
        self.line_key.insert('insert', "\n")
        self.line_key.insert('insert', "这两个大素数的乘积为：" + str(n) + '\n')
        self.line_key.insert('insert', "\n")
        self.line_key.insert('insert', "其欧拉函数为：" + str(Euler_fun) + '\n')
        self.line_key.insert('insert', "\n")
        self.line_key.insert('insert', "公钥为：(" + str(e) + "," + str(n) + ")" + '\n')
        self.line_key.insert('insert', "\n")
        self.line_key.insert('insert', "生成的私钥为：(" + str(d) + "," + str(n) + ")" + '\n')
        self.line_key.insert('insert', "\n")

    def rsa_encrypt(self):
        self.line_encrypted_file.delete(0, "end")
        message = []
        result = []
        result_path = 'C:/Users/LENOVO/Desktop/Cryptography_project/encrypted_result.txt'
        with open(file_path, 'rb') as f:
            for x in f.read():
                message.append(int(x))
            for m in message:
                result.append(exp_mode(int(m), e, n))
        with open(result_path, 'w') as m:
            for x in result:
                m.write(str(x) + '\r')
        self.line_encrypted_file.insert('insert', result_path)

    def rsa_decrypt(self):
        self.line_decrypted_file.delete(0, "end")
        result = []
        result_path = 'C:/Users/LENOVO/Desktop/Cryptography_project/decrypted_result.txt'
        with open(file_path) as f:
            for x in f.readlines():
                result.append(exp_mode(int(x), d, n))
        with open(result_path, 'wb') as m:
            m.write(bytes(result))
        self.line_decrypted_file.insert('insert', result_path)
