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

r = 0
t = 0
x = 0
y = 0
u = 0


class rsa_attack_perform(object):

    def __init__(self):
        root = tk.Tk()
        root.minsize(700, 610)  # 窗口大小
        root.resizable(width=False, height=False)  # False窗口大小不可变

        root.title('RSA选择密文攻击演示系统')  # 窗口标题

        ft = tf.Font(family='Fixdsys', size=15)
        ft_attack = tf.Font(family='Times', size=15)

        button_load_file = Button(text='载入密文', command=self.open_file)  # 载入文件按钮
        button_load_file.place(x=10, y=10, width=80, height=25)

        self.line_text_load_file = Entry(root)  # 单行文本输入
        self.line_text_load_file.place(x=100, y=10, width=535, height=25)

        button_generate_key = Button(text='本次演示密钥', command=self.generate_key)  # 生成密钥按钮
        button_generate_key.place(x=10, y=100, width=80, height=25)

        self.line_key = scrolledtext.ScrolledText(root, font=ft)  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        self.line_key.place(x=100, y=50, width=550, height=150)

        button_act = Button(text='开始攻击演示', command=self.attack_perform)  # 加密按钮
        button_act.place(x=100, y=220, width=535, height=25)

        label_encrypted = Label(text='攻击过程：')  # 标签
        label_encrypted.place(x=10, y=405, width=80, height=25)  # 确定位置

        self.line_attack = scrolledtext.ScrolledText(root, font=ft_attack)
        self.line_attack.place(x=100, y=275, width=550, height=300)

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
        print("file_path:" + file_path)

    def generate_key(self):
        self.line_key.delete('1.0', 'end')
        global p
        p = 178301413501630336956776299999583225023729596096591592494755957878838154431712028012342101001785623453284616271572196818667185321361134107159019363506612727883143441005063438777901982589849889774248438059700078836209852897881664908420999861842680240595902113823201259543956606094937395754408139610260463578591
        global q
        q = 127509724926803530065232218798991510526520565598786907218328592699997127087187298090532452958192873618401268402517603744005731588340343179855141589284355615917192139686160455727482592085063021510927678392513383845590846176441348320921875218424092363754950789846189097591361029735302893751636206549244006969407
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

    def attack_perform(self):
        # self.line_attack.delete('1.0', 'end')
        c = int(file_text)
        r = generate_puk(n)  # 此时是生成随机数r
        t = generate_prk(r, n)  # 生成r关于n的逆元t
        x = exp_mode(r, e, n)
        y = (x * c) % n
        u = exp_mode(y, d, n)
        result = (t * u) % n
        plain_text_result = int_to_msg(result)
        print("攻击结果为：" + plain_text_result)
        self.line_attack.delete('1.0', 'end')
        self.line_attack.insert('insert', "1.攻击者选择随机数r < n，计算其关于n的逆元t:" + "\n")
        self.line_attack.insert('insert', "选择的r为：" + '\n')
        self.line_attack.insert('insert', str(r) + '\n')
        self.line_attack.insert('insert', "r关于n的逆元t为：" + '\n')
        self.line_attack.insert('insert', str(t) + '\n')
        self.line_attack.insert('insert', "\n")
        self.line_attack.insert('insert', "2.攻击者计算x=r的e方mod n,y=xc mod n" + '\n')
        self.line_attack.insert('insert', "计算的x为：" + str(x) + '\n')
        self.line_attack.insert('insert', "计算的y为：" + str(y) + '\n')
        self.line_attack.insert('insert', "\n")
        self.line_attack.insert('insert', "3.攻击者请求被发送方的签名服务，计算u = y的d方 mod n" + '\n')
        self.line_attack.insert('insert', "计算得到的u为：" + str(u) + '\n')
        self.line_attack.insert('insert', "\n")
        self.line_attack.insert('insert', "4.计算tu mod n,转成字符，即可攻击成功得到明文" + '\n')
        self.line_attack.insert('insert', "计算得到的结果为：" + str(result) + '\n')
        self.line_attack.insert('insert', "攻击得到的明文结果为：" + plain_text_result + '\n')
