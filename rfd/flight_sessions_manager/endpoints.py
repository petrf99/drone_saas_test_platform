# rfd_server.py
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

from tech_utils.logger import init_logger
logger = init_logger("RFD_FlightSessionsManager")

from tech_utils.db import get_conn

def validate_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"status": "error", "reason": "Missing token"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                # Проверим токен
                cur.execute("""
                    SELECT id, is_active_flg, expires_at, session_id
                    FROM grfp_sm_auth_tokens
                    WHERE token = %s
                    LIMIT 1
                """, (token,))
                row = cur.fetchone()

                if not row:
                    logger.info(f"Token {token} not found in DB")
                    return jsonify({"status": "error", "reason": "Invalid token"}), 403

                token_id, is_active, expires_at, session_id = row

                if not is_active or expires_at < datetime.utcnow():
                    logger.info(f"Token {token} is inactive or expired")
                    return jsonify({"status": "error", "reason": "Token expired or inactive"}), 403

                logger.info(f"Token {token} validation succeeded. Session-id: {session_id}")
                return jsonify({"status": "ok", "session_id": session_id})

    except Exception as e:
        logger.error(f"Exception in validate_token {token}: {e}", exc_info=True)
        return jsonify({"status": "error", "reason": "Internal server error"}), 500
