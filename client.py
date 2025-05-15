# deck_client.py
import pygame
from pymavlink import mavutil
import time

VPS_IP = '188.245.79.193'  # <-- сюда подставь IP VPS
VPS_PORT = 14550

def scale(val, neutral=1500, amplitude=400):
    return int(neutral + val * amplitude)

def main():
    # Инициализация MAVLink
    master = mavutil.mavlink_connection(f'udp:{VPS_IP}:{VPS_PORT}')
    master.wait_heartbeat()
    print(f"Connected to system {master.target_system}, component {master.target_component}")

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

        print(f"RC → roll: {scale(roll)}, pitch: {scale(pitch)}, throttle: {scale(throttle)}, yaw: {scale(yaw)}")

        time.sleep(0.05)  # 20 Гц

if __name__ == '__main__':
    main()
