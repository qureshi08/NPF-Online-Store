import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Get DATABASE_URL and handle Railway's postgres:// format
    database_url = os.environ.get('DATABASE_URL', '')
    print(f"DEBUG: DATABASE_URL = {database_url[:50]}..." if database_url else "DEBUG: DATABASE_URL is empty!")
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///npf_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    print(f"DEBUG: Using database: {SQLALCHEMY_DATABASE_URI[:50]}...")
