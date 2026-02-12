import os

class Config:
    SECRET_KEY = "dev-secret-key"  # change later

    SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://appuser:Hemmelig123!@10.0.0.20:1433/Todoapp"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False