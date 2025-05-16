from tech_utils.logger import init_logger
logger = init_logger("RFD_FlightTaskManager")

from tech_utils.db import get_conn
from tech_utils.email_utils import send_email

def alert_pending_tasks():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT task_id, location, time_window, drone_type, created_at
                    FROM grfp_flight_tasks
                    WHERE status = 'new'
                """)
                rows = cur.fetchall()

        if rows:
            body = "Pending Flight Tasks:\n\n"
            for r in rows:
                body += f"ID: {r[0]}, Loc: {r[1]}, Time: {r[2]}, Drone: {r[3]}, Created: {r[4]}\n"

            send_email("[GRFP] Hourly Alert: New Tasks", body)

    except Exception as e:
        logger.error(f"Error sending hourly task alert: {e}")
