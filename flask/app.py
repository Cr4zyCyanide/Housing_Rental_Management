from flask import Flask, jsonify, request
from flask_cors import CORS
from sql import *
import hashlib
import re

app = Flask(__name__)
CORS(app)

db = Database(
    host="",
    user="",
    passwd="",
    db_name=""
)


@app.route("/")
def index():
    return "hello"


@app.route("/api/hello", methods=['GET'])
def hello():
    data = {'message': 'Hello from Flask'}
    return jsonify(data)


@app.route("/api/registry", methods=['POST'])
def registry():
    data = request.json
    if data:
        print(data)
        userList: list = db.getAllUsers()
        if data['username'] not in userList:
            regUsername = re.compile("^[a-zA-Z0-9_-]{4,16}$")
            regIdNumber = re.compile(
                "^[1-9]\\d{5}(19|20|21)\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$")
            regPhone = re.compile("^1[3,4,5,7,8][0-9]{9}$")
            regEmail = re.compile("^([a-zA-Z]|[0-9])(\\w|-)+@[a-zA-Z0-9]+\\.([a-zA-Z]{2,4})$")
            regContactInfo = re.compile(r'^[^\s"#$%&\'()*+\-/<=>?@[\\\]^_`{|}~]*$')
            if regUsername.match(data['username']) and regIdNumber.match(data['id_number']) and regPhone.match(
                    data['phone']) and regEmail.match(data['email']) and regContactInfo.match(data['contact_info']):
                # pwd_hash = sha512( "salt" + sha256(pwd))
                pwd_hash = hashlib.sha3_512(("salt" + data['pwd_hash']).encode("utf-8")).hexdigest()
                try:
                    db.insertUser(
                        username=data['username'],
                        pwd_hash=pwd_hash,
                        isOperator=False
                    )
                    db.insertUserInfo(
                        username=data['username'],
                        id_number=data['id_number'],
                        phone=data['phone'],
                        email=data['email'],
                        contact_info=data['contact_info']
                    )
                    print("[info]User Registration Successful")
                    db.insertLog(
                        event='注册',
                        username='guest',
                        ip=request.remote_addr,
                        note="注册成功，新用户名:" + data['username']
                    )
                    return jsonify({
                        'status': True,
                        'code': 0,
                        'info': 'REGISTRATION SUCCESSFUL'
                    })
                except UserWarning:
                    print("[error:-11]Insert user data failed.")
                    db.insertLog(
                        event='注册',
                        username='guest',
                        ip=request.remote_addr,
                        note='注册失败，数据库插入数据失败'
                    )
                    return jsonify({
                        'status': False,
                        'code': -11,
                        'info': 'Server or database error'
                    })
            else:
                print("[browser error:-10]Illegal information injection")
                print(regUsername.match(data['username']), regIdNumber.match(data['id_number']),
                      regPhone.match(data['phone']), regEmail.match(data['email']),
                      regContactInfo.match(data['contact_info']))
                db.insertLog(
                    event='注册',
                    username='guest',
                    ip=request.remote_addr,
                    note='注册失败，使用了非法的信息'
                )
                return jsonify({
                    'status': False,
                    'code': -10,
                    'info': 'Illegal information injection'
                })
        else:
            print(f"[info]username {data['username']} already exists.")
            db.insertLog(
                event='注册',
                username='guest',
                ip=request.remote_addr,
                note='注册失败，使用了已存在的用户名' + data['username']
            )
            return jsonify({
                'status': False,
                'code': -1,
                'info': 'Username already exists'
            })
    else:
        print("[browser error:-2]Illegal or empty form.")
        db.insertLog(
            event='注册',
            username='guest',
            ip=request.remote_addr,
            note='注册失败，传入了一个非法或空的表单'
        )
        return jsonify({
            'status': False,
            'code': -2,
            'info': 'Illegal or empty form'
        })


@app.route("/api/login", methods=['POST'])
def login():
    # using SHA-256
    data = request.json
    if data:
        # print(data)
        userList: list = db.getAllUsers()
        if data['username'] in userList:
            pwd_hash = hashlib.sha3_512(("salt" + data['pwd_hash']).encode("utf-8")).hexdigest()
            # print(pwd_hash)
            if db.loginVerify(data['username'], pwd_hash):
                print(f"[info]user {data['username']} login succeed.")
                db.insertLog(
                    event='登录',
                    username=data['username'],
                    ip=request.remote_addr,
                    note='登陆成功'
                )
                return jsonify({
                    'status': True,
                    'code': 0,
                    'info': "LOGIN SUCCESSFULLY",
                    'userInfo': {
                        'username': data['username'],
                        'isOperator': db.isOperator(data['username'])
                    }
                })
            else:
                print(f"[info]user {data['username']} login failed: wrong passwd")
                db.insertLog(
                    event='登录',
                    username=data['username'],
                    ip=request.remote_addr,
                    note='登陆失败，使用了错误的密码'
                )
        return jsonify({
            'status': False,
            'code': -1,
            'info': 'wrong username or password'
        })
    else:
        print("[error:-2]Illegal or empty form.")
        db.insertLog(
            event='登录',
            username='unknown',
            ip=request.remote_addr,
            note='登陆失败，提交了一个非法或空的表单'
        )
        return jsonify({
            'status': False,
            'code': -2,
            'info': 'Illegal or empty form'
        })


