"""
Flask Application for Student Study Planner
Serves API routes and the main single-page dashboard.
"""
from flask import Flask, render_template, request, jsonify
from datetime import date, datetime
import database

app = Flask(__name__)

# Ensure tables are initialized on startup
database.init_db(seed_sample_data=True)

@app.route('/')
def index():
    """Render the dashboard UI."""
    return render_template('index.html')

# ==================== SUBJECT ROUTES ====================

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Retrieve all subjects with task counts and completion rates."""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            s.id, s.name, s.color, s.description, s.created_at,
            COUNT(t.id) AS total_tasks,
            SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) AS completed_tasks,
            SUM(CASE WHEN t.is_completed = 0 THEN 1 ELSE 0 END) AS pending_tasks,
            COALESCE(SUM(t.duration_mins), 0) AS total_duration_mins
        FROM subjects s
        LEFT JOIN tasks t ON s.id = t.subject_id
        GROUP BY s.id
        ORDER BY s.name ASC;
    """)
    rows = cursor.fetchall()
    subjects = []
    for r in rows:
        total = r['total_tasks']
        completed = r['completed_tasks'] or 0
        rate = round((completed / total * 100), 1) if total > 0 else 0
        subjects.append({
            'id': r['id'],
            'name': r['name'],
            'color': r['color'],
            'description': r['description'],
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': r['pending_tasks'] or 0,
            'completion_rate': rate,
            'total_duration_mins': r['total_duration_mins']
        })
    conn.close()
    return jsonify(subjects)

@app.route('/api/subjects', methods=['POST'])
def add_subject():
    """Create a new subject."""
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    color = data.get('color', '#6366f1').strip()
    description = data.get('description', '').strip()

    if not name:
        return jsonify({'error': 'Subject name is required.'}), 400

    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO subjects (name, color, description) VALUES (?, ?, ?);",
            (name, color, description)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Subject created successfully!', 'id': new_id}), 201
    except Exception as e:
        conn.close()
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({'error': f'Subject "{name}" already exists.'}), 409
        return jsonify({'error': str(e)}), 500

@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    """Delete a subject and all associated tasks."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE id = ?;", (subject_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Subject deleted successfully.'})

# ==================== TASK ROUTES ====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Retrieve tasks with optional filtering."""
    filter_type = request.args.get('filter', 'all')
    subject_id = request.args.get('subject_id')
    search = request.args.get('search', '').strip()

    today_str = date.today().isoformat()

    conn = database.get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            t.id, t.subject_id, t.title, t.description, 
            t.due_date, t.due_time, t.duration_mins, t.priority, 
            t.is_completed, t.completed_at, t.created_at,
            s.name AS subject_name, s.color AS subject_color
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE 1=1
    """
    params = []

    if subject_id and subject_id != 'all':
        query += " AND t.subject_id = ?"
        params.append(subject_id)

    if search:
        query += " AND (t.title LIKE ? OR t.description LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param])

    # Smart deadline filtering
    if filter_type == 'today':
        query += " AND t.due_date = ?"
        params.append(today_str)
    elif filter_type == 'upcoming':
        query += " AND t.due_date > ? AND t.is_completed = 0"
        params.append(today_str)
    elif filter_type == 'overdue':
        query += " AND t.due_date < ? AND t.is_completed = 0"
        params.append(today_str)
    elif filter_type == 'completed':
        query += " AND t.is_completed = 1"
    elif filter_type == 'pending':
        query += " AND t.is_completed = 0"

    query += " ORDER BY t.is_completed ASC, t.due_date ASC, t.due_time ASC;"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    tasks = []
    for r in rows:
        # Determine status label
        task_due = r['due_date']
        is_done = bool(r['is_completed'])
        
        if is_done:
            status = 'completed'
        elif task_due < today_str:
            status = 'overdue'
        elif task_due == today_str:
            status = 'today'
        else:
            status = 'upcoming'

        tasks.append({
            'id': r['id'],
            'subject_id': r['subject_id'],
            'subject_name': r['subject_name'],
            'subject_color': r['subject_color'],
            'title': r['title'],
            'description': r['description'],
            'due_date': r['due_date'],
            'due_time': r['due_time'],
            'duration_mins': r['duration_mins'],
            'priority': r['priority'],
            'is_completed': is_done,
            'completed_at': r['completed_at'],
            'status': status
        })

    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Create a new study task."""
    data = request.get_json() or {}
    subject_id = data.get('subject_id')
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    due_date = data.get('due_date', '').strip()
    due_time = data.get('due_time', '23:59').strip() or '23:59'
    duration_mins = int(data.get('duration_mins', 45))
    priority = data.get('priority', 'Medium')

    if not title or not subject_id or not due_date:
        return jsonify({'error': 'Title, subject, and due date are required.'}), 400

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (subject_id, title, description, due_date, due_time, duration_mins, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (subject_id, title, description, due_date, due_time, duration_mins, priority))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Task created successfully!', 'id': new_id}), 201

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    """Toggle a task between completed and pending."""
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_completed FROM tasks WHERE id = ?;", (task_id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404

    current_state = task['is_completed']
    new_state = 0 if current_state == 1 else 1
    completed_at = datetime.now().isoformat() if new_state == 1 else None

    cursor.execute("""
        UPDATE tasks 
        SET is_completed = ?, completed_at = ? 
        WHERE id = ?;
    """, (new_state, completed_at, task_id))
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Task status updated.',
        'is_completed': bool(new_state)
    })

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully.'})

