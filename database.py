"""
Database module for Student Study Planner
Handles SQLite connection, schema creation, migrations, and seed data.
"""
import sqlite3
import os
from datetime import date, datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'study_planner.db')

def get_connection():
    """Get a database connection with dictionary-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(seed_sample_data=True):
    """Initialize database tables and optionally seed realistic sample data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Subjects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color TEXT NOT NULL DEFAULT '#6366f1',
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT NOT NULL,
        due_time TEXT DEFAULT '23:59',
        duration_mins INTEGER DEFAULT 45,
        priority TEXT DEFAULT 'Medium',
        is_completed INTEGER DEFAULT 0,
        completed_at TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # Seed initial subjects and tasks if table is empty
    if seed_sample_data:
        cursor.execute("SELECT COUNT(*) FROM subjects;")
        count = cursor.fetchone()[0]
        if count == 0:
            seed_data(conn)

    conn.close()

def seed_data(conn):
    """Seed sample academic subjects and tasks so the user sees a rich UI on day 1."""
    cursor = conn.cursor()
    today_str = date.today().isoformat()
    yesterday_str = (date.today() - timedelta(days=1)).isoformat()
    tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
    in_3_days_str = (date.today() + timedelta(days=3)).isoformat()

    sample_subjects = [
        ("Data Structures & Algorithms", "#4f46e5", "Binary Trees, Dynamic Programming, Graphs"),
        ("Computer Networks", "#0ea5e9", "TCP/IP, OSI Layers, Routing Protocols"),
        ("Database Management Systems", "#10b981", "SQL Queries, Normalization, Indexing"),
        ("Mathematics for CS", "#f59e0b", "Discrete Mathematics, Linear Algebra, Probability")
    ]

    cursor.executemany(
        "INSERT INTO subjects (name, color, description) VALUES (?, ?, ?);",
        sample_subjects
    )
    conn.commit()

    # Retrieve subject IDs
    cursor.execute("SELECT id, name FROM subjects;")
    subj_map = {row['name']: row['id'] for row in cursor.fetchall()}

    sample_tasks = [
        # Today tasks
        (subj_map["Data Structures & Algorithms"], "Solve 3 LeetCode Binary Tree Problems", "Inorder, Preorder traversal & maximum depth", today_str, "18:00", 60, "High", 1, datetime.now().isoformat()),
        (subj_map["Data Structures & Algorithms"], "Revise Dynamic Programming Memoization", "Knapsack and Fibonacci patterns", today_str, "21:00", 45, "High", 0, None),
        (subj_map["Computer Networks"], "Read Chapter 4: Transport Layer", "Understand TCP 3-way handshake and UDP differences", today_str, "16:30", 50, "Medium", 0, None),
        
        # Overdue task
        (subj_map["Mathematics for CS"], "Complete Assignment on Graph Theory", "Problems 1 to 10 from syllabus module 3", yesterday_str, "23:59", 90, "High", 0, None),
        
        # Upcoming tasks
        (subj_map["Database Management Systems"], "Practice SQL Joins & Subqueries", "Write complex queries using GROUP BY and HAVING", tomorrow_str, "19:00", 45, "Medium", 0, None),
        (subj_map["Database Management Systems"], "Study B-Tree and Hash Indexing", "Prepare short notes for lab viva", in_3_days_str, "20:00", 40, "Low", 0, None),
        (subj_map["Computer Networks"], "Configure Subnetting in Packet Tracer", "Practice /24 and /26 CIDR subnet masks", in_3_days_str, "17:00", 60, "Medium", 0, None)
    ]

    cursor.executemany("""
    INSERT INTO tasks (subject_id, title, description, due_date, due_time, duration_mins, priority, is_completed, completed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, sample_tasks)

    conn.commit()