@app.route("/api/publish", methods=['POST'])
def publish():
    data = request.json
    if data:
        print(data)
        userList: list = db.getAllUsers()
        print(userList)
        if data['username'] in userList:
            try:
                db.insertRental(
                    username=data['username'],
                    address=data['address'],
                    area=int(data['area']),
                    floor=int(data['floor']),
                    rent=int(data['rent']),
                    house_type=data['type'],
                    orientation=data['orientation'],
                    decoration=data['decoration'],
                    region=data['region'],
                    surroundings=data['surroundings']
                )
                print("[info]insert rental info succeed.")
                db.insertLog(
                    event='发布',
                    username=data['username'],
                    ip=request.remote_addr,
                    note='发布成功'
                )
                return jsonify({
                    'status': True,
                    'code': 0,
                    'info': 'INSERT RENTAL INFO SUCCEED.'
                })
            except UserWarning:
                print("[Server error:-11]Insert user data failed")
                db.insertLog(
                    event='发布',
                    username=data['username'],
                    ip=request.remote_addr,
                    note='发布失败，数据库或服务器出错'
                )
                return jsonify({
                    'status': False,
                    'code': -11,
                    'info': 'Server or database error'
                })
        else:
            print("[error:-1]username doesn't exist.")
            db.insertLog(
                event='发布',
                username='guest',
                ip=request.remote_addr,
                note='发布失败，当前用户未登录或使用了一个不存在的用户名'
            )
            return jsonify({
                'status': False,
                'code': -2,
                'info': "username doesn't exist."
            })
    else:
        print("[error:-2]Illegal or empty form.")
        db.insertLog(
            event='发布',
            username='unknown',
            ip=request.remote_addr,
            note='传入了一个非法或空的表单'
        )
        return jsonify({
            'status': False,
            'code': -2,
            'info': 'Illegal or empty form'
        })


@app.route("/api/get_rentals", methods=['GET'])
def getRentals():
    ret = []
    for row in db.getAllRentalInfo():
        userInfo: list = db.getUserInfo(row[1])
        ret.append({
            'rental_id': row[0],
            'publisher': row[1],
            'address': row[2],
            'area': row[3],
            'floor': row[4],
            'rent': row[5],
            'house_type': row[6],
            'region': row[7],
            'orientation': row[8],
            'decoration': row[9],
            'surroundings': row[10],
            'phone': userInfo[0],
            'email': userInfo[1]
        })
    return jsonify(ret)


@app.route("/api/get_rental_by_username", methods=['GET'])
def getRentalByUsername():
    publisher = request.values.get('publisher')
    ret = []
    for row in db.getAllRentalInfo(publisher):
        ret.append({
            'rental_id': row[0],
            'publisher': row[1],
            'address': row[2],
            'area': row[3],
            'floor': row[4],
            'rent': row[5],
            'house_type': row[6],
            'region': row[7],
            'orientation': row[8],
            'decoration': row[9],
            'surroundings': row[10],
        })
    return jsonify(ret)


@app.route("/api/get_rental_by_userid", methods=['GET'])
def getRentalByUserID():
    rentalInfo = db.getRentalsById(request.values.get('id'))
    return jsonify({
        'rental_id': rentalInfo[0],
        'publisher': rentalInfo[1],
        'address': rentalInfo[2],
        'area': rentalInfo[3],
        'floor': rentalInfo[4],
        'rent': rentalInfo[5],
        'house_type': rentalInfo[6],
        'region': rentalInfo[7],
        'orientation': rentalInfo[8],
        'decoration': rentalInfo[9],
        'surroundings': rentalInfo[10]
    })


@app.route("/api/update_rental", methods=['POST'])
def updateRental():
    data = request.json


@app.route("/api/get_logs", methods=['GET'])
def getLog():
    ret = []
    for row in db.getLog():
        ret.append({
            'id': row[0],
            'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'user': row[2],
            'ip': row[3],
            'event': row[4],
            'note': row[5]
        })
    return jsonify(ret)


@app.route("/api/get_userinfo", methods=['GET'])
def getUserInfo():
    ret = []
    for row in db.getAllUserInfo():
        ret.append({
            'username': row[0],
            'id_number': row[1],
            'phone': row[2],
            'email': row[3],
            'contact_info': row[4],
            'user_id': row[5],
            'user_type': row[8]
        })
    # print(ret)
    return jsonify(ret)


@app.route("/api/get_userinfo_by_name", methods=['GET'])
def getUserInfoByUsername():
    username = request.values.get('username')
    userInfo = db.getUserInfoByUsername(username)
    return jsonify({
        'username': userInfo[0],
        'id_number': userInfo[1],
        'phone': userInfo[2],
        'email': userInfo[3],
        'contact_info': userInfo[4]
    })


@app.route("/api/op", methods=['GET'])
def getIsOperator():
    data = request.values.get('username')
    # print(data)
    if data:
        return jsonify({
            'isOperator': db.isOperator(data)
        })


@app.route("/api/del_user", methods=['get'])
def delUser():
    userID = request.values.get('userId')
    # print(userID)
    if userID:
        try:
            db.delUser(userID)
            return jsonify({
                'status': True,
                'info': 'delete user successfully'
            })
        except UserWarning:
            return jsonify({
                'status': False,
                'info': 'server error'
            })
    else:
        return jsonify({
            'status': False,
            'info': 'invalid request'
        })


@app.route("/api/del_rental", methods=['get'])
def delRental():
    rentalID = request.values.get('rentalId')
    print(rentalID)
    if rentalID:
        try:
            db.delRentalByID(rentalID)
            return jsonify({
                'status': True,
                'info': 'delete rental info successfully'
            })
        except UserWarning:
            return jsonify({
                'status': False,
                'info': 'server error'
            })
    else:
        return jsonify({
            'status': False,
            'info': 'invalid request'
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4567, debug=False)
