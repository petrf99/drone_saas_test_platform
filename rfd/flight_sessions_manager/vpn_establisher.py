from tech_utils.logger import init_logger
logger = init_logger("RFD_FlightSessionsManagerVPN")

def setup_vpn(mission_id):
    print(f"[MOCK] Setting up Tailscale VPN for mission {mission_id}")
