import os

# === Настройки ===
RFD_IP = os.getenv("RFD_IP")       # адрес сервера RFD
RFD_PORT = int(os.getenv("RFD_PORT"))           # порт приёма RC-команд

# === Константы каналов ===
RC_CHANNELS_DEFAULTS = {
    "ch1": 1500,  # roll (← →)
    "ch2": 1500,  # pitch (↑ ↓)
    "ch3": 1000,  # throttle (W/S)
    "ch4": 1500,  # yaw (A/D)
    "ch5": 1000,  # arm/disarm (Space)
    "ch6": 1000   # aux (Shift)
}

STEP_ANALOG = 20      # шаг изменения каналов
LIMIT_MIN = 1000
LIMIT_MAX = 2000

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

FREQUENCY = 20

UDP_SEND_LOG_DELAY = 1