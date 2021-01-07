#必要なモジュールをインポート
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

#ポート番号の定義
Trig = 27                           #変数"Trig"に27を代入
Echo = 23                           #変数"Echo"に23を代入
Servo_pin = 18                      #変数"Servo_pin"に18を格納

#GPIOの設定(超音波センサ)
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo, GPIO.IN)           #GPIO23を入力モードに設定
GPIO.setup(Servo_pin, GPIO.OUT)     #GPIO18を出力モードに設定

#GPIOの設定(LED)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

#PWMの設定
#サーボモータSG90の周波数は50[Hz]
Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])
Servo.start(0)                      #Servo.start(デューティ比[0-100%])

#角度からデューティ比を求める関数
def servo_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)     #デューティ比を変更

#HC-SR04で距離を測定する関数
def read_distance():
    GPIO.output(Trig, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo) == GPIO.LOW:     #GPIO23がLowの時間
        sig_off = time.time()
    while GPIO.input(Echo) == GPIO.HIGH:    #GPIO23がHighの時間
        sig_on = time.time()

    duration = sig_on - sig_off             #GPIO23がHighしている時間を演算
    distance = duration * 34000 / 2         #距離を求める(cm)
    return distance

#連続して値を超音波センサの状態を読み取る
while True:
    try:
        cm = read_distance()                   #HC-SR04で距離を測定する
        if cm > 30 and cm < 60:                 #距離が30〜60cmの場合
            GPIO.output(25, GPIO.HIGH)
            servo_angle(90)
            servo_angle(-90)
            servo_angle(90)
            servo_angle(-90)
            servo_angle(90)
            servo_angle(-90)
            GPIO.output(25, GPIO.LOW)
        time.sleep(0.01)                       #0.01秒間待つ

    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        Servo.stop()                #サーボモータをストップ
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了