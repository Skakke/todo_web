import os

class Config:
    SECRET_KEY = "dev-secret-key"  # change later

    SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://appuser:Hemmelig123!@10.0.0.20:1433/Todoapp"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False