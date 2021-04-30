import random
import sys

from numpy import long

sys.setrecursionlimit(9000000)  # 递归深度设置提高


def extension_euclid(a, b):
    """
    扩展欧几里得算法
    :param a:
    :param b:
    :return:
    """
    if b == 0:
        return 1, 0, a
    x, y, gcd = extension_euclid(b, a % b)
    return y, x - a // b * y, gcd


def rabin_miller(num):
    """
    rabin_miller素性测试算法
    :param num:
    :return:
    """
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(10):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    # 排除0,1和负数
    if num < 2:
        return False

    # 创建小素数的列表,可以大幅加快速度
    # 如果是小素数,那么直接返回true
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]
    if num in small_primes:
        return True

    # 如果大数是这些小素数的倍数,那么就是合数,返回false
    for prime in small_primes:
        if num % prime == 0:
            return False

    # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
    return rabin_miller(num)


# 得到大整数,默认位数为1024
def get_prime(key_size=1024):
    while True:
        num = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if is_prime(num):
            return num


def generate_puk(Euler_fun):
    """
    生成公钥
    :param Euler_fun:
    :return:
    """
    while True:
        num = random.randint(2, Euler_fun)
        if extension_euclid(num, Euler_fun)[2] == 1:
            return num


def generate_prk(e, Euler_fun):
    """
    生成私钥
    :param e:
    :param Euler_fun:
    :return:
    """
    f = extension_euclid(e, Euler_fun)
    return f[0] % Euler_fun


def euler(p, q):
    """
    欧拉函数
    :param p:
    :param q:
    :return:
    """
    return (p - 1) * (q - 1)


def exp_mode(base, exponent, n):
    """
    蒙哥马利幂模算法
    :param base:
    :param exponent:
    :param n:
    :return:
    """
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n
        base_array.append(next_base)
        pre_base = next_base

    result = __multi(base_array, bin_array, n)
    return result % n


def __multi(array, bin_array, n):
    """
    辅助方法 用来连乘
    :param array:
    :param bin_array:
    :param n:
    :return:
    """
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n  # 加快连乘的速度
    return result


def encrypt(m, e, n):
    """
    加密
    :param m:
    :param e:
    :param n:
    :return:
    """
    msg = msg_to_int(m)
    c = exp_mode(msg, e, n)
    # msg = list(map(ord, m))  # 数字化
    # c = []
    # for x in msg:
    #     c.append(exp_mode(x, e, n))
    return c


def decrypt(c, d, n):
    """
    解密
    :param c:传入数字
    :param d:
    :param n:
    :return:
    """
    m = exp_mode(c, d, n)
    return int_to_msg(m)
    # plaintext = []
    # for x in c:
    #     plaintext.append(exp_mode(x, d, n))
    # return bytes(plaintext)


def msg_to_int(msg):
    """
    把字符串转换成数字
    :param msg:
    :return:
    """
    b = msg.encode(encoding='UTF-8')
    res = int(b.hex(), 16)
    # message = list(map(ord, msg))  # 数字
    # res = []
    # for x in message:
    #     res.append(pow(x, e, n))
    return res


def int_to_msg(m_num):
    """
    把数字转换成字符串`
    :param m_num:
    :return:
    """
    hex_num = hex(m_num)
    pure = hex_num[2:]
    msg_bytes = bytes.fromhex(pure)

    return msg_bytes.decode(encoding='UTF-8', errors='ignore')


def main1():
    p = 178301413501630336956776299999583225023729596096591592494755957878838154431712028012342101001785623453284616271572196818667185321361134107159019363506612727883143441005063438777901982589849889774248438059700078836209852897881664908420999861842680240595902113823201259543956606094937395754408139610260463578591
    q = 127509724926803530065232218798991510526520565598786907218328592699997127087187298090532452958192873618401268402517603744005731588340343179855141589284355615917192139686160455727482592085063021510927678392513383845590846176441348320921875218424092363754950789846189097591361029735302893751636206549244006969407
    # p = get_prime()
    # q = get_prime()
    n = p * q
    Euler_fun = euler(p, q)
    # e = generate_puk(Euler_fun)
    e = 65537  # 一般互联网中使用RSA加密均使用e=65537
    print("用到的大素数为：", p)
    print("用到的大素数为：", q)
    print("这两个大素数的乘积为：", n)
    print("其欧拉函数为：", Euler_fun)
    print("公钥为：(" + str(e) + "," + str(n) + ")")
    d = generate_prk(e, Euler_fun)
    print("生成的私钥为：(" + str(d) + "," + str(n) + ")")
    print('请输入明文:')
    plain_text = input()
    plain_number = msg_to_int(plain_text)
    print("明文转为数字后的结果为：", plain_number)
    print("加密后的密文结果为:")
    cipher_text = encrypt(plain_text, e, n)
    print(cipher_text)
    encrypt_number = exp_mode(cipher_text, d, n)
    print("解密后得到的数字结果为：", encrypt_number)
    print("对密文进行解密后:")
    decrypted_text = decrypt(cipher_text, d, n)
    print(decrypted_text)