# ==================== DASHBOARD STATS ====================

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Provide comprehensive statistics for summary cards and visual charts."""
    today_str = date.today().isoformat()
    conn = database.get_connection()
    cursor = conn.cursor()

    # Overall Counts
    cursor.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN is_completed = 0 AND due_date < ? THEN 1 ELSE 0 END) AS overdue,
            SUM(CASE WHEN due_date = ? THEN 1 ELSE 0 END) AS today_total,
            SUM(CASE WHEN due_date = ? AND is_completed = 1 THEN 1 ELSE 0 END) AS today_completed,
            COALESCE(SUM(duration_mins), 0) AS total_mins_planned,
            COALESCE(SUM(CASE WHEN is_completed = 1 THEN duration_mins ELSE 0 END), 0) AS total_mins_completed
        FROM tasks;
    """, (today_str, today_str, today_str))
    stats_row = cursor.fetchone()

    total = stats_row['total'] or 0
    completed = stats_row['completed'] or 0
    pending = stats_row['pending'] or 0
    overdue = stats_row['overdue'] or 0
    today_total = stats_row['today_total'] or 0
    today_completed = stats_row['today_completed'] or 0
    total_mins_planned = stats_row['total_mins_planned'] or 0
    total_mins_completed = stats_row['total_mins_completed'] or 0

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0
    today_completion_rate = round((today_completed / today_total * 100), 1) if today_total > 0 else 0

    # Subject breakdown for Chart.js
    cursor.execute("""
        SELECT 
            s.name, s.color,
            COUNT(t.id) AS total_tasks,
            SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) AS completed_tasks,
            SUM(CASE WHEN t.is_completed = 0 THEN 1 ELSE 0 END) AS pending_tasks
        FROM subjects s
        LEFT JOIN tasks t ON s.id = t.subject_id
        GROUP BY s.id
        ORDER BY total_tasks DESC;
    """)
    subject_rows = cursor.fetchall()
    subject_chart_data = []
    for sr in subject_rows:
        subject_chart_data.append({
            'name': sr['name'],
            'color': sr['color'],
            'total': sr['total_tasks'],
            'completed': sr['completed_tasks'] or 0,
            'pending': sr['pending_tasks'] or 0
        })

    conn.close()

    return jsonify({
        'total_tasks': total,
        'completed_tasks': completed,
        'pending_tasks': pending,
        'overdue_tasks': overdue,
        'today_total': today_total,
        'today_completed': today_completed,
        'completion_rate': completion_rate,
        'today_completion_rate': today_completion_rate,
        'study_hours_planned': round(total_mins_planned / 60.0, 1),
        'study_hours_completed': round(total_mins_completed / 60.0, 1),
        'subjects': subject_chart_data
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🎓 Student Study Planner is running!")
    print("👉 Open your browser at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
