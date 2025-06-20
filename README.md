# Personal Immersion Tracker 

This project is a personal immersion tracking tool built with FastAPI, Supabase, and Streamlit. It fulfills the core requirements of the Keploy API Fellowship by implementing a custom API with 4+ endpoints, full CRUD functionality, and integration with a real database. Users can log time spent on various language immersion activities, update or delete their logs, and view statistics like total time by activity type. A simple Streamlit-based frontend is also provided for interacting with the API.

## Features

- Log immersion activities (type, duration, description, date)
- Retrieve all logs
- Filter total time by type
- Update existing logs
- Delete logs
- Streamlit-based frontend for easy interaction

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Streamlit
- **API Testing:** Swagger UI (`/docs`)

---

## API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| POST   | `/log`            | Add a new immersion log            |
| GET    | `/logs`           | Get all immersion logs             |
| GET    | `/time?type=xyz`  | Get total duration (optional type) |
| PUT    | `/log/{log_id}`   | Update a specific log              |
| DELETE | `/log/{log_id}`   | Delete a specific log              |

---

## Example Log Format

```json
{
  "type": "listening",
  "duration": 30,
  "description": "Watched anime",
  "date": "2025-06-19"
}
```

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/immersion-tracker.git
cd immersion-tracker
```
### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add a `.env` file

Create a `.env` file in the root directory and include:

```ini
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 5. Run the FastAPI backend

```bash
uvicorn main:app --reload
```
Then visit the API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 6. Run the Streamlit frontend

In a new terminal (with your virtual environment still activated):

```bash
streamlit run streamlit_app.py
```
Then open your browser and go to: [http://localhost:8501](http://localhost:8501)