def main2():
    # p = 12203784560739063841055714433167612997448850910465176835928034238805442755752599786325743660501454809740192260682118889176259852228765822048023685691698857
    # q = 7597290770382093475275473298508861825954038293563206229438263577970410452555258851465932863176877073163990234692467157966005233053672750035983687087359621
    # p = get_prime()
    # q = get_prime()
    p = 157726576118512093066982796794326528428073340145406599913231171179424889886896584188251696431884033896201186172146084281710843973146629386523733669318023395688536509003914270056593409153705504787184643686595905652744182918181057130033407552017196302541112748134347021217684422996074734861084695432578232158283
    q = 131366543385678563795341097166758110076039634760442240806001808463385595352141346477150778645614314220691025045327992456371486692060458427431931262189496317473011704990325439777065125572929761545679115549582499632650019721070703170586132485458401771049486192697970455042400976416050103530574415374179454174877
    n = p * q
    e = 65537  # 一般互联网中使用RSA加密均使用e=65537
    result = ""
    with open('C:/Users/LENOVO/Desktop/Cryptography_project/test_file.txt', 'r', encoding='UTF-8') as f:
        while True:
            chs = f.read(5)
            if not chs:
                break
            result += str(encrypt(chs, e, n))
    with open('C:/Users/LENOVO/Desktop/Cryptography_project/result.txt', 'w', encoding='UTF-8') as m:
        m.write(result)


def choosen_cipher_text_attack1():
    p = 178301413501630336956776299999583225023729596096591592494755957878838154431712028012342101001785623453284616271572196818667185321361134107159019363506612727883143441005063438777901982589849889774248438059700078836209852897881664908420999861842680240595902113823201259543956606094937395754408139610260463578591
    q = 127509724926803530065232218798991510526520565598786907218328592699997127087187298090532452958192873618401268402517603744005731588340343179855141589284355615917192139686160455727482592085063021510927678392513383845590846176441348320921875218424092363754950789846189097591361029735302893751636206549244006969407
    n = p * q
    Euler_fun = euler(p, q)
    e = 65537  # 一般互联网中使用RSA加密均使用e=65537
    d = generate_prk(e, Euler_fun)
    # 58736209353191739422782134497356011033998431547699167074781335871327247608531018428309924673463874412
    c = 5015547068662436689489321306393575050328114285634469201734275495529811622508348111616218916464483996421853049674222721452180884437297934131281565229617440275461288365729380999261241229594702244039609751274172084405868164820461731881891434859970435935597251479675286447406093872755357777752933947861696690526684319516840092683785397592539218587618061904286560735196943229801935276299261440678148308821811359518949533358094744989338298579238312215037038200886856439672741438691257196732482731659119537084233773985158604603904446465753652220116738057026517431729498215325983266843902850833722599366313933174207997300498
    r = generate_puk(n)  # 此时是生成随机数r
    t = generate_prk(r, n)  # 生成r关于n的逆元t
    x = exp_mode(r, e, n)
    y = (x * c) % n
    u = exp_mode(y, d, n)
    result = (t * u) % n
    print("结果为：" + int_to_msg(result))


def choosen_cipher_text_attack2():
    p = 12203784560739063841055714433167612997448850910465176835928034238805442755752599786325743660501454809740192260682118889176259852228765822048023685691698857
    q = 7597290770382093475275473298508861825954038293563206229438263577970410452555258851465932863176877073163990234692467157966005233053672750035983687087359621
    n = p * q
    euler_fun = euler(p, q)
    e = 65537
    d = 79966353839703043482696794705831485556226221363031465787554102009700795844934317922363695242420955947330451891856824559335522077973715242300321269612064247558785734707312727047142528240907145540763408475081832130802932624660543153347351493579538341074304098455099719788441775522643393951573252244989191677473

    c = 30240597482101106201974950835829388178153470045189323653672571328879384712189248754190274715173068055874574437612166095168399734845568351568612176828684496546753108699067932198775145416556263452856044482994434006443932497648115626307069807041252326314471386940928141185185341958748698339538536976792983526506

    print("请输入您随机选择的密文以获得其解密服务")
    random_cipher_text = long(input())
    random_plain_text = decrypt(random_cipher_text, d, n)
    print("您输入的密文对应的明文为" + random_plain_text)

    product = c * random_cipher_text
    product_plain_number = exp_mode(product, d, n)
    random_plain_number = exp_mode(random_cipher_text, d, n)
    c_plain_number = product_plain_number // random_plain_number
    print("所以对密文的攻击结果为：" + int_to_msg(c_plain_number))


# 87224211072136884488135002404533263671456237664142939588222832690012556318046489640430702274403236196863467169188820693449122873227595221709169524453993598039223998057819503017365637970718716430503774707261369811473846611674766394850265321082200669604220117419136260569553469872164067476665113430814106292537
if __name__ == '__main__':
    # choosen_cipher_text_attack2()
    # choosen_cipher_text_attack1()
    main1()
