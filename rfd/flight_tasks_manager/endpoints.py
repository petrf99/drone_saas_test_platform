from flask import Flask, request, jsonify

from tech_utils.db import get_conn
from tech_utils.email_utils import send_email

from tech_utils.logger import init_logger
logger = init_logger("RFD_FlightTaskManager")

def receive_flight_task():
    data = request.get_json()
    required = ["task_id", "location", "time_window", "drone_type"]

    if not all(k in data for k in required):
        return jsonify({"status": "error", "reason": "Missing parameters"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO grfp_flight_tasks (task_id, location, time_window, drone_type)
                    VALUES (%s, %s, %s, %s)
                """, (data["task_id"], data["location"], data["time_window"], data["drone_type"]))

        # Email alert
        subject = f"[GRFP] New Flight Task: {data['task_id']}"
        body = "\n".join([f"{k}: {data[k]}" for k in required])
        send_email(subject, body)

        return jsonify({"status": "ok"})

    except Exception as e:
        logger.error(f"Error creating flight task: {e}", exc_info=True)
        return jsonify({"status": "error", "reason": "DB insert error"}), 500
