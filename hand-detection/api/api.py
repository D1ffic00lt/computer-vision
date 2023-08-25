import os
import time
import pigpio

from flask import Flask, request, make_response, jsonify

application = Flask(__name__)


def setup_gpio():
    os.system("sudo pigpiod")
    time.sleep(1)
    bot = pigpio.pi()
    bot.set_servo_pulsewidth(17, 0)
    bot.set_servo_pulsewidth(18, 0)
    time.sleep(1)
    return bot, 17, 18


pi, ESC, STEER = setup_gpio()


def control(bot, esc, speed, steer, angle):
    bot.set_servo_pulsewidth(esc, speed)
    bot.set_servo_pulsewidth(steer, int(11.1 * angle + 500))
    time.sleep(1)


@application.route("/app/api/v1.0/do/", methods=["POST"])
def do_something():
    data = request.json
    if data["object"] == 'forward':
        control(pi, ESC, 1560, STEER, 90)
    elif data["object"] == 'back':
        control(pi, ESC, 1430, STEER, 90)
    elif data["object"] == "left":
        control(pi, ESC, 1500, STEER, 110)
    elif data["object"] == "right":
        control(pi, ESC, 1500, STEER, 72)
    elif data["object"] == "stop":
        control(pi, ESC, 1500, STEER, 90)
    return make_response(jsonify({"status": True}), 201)


if __name__ == "__main__":
    application.run("0.0.0.0", port=1354)
