# KGEN Python Backend

Python backend service for dataset anonymization based on **K-Anonymity (KGEN)**.  
This project is a simplified and modern re-implementation of an existing Java-based KGEN backend, designed for easy integration with web frontends.

The service exposes a REST API built with Flask and currently supports the **OLA algorithm** for finding minimal generalization strategies that satisfy k-anonymity constraints.  
The architecture is designed to be extensible and support additional anonymization algorithms in the future.

---

## 🚀 Features

- REST API for dataset anonymization  
- K-Anonymity implementation  
- OLA algorithm  
- CSV-like dataset support (JSON input)  
- Extensible algorithm architecture  
- CORS enabled for frontend integration  
- Simple and readable Python codebase  

---

## 📦 Tech Stack

- Python 3.10+
- Flask
- Flask-CORS

---

## 📥 Installation

```bash
git clone https://github.com/<your-username>/kgen-python-backend.git
cd kgen-python-backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
