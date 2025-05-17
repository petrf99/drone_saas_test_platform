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

                logger.info(f"Token {token} validation succeeded. Token_id: {token_id}. Session-id: {session_id}")
                return jsonify({"status": "ok", "session_id": session_id})

    except Exception as e:
        logger.error(f"Exception in validate_token {token}: {e}", exc_info=True)
        return jsonify({"status": "error", "reason": "Internal server error"}), 500




from rfd.flight_sessions_manager.vpn_establisher import setup_vpn
from rfd.flight_sessions_manager.token_manager import create_token

def gcs_ready():
    data = request.get_json()
    mission_id = data.get("mission_id")

    if not mission_id:
        return jsonify({"status": "error", "reason": "Missing mission_id"}), 400

    try:
        session_id = str(uuid.uuid4())
        token = create_token(mission_id, session_id)

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT status
                    FROM grfp_missions
                    WHERE mission_id = %s
                            """, (mission_id,))
                
                status = cur.fetchone()
                if status:
                    status = status[0]
                else:
                    logger.error(f"Mission {mission_id} not found")
                    return jsonify({"status": "error", "reason": "mission not found"}), 400

                if status != 'in progress':
                    logger.error(f"Mission {mission_id} is not in progress")
                    return jsonify({"status": "error", "reason": "mission is not in progress"}), 400

                # Обновим миссию
                cur.execute("""
                    UPDATE grfp_missions
                    SET status = 'ready',
                        updated_at = %s
                    WHERE mission_id = %s
                """, (datetime.utcnow(), mission_id))
                
                # Write session to db
                cur.execute("""
                    INSERT INTO grfp_sm_sessions 
                            (session_id, status)
                    VALUES (%s, 'new')
                """, (session_id, ))
                conn.commit()

        # Мокаем tailscale настройку
        setup_vpn(mission_id)

        logger.info(f"GCS for mission {mission_id} marked as ready. Session: {session_id}")
        return jsonify({
            "status": "ok",
            "session_id": session_id
        })

    except Exception as e:
        logger.exception(f"GCS-ready failed with exception {e}")
        return jsonify({"status": "error", "reason": "internal server error"}), 500