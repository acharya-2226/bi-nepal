"""
state.py  -  In-memory cache shared across routes.
Source of truth is SQLite (data/app.db); this dict is refreshed
from DB at startup and after each upload.
"""

store = {
    "inv":   None,
    "sales": None,
    "purch": None,
    "exp":   None,
    "vars":  None,
    "ready": False,
}
