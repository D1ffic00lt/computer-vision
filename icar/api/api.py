import os
import time
import pigpio

from flask import Flask, request, make_response, jsonify

application = Flask(__name__)


def setup_gpio():
    os.system("sudo pigpiod")
    time.sleep(1)
    ESC = 17
    STEER = 18
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    pi.set_servo_pulsewidth(STEER, 0)
    time.sleep(1)
    return pi, ESC, STEER


pi, ESC, STEER = setup_gpio()


def control(pi, ESC, speed, STEER, angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER, int(11.1 * angle + 500))


@application.route("/app/api/v1.0/do/", methods=["POST"])
def do_something():
    data = request.json
    # print(data["object"])
    if data["object"] == 'forward':
        # print("[INFO]: forward")
        control(pi, ESC, 1560, STEER, 90)
        time.sleep(1)
    elif data["object"] == 'back':
        # print("[INFO]: back")
        control(pi, ESC, 1430, STEER, 90)
        time.sleep(1)
    elif data["object"] == "left":
        # print("[INFO]: left")
        control(pi, ESC, 1500, STEER, 110)
        time.sleep(1)
    elif data["object"] == "right":
        # print("[INFO]: right")
        control(pi, ESC, 1500, STEER, 72)
        time.sleep(1)
    elif data["object"] == "stop":
        # print("[INFO]: stop")
        control(pi, ESC, 1500, STEER, 90)
        time.sleep(1)
    return make_response(jsonify({"status": True}), 201)


if __name__ == "__main__":
    application.run("0.0.0.0", port=1354)
