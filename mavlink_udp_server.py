# mavlink_udp_server.py
from pymavlink import mavutil

# Ждём соединения на порту 14550
print("Ожидание MAVLink-соединения на порту 14550...")
master = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Ждём первого пакета (heartbeat)
master.wait_heartbeat()
print("Подключение установлено с системой ID %d, комп ID %d" % (master.target_system, master.target_component))

while True:
    msg = master.recv_match(blocking=True)
    if msg:
        print(f"[{msg.get_type()}] {msg.to_dict()}")
