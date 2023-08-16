import os
import time
import pigpio

from flask import Flask, make_response, request, jsonify

angles = iter([70, 90, 110])
direction = False
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
def do():
    global direction, angles
    data = request.json
    if data["object"] == 1:
        if direction:
            control(pi, ESC, 1500, STEER, 90)
        else:
            control(pi, ESC, 1560, STEER, 90)
        direction = not direction
    else:
        value = next(angles, -1)
        if value == -1:
            angles = iter([70, 90, 110])
            value = next(angles)
        control(pi, ESC, 1500, STEER, value)

    return make_response(jsonify({"status": True}), 201)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=1664)
