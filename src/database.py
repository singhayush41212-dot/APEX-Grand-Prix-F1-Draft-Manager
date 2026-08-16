import sqlite3
import hashlib
from pathlib import Path
from collections import Counter

DB_PATH = Path("f1_draft_game.db")

def init_db():
    """Initialize SQLite tables for Users and detailed Career Scores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Career Scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            team_name TEXT NOT NULL,
            driver1 TEXT NOT NULL,
            driver2 TEXT NOT NULL,
            car TEXT NOT NULL,
            principal TEXT NOT NULL,
            points INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            wins INTEGER NOT NULL,
            podiums INTEGER NOT NULL DEFAULT 0,
            wdc_won INTEGER NOT NULL DEFAULT 0,
            wcc_won INTEGER NOT NULL DEFAULT 0,
            races_run INTEGER NOT NULL DEFAULT 20,
            is_public INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Check for is_public column auto-migration
    cursor.execute("PRAGMA table_info(user_scores)")
    columns = [col[1] for col in cursor.fetchall()]
    if "is_public" not in columns:
        cursor.execute("ALTER TABLE user_scores ADD COLUMN is_public INTEGER NOT NULL DEFAULT 0")
        
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str):
    """Register a new user account."""
    if not username.strip() or not password.strip():
        return False, "Username and password cannot be empty."
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username.strip(), hash_password(password))
        )
        conn.commit()
        conn.close()
        return True, "Account created successfully! You are now logged in."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already taken. Please choose another."

def login_user(username: str, password: str):
    """Authenticate a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, {"id": user[0], "username": user[1]}
    return False, "Invalid username or password."

def save_user_score(user_id: int, team_name: str, driver1: str, driver2: str, car: str, principal: str, points: int, rank: int, wins: int, podiums: int, wdc_won: bool, wcc_won: bool, is_public: bool):
    """Save full season metrics to user's personal career profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_scores (user_id, team_name, driver1, driver2, car, principal, points, rank, wins, podiums, wdc_won, wcc_won, races_run, is_public)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 20, ?)
    """, (user_id, team_name, driver1, driver2, car, principal, points, rank, wins, podiums, 1 if wdc_won else 0, 1 if wcc_won else 0, 1 if is_public else 0))
    conn.commit()
    conn.close()

def get_user_career_stats(user_id: int):
    """Compile 'Your 24-0' career stats for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, team_name, driver1, driver2, car, principal, points, rank, wins, podiums, wdc_won, wcc_won, races_run, created_at, is_public
        FROM user_scores
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    runs = cursor.fetchall()
    conn.close()
    
    if not runs:
        return None
        
    seasons_played = len(runs)
    total_points = sum(r[6] for r in runs)
    avg_points = round(total_points / seasons_played, 1)
    highest_score = max(r[6] for r in runs)
    
    total_wins = sum(r[8] for r in runs)
    total_podiums = sum(r[9] for r in runs)
    total_races = sum(r[12] for r in runs)
    win_rate = round((total_wins / total_races) * 100, 1) if total_races > 0 else 0.0
    
    wdc_count = sum(r[10] for r in runs)
    wcc_count = sum(r[11] for r in runs)
    
    drivers_list = []
    cars_list = []
    principals_list = []
    for r in runs:
        if r[2]: drivers_list.append(r[2])
        if r[3]: drivers_list.append(r[3])
        if r[4]: cars_list.append(r[4])
        if r[5]: principals_list.append(r[5])
        
    most_used_driver = Counter(drivers_list).most_common(1)[0][0] if drivers_list else "N/A"
    most_used_car = Counter(cars_list).most_common(1)[0][0] if cars_list else "N/A"
    most_used_principal = Counter(principals_list).most_common(1)[0][0] if principals_list else "N/A"
    
    return {
        "seasons_played": seasons_played,
        "total_wins": total_wins,
        "win_rate": win_rate,
        "wdc_count": wdc_count,
        "wcc_count": wcc_count,
        "podium_count": total_podiums,
        "avg_points": avg_points,
        "highest_score": highest_score,
        "most_used_driver": most_used_driver,
        "most_used_car": most_used_car,
        "most_used_principal": most_used_principal,
        "history": runs
    }

def get_global_leaderboard():
    """Retrieve global top scores across players who opted in."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, s.team_name, (s.driver1 || ' / ' || s.driver2) as drivers, s.car, s.points, s.rank, s.wins
        FROM user_scores s
        JOIN users u ON s.user_id = u.id
        WHERE s.is_public = 1
        ORDER BY s.points DESC
        LIMIT 10
    """)
    records = cursor.fetchall()
    conn.close()
    return records