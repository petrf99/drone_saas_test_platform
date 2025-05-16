import os
import hashlib
import uuid
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

from tech_utils.logger import init_logger
logger = init_logger("RFD_MATokensManager")

load_dotenv()

from tech_utils.db import get_conn

TOKEN_EXPIRE_TMP = int(os.getenv("TOKEN_EXPIRE_TMP", 300))

def generate_token():
    raw = uuid.uuid4().hex
    token = hashlib.md5(raw.encode()).hexdigest()[:10]
    return token

def create_token():
    token = generate_token()
    now = datetime.utcnow()
    expires = now + timedelta(seconds=TOKEN_EXPIRE_TMP)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO grfp_auth_tokens 
                (token, session_id, is_active_flg, created_at, expires_at)
                VALUES (%s, %s, TRUE, %s, %s)
            """, (token, None, now, expires))
    logger.info("Tokens created successfully\n")
    return token

def deactivate_expired_tokens():
    try:
        now = datetime.utcnow()
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE grfp_auth_tokens
                    SET is_active_flg = FALSE
                    WHERE expires_at <= %s AND is_active_flg = TRUE
                """, (now,))
            logger.info("Deactivation of expired tokens succeed\n")
    except Exception as e:
        logger.error(f"[!] Error in deactivate_expired_tokens: {e}\n")


if __name__ == "__main__":
    print(create_token())
    print(create_token())