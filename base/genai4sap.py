import requests
#import pandas as pd 
from utilities import (BACKEND_URL, ADMIN_API_KEY, GENERATE_SQL, RUN_SQL, GENERATE_GRAPH)

def call_generate_sql(user_question):
    """Generates SQL for a given question and database."""
    endpoint = f"{BACKEND_URL}{GENERATE_SQL}?question='{user_question}'"
    headers = {"ADMIN-API-KEY": f"{ADMIN_API_KEY}"}
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        exception = (f"Error generating SQL: {e}")
        return exception
    
def run_sql(id, sql):
    """Fetch Results for generated sql"""
    endpoint = f"{BACKEND_URL}{RUN_SQL}?id={id}&sql='{sql}'"
    headers = {"ADMIN-API-KEY": f"{ADMIN_API_KEY}"}
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        exception = (f"Error fetching the results: {e}")
        return exception