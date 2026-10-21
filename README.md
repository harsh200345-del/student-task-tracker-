# 🎓 Student Study Planner

A modern, full-stack **Student Study Planner & Daily Goal Tracker** built with **Python (Flask)**, **SQLite**, and modern web technologies (**Tailwind CSS**, **Lucide Icons**, and **Chart.js**). 

Organize subjects, schedule daily study sessions, track deadlines, monitor completion rates, and stay on top of your academic goals with an intuitive real-time dashboard.

---

## ✨ Features

- **📚 Subject Management:** Create academic subjects with custom color tags and descriptions.
- **📝 Daily Study Tasks:** Add tasks with estimated study duration (mins), priority levels (Low, Medium, High 🔥), and notes.
- **⏰ Smart Deadline Tracking:** Automated categorization for **Due Today**, **Upcoming**, and **Overdue** tasks.
- **✅ Instant Progress Tracking:** One-click task completion checkbox with instant feedback and animated status updates.
- **🎯 Today's Focus View:** Quick filter to isolate tasks that must be finished today.
- **📊 Interactive Dashboard & Analytics:**
  - Real-time KPI metric cards (Total tasks, Pending, Completion rate %, Study hours).
  - **Donut Chart:** Overall status distribution (Completed, Pending, Overdue).
  - **Bar Chart:** Subject-wise workload breakdown (Completed vs. Pending tasks).
- **💾 Persistent SQLite Database:** Zero configuration required; data is automatically stored in `study_planner.db` with sample data seeded on the first launch.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **Database** | SQLite3 (Built-in, zero setup) |
| **Frontend** | HTML5, JavaScript (ES6+ Fetch API), Tailwind CSS |
| **Icons & Charts** | Lucide Icons, Chart.js |

---

## 📂 Project Structure

```text
student-study-planner/
│
├── app.py                 # Main Flask server and REST API routes
├── database.py            # SQLite schema initialization and seed data
├── requirements.txt       # Project dependencies (Flask)
├── run.bat                # 1-Click launcher for Windows
├── .gitignore             # Standard Git ignore file
├── README.md              # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom checkboxes, badges, and animations
│   └── js/
│       └── app.js         # Client-side state, API calls, and Chart.js rendering
│
└── templates/
    └── index.html         # Responsive dashboard user interface
```

---

## 🚀 Quick Start (Run Locally)

### Option 1: One-Click Launch (Windows)
Simply double-click the **`run.bat`** file in the project folder. It will install dependencies if needed, start the local server, and open your browser automatically.

### Option 2: Terminal / Command Line

1. **Clone or navigate to the project directory:**
   ```bash
   cd student-study-planner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   python app.py
   ```

4. **Open in your browser:**
   ```text
   http://127.0.0.1:5000
   ```

---

## 🌐 How to Upload to GitHub

Follow these steps to publish this project to your GitHub profile:

### Method A: Using Git CLI

1. **Create a new repository on GitHub:**
   - Go to [github.com/new](https://github.com/new).
   - Enter repository name: `student-study-planner`.
   - Leave it **Public**, and **do not** initialize with README or .gitignore (we already have them).
   - Click **Create repository**.

2. **Run the following commands in PowerShell or Command Prompt inside your project folder:**
   ```bash
   # Initialize git repository
   git init

   # Stage all files
   git add .

   # Commit files
   git commit -m "Initial commit: Student Study Planner full-stack project"

   # Rename branch to main
   git branch -M main

   # Link your remote repository (replace with your GitHub URL)
   git remote add origin https://github.com/<YOUR-USERNAME>/student-study-planner.git

   # Push to GitHub
   git push -u origin main
   ```

### Method B: Using GitHub Desktop (Beginner Friendly)
1. Download & open [GitHub Desktop](https://desktop.github.com/).
2. Click **File** > **Add Local Repository...**
3. Browse and select the `student-study-planner` directory.
4. If prompted to create a repository, click **Create a repository here**.
5. Click **Publish repository** to push it directly to your GitHub account!

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | `GET` | Render the study planner dashboard |
| `GET /api/subjects` | `GET` | Retrieve all subjects with completion statistics |
| `POST /api/subjects` | `POST` | Add a new subject (`{ name, color, description }`) |
| `DELETE /api/subjects/<id>` | `DELETE` | Delete a subject and its associated tasks |
| `GET /api/tasks` | `GET` | Get tasks with optional filters (`filter`, `subject_id`, `search`) |
| `POST /api/tasks` | `POST` | Create a new study task |
| `PUT /api/tasks/<id>/toggle` | `PUT` | Toggle task completion status |
| `DELETE /api/tasks/<id>` | `DELETE` | Delete a study task |
| `GET /api/dashboard/stats` | `GET` | Get overall summary metrics and chart datasets |

---

## 🎓 College Viva / Project Presentation Talking Points

- **Why SQLite?** Zero-configuration, serverless, and portable; ideal for local desktop and embedded web applications without running a separate database server.
- **RESTful Architecture:** Separation of concerns between backend API endpoints and a dynamic Single Page Application (SPA) frontend.
- **Responsive Design:** Utilizes Tailwind utility-first styling for consistent UI across mobile and desktop screens.
- **Performance:** Asynchronous data fetching via modern JavaScript `fetch()` API with zero page refreshes during task completion toggles.

---

## 📜 License
This project is open-source and free to use for educational and personal purposes under the MIT License.
