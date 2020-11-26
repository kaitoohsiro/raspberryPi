import RPi.GPIO as GPIO
import time
import sys

## ポート番号
Tring = 11  ## 適当な数字を現時点では指定している
Echo = 11  ## 適当な数字を現時点では指定している

#GPIOの設定（集積回路やコンピュータボード上での設定）
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo, GPIO.IN)           #GPIO18を入力モードに設定


#HC-SR04で距離を測定する関数
def read_distance():
    GPIO.output(Trig, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ(ここをいじってみる)
    GPIO.output(Trig, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo) == GPIO.LOW:     #GPIO18がLowの時間
        low_time = time.time()
    while GPIO.input(Echo) == GPIO.HIGH:    #GPIO18がHighの時間
        high_time = time.time()

    difference = low_time - high_time         #GPIO18がHighしている時間を算術
    distance = difference * 34000 / 2         #距離を求める(cm)
    return distance

#連続して値を超音波センサの状態を読み取る
while True:
    try:
        distance = read_distance()                     #HC-SR04で距離を測定する
        # 消毒液を噴射する条件
        if distance > 10 and distance < 50:            #距離が10～50cmの場合（反応距離はセンサーの位置に依存するから変更あり）
        #     print("distance = ", int(distance), "cm")  #距離をint型で表示
        # time.sleep(1)                                  #1秒間待つ

    # 強制終了
    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了