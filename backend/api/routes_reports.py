from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import text
import uuid
from datetime import datetime

from models.database import SessionLocal

router = APIRouter()


class FieldReport(BaseModel):
    report_type: str
    title: str
    description: str
    lat: float
    lon: float
    severity: str = "moderate"


@router.post("/submit")
async def submit_report(report: FieldReport):
    db = SessionLocal()
    try:
        report_id = f"rpt-{uuid.uuid4().hex[:8]}"
        db.execute(
            text("INSERT INTO field_reports (id, report_type, title, description, lat, lon, severity, status, created_at) "
                 "VALUES (:id, :type, :title, :desc, :lat, :lon, :sev, 'open', :now)"),
            {"id": report_id, "type": report.report_type, "title": report.title,
             "desc": report.description, "lat": report.lat, "lon": report.lon,
             "sev": report.severity, "now": datetime.utcnow().isoformat()},
        )
        db.commit()
        return {"status": "received", "report_id": report_id}
    finally:
        db.close()


@router.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...), report_id: str = Form(...)):
    return {"status": "uploaded", "filename": file.filename, "report_id": report_id}


@router.get("/recent")
async def get_recent_reports():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT id, report_type, title, description, lat, lon, severity, status, created_at "
                 "FROM field_reports ORDER BY created_at DESC LIMIT 50")
        ).fetchall()
        return {"reports": [
            {"id": r[0], "type": r[1], "title": r[2], "description": r[3],
             "lat": r[4], "lon": r[5], "severity": r[6], "status": r[7], "created_at": str(r[8])}
            for r in rows
        ], "count": len(rows)}
    finally:
        db.close()
