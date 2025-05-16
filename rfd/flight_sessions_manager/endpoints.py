# rfd_server.py
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

from tech_utils.logger import init_logger
logger = init_logger("RFD_MATokensManager")

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
                    SELECT id, is_active_flg, expires_at
                    FROM grfp_auth_tokens
                    WHERE token = %s
                    LIMIT 1
                """, (token,))
                row = cur.fetchone()

                if not row:
                    logger.info(f"Token {token} not found in DB")
                    return jsonify({"status": "error", "reason": "Invalid token"}), 403

                token_id, is_active, expires_at = row

                if not is_active or expires_at < datetime.utcnow():
                    logger.info(f"Token {token} is inactive or expired")
                    return jsonify({"status": "error", "reason": "Token expired or inactive"}), 403

                # Сгенерировать и записать session_id
                session_id = str(uuid.uuid4())
                cur.execute("""
                    UPDATE grfp_auth_tokens
                    SET session_id = %s
                    WHERE id = %s
                """, (session_id, token_id))

                logger.info(f"Token {token} validation succeeded. Session-id: {session_id}")
                return jsonify({"status": "ok", "session_id": session_id})

    except Exception as e:
        logger.error(f"Exception in validate_token: {e}", exc_info=True)
        return jsonify({"status": "error", "reason": "Internal server error"}), 500

