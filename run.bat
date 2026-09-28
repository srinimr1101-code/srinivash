@echo off
if not exist env python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
if not exist .env copy .env.example .env
python run.py
