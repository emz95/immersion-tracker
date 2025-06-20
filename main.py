from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = FastAPI()

class ImmersionLog(BaseModel):
    type: str
    duration: int
    description: str

@app.post("/log")
def create_log(log: ImmersionLog):
    res = supabase.table("immersion_logs").insert(log.dict()).execute()
    return res.data

@app.get("/logs")
def return_log():
    res = supabase.table("immersion_logs").select("*").execute()
    return res.data

@app.get("/time")
def get_time(selected_type: str):
    if selected_type == "All":
        res = supabase.table("immersion_logs").select("duration").execute()
    else:
        res = supabase.table("immersion_logs").select("duration").eq("type", selected_type).execute()
    total = sum (log["duration"] for log in res.data)
    return total

@app.put("/log/{log_id}")
def update_log(log_id: str, updated_data: dict):
    res = supabase.table("immersion_logs").update(updated_data).eq("id", log_id).execute()
    return res

@app.delete("/log/{log_id}")
def delete_log(log_id: str):
    res = supabase.table("immersion_logs").delete().eq("id", log_id).execute()
    return res