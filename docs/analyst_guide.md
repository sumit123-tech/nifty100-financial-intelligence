# Financial Intelligence Platform
## Analyst Guide

### Overview
This project provides financial analysis of NIFTY 100 companies using financial statements and ratio analysis.

### Features
- Financial Ratios
- Company Screener
- Portfolio Analytics
- Peer Comparison
- Capital Allocation
- Cashflow Intelligence
- FastAPI
- Streamlit Dashboard

### Dashboard
Run

streamlit run src/dashboard/app.py

### API

uvicorn src.api.main:app --reload

Available Endpoints

/company
/ratios
/pros-cons
/capital-allocation
/screener
...

### Reports
- Company Tearsheets
- Sector Reports
- Portfolio Summary

### Database

SQLite

database/nifty100.db

### Author

Sumit Banerjee