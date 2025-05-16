from pymavlink import mavutil

# Подключаемся к тому же порту, что и SITL
conn = mavutil.mavlink_connection('udp:127.0.0.1:14550')
conn.wait_heartbeat()
print("Connected to SITL")

while True:
    msg = conn.recv_match(blocking=True)
    if msg and msg.get_type() == "RC_CHANNELS_OVERRIDE":
        print("[LOG] RC_OVERRIDE RECEIVED BY SITL:", msg.to_dict())
