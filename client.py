# deck_client.py
import pygame
from pymavlink import mavutil
import time

VPS_IP = '188.245.79.193'  # <-- сюда подставь IP VPS
VPS_PORT = 14550

def scale(val):
    return int(1500 + val * 500)  # RC: 1000–2000

def main():
    # Инициализация MAVLink
    master = mavutil.mavlink_connection(f'udpout:{VPS_IP}:{VPS_PORT}')
    print("MAVLink connection established")

    # Инициализация геймпада
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Gamepad: {joystick.get_name()}")

    while True:
        pygame.event.pump()
        roll  = joystick.get_axis(0)  # Лево-право
        pitch = -joystick.get_axis(1) # Вперёд-назад
        throttle = -joystick.get_axis(3)  # Газ
        yaw = joystick.get_axis(2)    # Вращение

        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            scale(roll),     # chan1
            scale(pitch),    # chan2
            scale(throttle), # chan3
            scale(yaw),      # chan4
            0, 0, 0, 0        # остальные каналы — без изменений
        )

        time.sleep(0.05)  # 20 Гц

if __name__ == '__main__':
    main()
