import pygame
from pymavlink import mavutil
import time

VPS_IP = '188.245.79.193'
VPS_PORT = 14550

def scale(val, neutral=1500, amplitude=400):
    return int(neutral + val * amplitude)

def main():
    # MAVLink init
    master = mavutil.mavlink_connection(f'udpout:{VPS_IP}:{VPS_PORT}')
    try:
        hb = master.wait_heartbeat(timeout=5)
        print(f"✅ Got heartbeat from system {hb.get_srcSystem()}, component {hb.get_srcComponent()}")
        target_system = hb.get_srcSystem()
        target_component = hb.get_srcComponent()
    except:
        print("⚠️ HEARTBEAT not received. Using default target IDs.")
        target_system = 1
        target_component = 1

    # Pygame init
    pygame.init()
    screen = pygame.display.set_mode((400, 300))  # нужно для обработки клавиш
    pygame.display.set_caption("RC Keyboard Control")

    # Инициализируем управление
    axes = {
        "roll": 0.0,
        "pitch": 0.0,
        "throttle": 0.0,
        "yaw": 0.0
    }

    print("🎮 Управление:")
    print("  WASD = pitch/roll (левый стик)")
    print("  стрелки = throttle/yaw (правый стик)")
    print("  ESC = выход")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()

        # Левый стик — WASD
        axes["roll"] = -1.0 if keys[pygame.K_a] else (1.0 if keys[pygame.K_d] else 0.0)
        axes["pitch"] = -1.0 if keys[pygame.K_w] else (1.0 if keys[pygame.K_s] else 0.0)

        # Правый стик — стрелки
        axes["yaw"] = -1.0 if keys[pygame.K_LEFT] else (1.0 if keys[pygame.K_RIGHT] else 0.0)
        axes["throttle"] = 1.0 if keys[pygame.K_UP] else (-1.0 if keys[pygame.K_DOWN] else 0.0)

        master.mav.rc_channels_override_send(
            target_system,
            target_component,
            scale(axes["roll"]),     # chan1 (Roll)
            scale(axes["pitch"]),    # chan2 (Pitch)
            scale(axes["throttle"]), # chan3 (Throttle)
            scale(axes["yaw"]),      # chan4 (Yaw)
            0, 0, 0, 0
        )

        print(f"RC → roll: {scale(axes['roll'])}, pitch: {scale(axes['pitch'])}, throttle: {scale(axes['throttle'])}, yaw: {scale(axes['yaw'])}")
        time.sleep(0.05)

if __name__ == '__main__':
    main()
