from pymavlink import mavutil

print("Запуск...")

sitl_conn = mavutil.mavlink_connection(
    'udpin:127.0.0.1:14550',
    source_system=42,
    source_component=100
)
client_conn = mavutil.mavlink_connection('udp:0.0.0.0:14552')  # отдельный порт для клиента

sitl_conn.wait_heartbeat()
sitl_conn.mav.param_set_send(1,0,
    b'ARMING_CHECK',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_INT32
)

sitl_conn.mav.command_long_send(
    1,#sitl_conn.target_system,
    0,#sitl_conn.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,     # confirmation
    1,     # 1 = arm, 0 = disarm
    0, 0, 0, 0, 0, 0
)
print("Sent ARM command to drone")
ack = sitl_conn.recv_match(type='COMMAND_ACK', blocking=True)
print("ACK:", ack.to_dict())


#client_conn.wait_heartbeat()
print(f"SITL: heartbeat от system {sitl_conn.target_system}, {sitl_conn.target_component}")

while True:
    sitl_conn.mav.heartbeat_send(
            type=mavutil.mavlink.MAV_TYPE_GCS,
            autopilot=mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            base_mode=0,
            custom_mode=0,
            system_status=mavutil.mavlink.MAV_STATE_ACTIVE
        )

    msg = sitl_conn.recv_match(blocking=False)
    if msg:
        pass#print(f"[SITL] {msg.get_type()}")

    msg2 = client_conn.recv_match(blocking=False)
    if msg2:
        #print(f"[CLIENT] {msg2.get_type()} - {msg2.to_dict()}")


        # Если хочешь переслать RC_OVERRIDE в SITL напрямую:
        if msg2.get_type() == "RC_CHANNELS_OVERRIDE":
            sitl_conn.mav.rc_channels_override_send(
                1, #sitl_conn.target_system,
                0, #sitl_conn.target_component,
                *[
                    getattr(msg2, f'chan{i+1}_raw', 0)
                    for i in range(8)
                ]
            )

