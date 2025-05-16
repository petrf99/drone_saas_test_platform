import pygame
import socket
import json
import uuid
import time

from tech_utils.logger import init_logger
logger = init_logger("RCClient")


from rc_client.config import UDP_SEND_LOG_DELAY, FREQUENCY, RC_CHANNELS_DEFAULTS, RFD_IP, RFD_PORT


# === Генерация уникального session_id ===
session_id = str(uuid.uuid4())


# === Инициализация pygame ===
from rc_client.gui import pygame_init, start_screen
screen, clock = pygame_init()

username, password, controller_type = start_screen(screen, clock)
logger.info(f"User '{username}' selected controller '{controller_type}'")

rc_input = get_rc_input(controller_type)


# === Создание UDP-сокета ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

last_log_time = 0
def send_rc_frame(sock, rc_state, source):
    global last_log_time
    rc_frame = {
        "timestamp": time.time(),
        "session_id": session_id,
        "source": source,
        "channels": rc_state
    }
    json_data = json.dumps(rc_frame).encode('utf-8')

    try:
        sock.sendto(json_data, (RFD_IP, RFD_PORT))
        current_time = time.time()
        if current_time - last_log_time >= UDP_SEND_LOG_DELAY:
            logger.info(f"Frame sent to {RFD_IP}:{RFD_PORT}\nJSON:\n{rc_frame}\n")
            last_log_time = current_time
    except Exception as e:
        logger.error(f"Exception occurred while sending UDP: {e}\n", exc_info=True)



# === Обработка ввода и RC-логика ===
from rc_client.inputs import get_rc_input
rc_input = get_rc_input("keyboard")



# === Главный цикл ===
rc_state = RC_CHANNELS_DEFAULTS.copy()

logger.info(f"RC Session ID: {session_id}\n")
logger.info(f"Sending RC frames to {RFD_IP}:{RFD_PORT}\n")

running = True
while running:
    clock.tick(FREQUENCY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rc_state = rc_input.process_event(event, rc_state)

    rc_state = rc_input.read_frame(rc_state)

    send_rc_frame(sock, rc_state, "keyboard")



# отправить финальный neutral frame (disarm дрона при выходе)
neutral = RC_CHANNELS_DEFAULTS.copy()
neutral["ch5"] = 1000
neutral["ch6"] = 1000

send_rc_frame(sock, neutral, "keyboard")

pygame.quit()
