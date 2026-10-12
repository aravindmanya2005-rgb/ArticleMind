import hashlib
import hmac
import os

# ============================================================
# SECURE PASSWORD HASHING UTILITIES (PBKDF2-HMAC-SHA256)
# ============================================================

def generate_salt():
    """Generate a random 16-byte salt."""
    return os.urandom(16)

def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
    Returns (salt_hex, hash_hex).
    """
    if salt is None:
        salt = generate_salt()
    
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex(), key.hex()

def verify_password(stored_salt_hex: str, stored_hash_hex: str, password_to_check: str) -> bool:
    """Verify a password against stored salt and hash."""
    try:
        salt = bytes.fromhex(stored_salt_hex)
        _, check_hash_hex = hash_password(password_to_check, salt)
        return hmac.compare_digest(stored_hash_hex, check_hash_hex)
    except Exception:
        return False


# ============================================================
# PRE-COMPUTED DEFAULT ACCOUNTS & CREDENTIAL STORE
# ============================================================

# Pre-computed salt and hash for default password 'admin123'
DEFAULT_ADMIN_SALT = "a1b2c3d4e5f67890123456789abcdef0"
_, DEFAULT_ADMIN_HASH = hash_password("admin123", bytes.fromhex(DEFAULT_ADMIN_SALT))

# Pre-computed salt and hash for researcher password 'research123'
DEFAULT_RESEARCH_SALT = "f0e9d8c7b6a543210987654321fedcba"
_, DEFAULT_RESEARCH_HASH = hash_password("research123", bytes.fromhex(DEFAULT_RESEARCH_SALT))

def get_user_database():
    """
    Load user credentials. Allows environment variable overrides
    (ARTICLEMIND_ADMIN_PASS, ARTICLEMIND_RESEARCH_PASS) for production deployment.
    """
    # Check for custom admin password override in environment
    env_admin_pass = os.getenv("ARTICLEMIND_ADMIN_PASS")
    if env_admin_pass:
        admin_salt, admin_hash = hash_password(env_admin_pass)
    else:
        admin_salt, admin_hash = DEFAULT_ADMIN_SALT, DEFAULT_ADMIN_HASH

    env_research_pass = os.getenv("ARTICLEMIND_RESEARCH_PASS")
    if env_research_pass:
        res_salt, res_hash = hash_password(env_research_pass)
    else:
        res_salt, res_hash = DEFAULT_RESEARCH_SALT, DEFAULT_RESEARCH_HASH

    return {
        "admin": {
            "display_name": "Administrator",
            "role": "Lead Researcher",
            "salt": admin_salt,
            "hash": admin_hash,
        },
        "researcher": {
            "display_name": "AI Researcher",
            "role": "Domain Specialist",
            "salt": res_salt,
            "hash": res_hash,
        }
    }


# ============================================================
# AUTHENTICATION API
# ============================================================

def authenticate_user(username_input: str, password_input: str) -> tuple[bool, str, dict]:
    """
    Authenticate a user by username and password.
    Returns (success_boolean, message, user_profile_dict).
    """
    if not username_input or not password_input:
        return False, "Username and password are required.", {}

    username_clean = username_input.strip().lower()
    users = get_user_database()

    if username_clean not in users:
        return False, "Incorrect username or password.", {}

    user_info = users[username_clean]
    is_valid = verify_password(
        user_info["salt"],
        user_info["hash"],
        password_input
    )

    if is_valid:
        profile = {
            "username": username_clean,
            "display_name": user_info["display_name"],
            "role": user_info["role"]
        }
        return True, "Login successful!", profile
    else:
        return False, "Incorrect username or password.", {}
