"""
Main App
author: Marco Aldana

to run from console, type:
    system('uvicorn main:app --reload')
"""
import uvicorn
from project import app

if __name__ == '__main__':
    app.title = "CardsGame"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
