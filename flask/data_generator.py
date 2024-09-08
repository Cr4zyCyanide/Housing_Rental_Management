import random
import re
import os
import hashlib
from sql import *

digits = '0123456789'
lower_letters = 'abcdefghigklmnopqrstuvwxyz'

db = Database("127.0.0.1", "", "", "")


def userInfoGenerator():
    # generate a random username
    random_name_no = random.randint(0, 1000000)
    random_name = f"test_user_{random_name_no}"

    # generate a random email
    random_str = ''.join(random.sample(lower_letters + digits, random.randint(5, 12)))
    domains = ['qq', 'gmail', '163', 'yahoo', 'outlook']
    random_email = random_str + '@' + random.choice(domains) + '.com'

    # generate a random phone number
    phone_head_list = ['135', '136', '137', '138', '139', '131', '151', '166', '177', '188']
    random_phone = random.choice(phone_head_list) + str(random.randint(10000000, 99999999))

    # generate a random id
    while True:
        id_pattern = re.compile("^[1-9]\\d{16}[0-9X]$")
        id_region = str(random.randint(110000, 659000))
        id_year = str(random.randint(1949, 2008))
        id_month = str(random.randint(1, 12)).zfill(2)
        id_date = str(random.randint(1, 28)).zfill(2)
        id_order = str(random.randint(1, 999)).zfill(3)
        id_check = str(random.choice("0123456789X"))
        id_number = id_region + id_year + id_month + id_date + id_order + id_check
        if id_pattern.match(id_number):
            break

    info = {
        "username": random_name,
        "email": random_email,
        "phone": random_phone,
        "id": id_number
    }
    return info


def rentalInfoGenerator():
    # get an existing user(not an operator) from database
    user_list = db.getUsers()
    random_publisher = random.choice(user_list)

    random_area = random.randint(40, 200)
    random_floor = random.randint(1, 32)
    random_rent = int(random.gauss(random_area * 27, random_area * 5))
    random_ori = random.choice(['东', '南', '西', '北'])

    info = {
        'publisher': random_publisher,
        'address': f'xx区xx小区xx栋xx单元{random.randint(1000, 9999)} (测试用)',
        'area': random_area,
        'floor': random_floor,
        'rent': random_rent,
        'house_type': 'type for testing',
        'orientation': random_ori
    }
    return info


def insert_testUser(count: int):
    i = 0
    while i < count:
        userinfo: dict = userInfoGenerator()
        pwd_hash_layer1 = hashlib.sha256("123456".encode("utf-8")).hexdigest()
        db.insertUser(
            username=userinfo['username'],
            pwd_hash=hashlib.sha3_512(("salt" + pwd_hash_layer1).encode("utf-8")).hexdigest()
        )
        db.insertUserInfo(
            username=userinfo['username'],
            id_number=userinfo['id'],
            phone=userinfo['phone'],
            email=userinfo['email'],
            contact_info=''
        )
        i += 1


def insert_rentalInfo(count: int):
    i = 0
    while i < count:
        rentalInfo: dict = rentalInfoGenerator()
        db.insertRental(
            username=rentalInfo['publisher'],
            address=rentalInfo['address'],
            area=rentalInfo['area'],
            floor=rentalInfo['floor'],
            rent=rentalInfo['rent'],
            house_type=rentalInfo['house_type'],
            orientation=rentalInfo['orientation']
        )
        i += 1


def generator_terminal():
    print("请选择要生成的用户数据:")
    print("1.新用户名以及其密码(生成的用户密码统一为123456)")
    print("2.出租信息")
    while True:
        select = input("请选择想要使用的功能:(输入1-2的整数)")
        op = ['1', '2']
        if select in op:
            break
        else:
            print("输入类型有误，请重试")
    if select == '1':
        while True:
            count: int = eval(input("请输入想要生成新用户的个数:"))
            if count > 0:
                insert_testUser(count)
                break
    elif select == '2':
        while True:
            count = eval(input("请输入想要生成新用户的个数:"))
            if count > 0:
                insert_rentalInfo(count)
                break


if __name__ == "__main__":
    generator_terminal()
