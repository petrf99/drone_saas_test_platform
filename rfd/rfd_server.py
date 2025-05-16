from flask import Flask, request, jsonify

from rfd.flight_sessions_manager.endpoints import validate_token
from rfd.flight_tasks_manager.endpoints import receive_flight_task

app = Flask(__name__)

from apscheduler.schedulers.background import BackgroundScheduler
from rfd.flight_sessions_manager.token_manager import deactivate_expired_tokens
from rfd.flight_tasks_manager.ftasks_manager import alert_pending_tasks

scheduler = BackgroundScheduler()
scheduler.add_job(deactivate_expired_tokens, "interval", seconds=60)
scheduler.add_job(alert_pending_tasks, "interval", hours=1)
scheduler.start()

app.add_url_rule("/validate-token", view_func=validate_token, methods=["POST"])
app.add_url_rule("/flight-task-receive", view_func=receive_flight_task, methods=["POST"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
