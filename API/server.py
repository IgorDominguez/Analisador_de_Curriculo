# python -m uvicorn server:app --reload

from fastapi import FastAPI
from routes.upload_send import router as upload_send_router
from routes.upload_get import router as upload_get_router
from routes.upload_resume import router as upload_resume_router
from routes.upload_clear import router as upload_clear_router
from routes.upload_get_analytics import router as upload_get_analytics_router
from routes.upload_clear_analytics import router as upload_clear_analytics_router
from routes.chat_send import router as chat_send_router
from routes.chat_clear import router as chat_clear_router
from routes.chat_get import router as chat_get_router

app = FastAPI()

# UPLOAD PDF
app.include_router(upload_send_router)
app.include_router(upload_get_router)
app.include_router(upload_resume_router)
app.include_router(upload_clear_router)
app.include_router(upload_get_analytics_router)
app.include_router(upload_clear_analytics_router)

# CHAT
app.include_router(chat_send_router)
app.include_router(chat_clear_router)
app.include_router(chat_get_router)