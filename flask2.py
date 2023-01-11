from flask import Flask, session, render_template, redirect, request, url_for, flash,  jsonify
from flaskext.mysql import MySQL
from DB import Database
from flask import request
import time
import RPi.GPIO as GPIO
import jwt

mysql = MySQL()
GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

servo_pin = 12                   # 서보핀은 라즈베리파이 GPIO 14번핀으로 

GPIO.setup(servo_pin, GPIO.OUT)  # 서보핀을 출력으로 설정 
servo = GPIO.PWM(servo_pin, 50)  # 서보핀을 PWM 모드 50Hz로 사용
servo.start(0)  # 서보모터의 초기값을 0으로 설정

servo_min_duty = 3               # 최소 듀티비를 2으로
servo_max_duty = 12              # 최대 듀티비를 13로
current_deg = 105                 # 현재 각도를 90도로

def set_servo_degree(degree):    # 각도를 입력하면 듀티비를 알아서 설정해주고 서보모터를 움직이는 함수
    # #8.5편에 나온 방법대로 서보모터가 떨리지 않게 함
    # 각도는 최소0, 최대 180으로 설정
    GPIO.setup(servo_pin, GPIO.OUT)         # 모터를 움직여야 하니 서보핀을 출력으로 설정
    past_time = time.time()                 # 과거 시간을 기록
    if degree > 180:                        # 입력받은 각도를 0~180도 사이로 재조정
        degree = 180
    elif degree < 0:
        degree = 0
    duty = servo_min_duty+(degree*(servo_max_duty-servo_min_duty)/180.0)    # 각도를 듀티비로 환산
    # 환산한 듀티비를 서보모터에 전달
    servo.ChangeDutyCycle(duty)             # 해당 각도대로 서보모터를 움직임
    while True:                             # 이부분은 sleep(0.5)와 같음(움직이는 시간동안 대기)
        current_time = time.time()
        if current_time - past_time > 0.5:
            break
    GPIO.setup(servo_pin, GPIO.IN)          # 0.5초간 기다린 후 서보핀을 입력으로 설정(서보모터가 움직이지 않음)
    return degree                           # 입력받은 각도를 출력
    
    
set_servo_degree(current_deg)

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'jh'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)

GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


@app.before_request
def before_request():
    print('success') 
@app.route('/', methods=['GET', 'POST'])
def main():
    error = None
 
    if request.method == 'POST':
        # Check if the request is a login request or a registration request
        if 'id' in request.form:
            # Login request
            id = request.form['id']
            pw = request.form['pw']
 
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT id FROM users WHERE id = %s AND pw = %s"
            value = (id, pw)
            cursor.execute("set names utf8")
            cursor.execute(sql, value)
 
            data = cursor.fetchall()
            cursor.close()
            conn.close()
 
            for row in data:
                data = row[0]
 
            if data:
                session['login_user'] = id
                
                return redirect(url_for('home'))
            else:

                error = 'invalid input data detected !'
                
        elif 'regi_id' in request.form:
            # Registration request
            id = request.form['regi_id']
            pw = request.form['regi_pw']
 
            conn = mysql.connect()
            cursor = conn.cursor()
 
            sql = "INSERT INTO users VALUES ('%s', '%s')" % (id, pw)
            cursor.execute(sql)
 
            data = cursor.fetchall()
 
            if not data:
                conn.commit()
                return redirect(url_for('main'))
            else:
                conn.rollback()
                return "Register Failed"
 
            cursor.close()
            conn.close()
    return render_template('main.html', error=error)




           
         
@app.route('/home.html', methods=['GET', 'POST'])
def home():
    error = None
    id = session['login_user']
    return render_template('home.html', error=error, name=id)

@app.route("/led/on")
def led_on():
    try:
        GPIO.output(14, GPIO.HIGH)
        return "on"
    except expression as identifier:
        return "fail"


@app.route("/led/off")
def led_off():
    try:
        GPIO.output(14, GPIO.LOW)
        return "off"
    except expression as identifier:
        return "fail"
@app.route("/fan/on")
def fan_on():
    try:
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        return "on"
    except expression as identifier:
        return "fail"


@app.route("/fan/off")
def fan_off():
    try:
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        return "off"
    except expression as identifier:
        return "fail"        
@app.route('/data')
def index():
    db=Database()
    sql_all=db.show()
    return render_template('data.html',list=sql_all)
@app.route('/motor')
def motor():
    return render_template('motor.html')
@app.route('/fancon')
def fan():
    return render_template('fancon.html')    
@app.route('/servo')                     # 기본 주소
def servomotor():                         # 여기서 index4#20.html을 화면에 보여주며, 서보모터 각도를 전달
    return render_template('index4#20.html', deg=current_deg)  

@app.route('/servo_control')        # 서보모터를 제어하기 위한 주소
def servo_control():                # 서보모터를 제어하기 위한 뷰함수
    deg = request.args.get('deg')   # html파일에서 각도를 입력받음
    deg = int(deg)                  # 각도를 정수형으로 바꿔주고 적절한 범위로바꿔줌
    if deg < 0: deg = 0
    elif deg > 180: deg = 180
    deg = set_servo_degree(deg)     # 서보모터 각도를 바꿔줌
    # index#20.html로 돌아가는데, 이때, deg 값을 넘겨줌(이 넘겨준 값은 html에서 사용할 수 있음)
    return render_template('index4#20.html', deg=deg)

# 플러터 연동API    

@app.route('/loginapp', methods=['POST'])
def loginapp():
    # Get the email and password from the request
    id = request.args.get('id')
    pw = request.args.get('pw')
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT id FROM users WHERE id = %s AND pw = %s"
    value = (id, pw)
    cursor.execute("set names utf8")
    cursor.execute(sql, value)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in data:
        data = row[0]

    if data:
        payload = {'user_id' : id}
        token = jwt.encode(payload, 'test183', algorithm='HS256')
        return jsonify({'success': True, 'token':token.decode('utf-8')}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401]
    
@app.route('/showapp')
def showapp():
    db=Database()
    HTD=db.show_app()
    return jsonify(HTD)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001 ,debug='True')
