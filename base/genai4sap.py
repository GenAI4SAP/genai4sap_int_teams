import requests
from utilities import (BACKEND_URL, ADMIN_API_KEY, GENERATE_SQL, RUN_SQL, GENERATE_GRAPH)
import plotly.io as pio
import base64

def call_generate_sql(user_question):
    #Generates SQL for a given question and database.
    endpoint = f"{BACKEND_URL}{GENERATE_SQL}?question='{user_question}'"
    headers = {"ADMIN-API-KEY": f"{ADMIN_API_KEY}"}
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        sql = response.json()
        return sql
    except requests.exceptions.RequestException as e:
        exception = (f"Error generating SQL: {e}")
        return exception
    
def run_sql(id, sql):
    #Fetch Results for generated sql
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

def generate_graph(id, df, question, sql):
    #Generate Graph
    endpoint = f"{BACKEND_URL}{GENERATE_GRAPH}?id={id}&df='{df}'&question='{question}'&sql='{sql}'"
    headers = {"ADMIN-API-KEY": f"{ADMIN_API_KEY}"}
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        graph = response.json()
        return graph
    except requests.exceptions.RequestException as e:
        exception = (f"Error fetching the results: {e}")
        return exception
    
def create_adaptive_card_with_plotly(plotly_json):
    fig = pio.from_json(plotly_json['fig'])  # Recreate the figure from JSON

    # Convert to JPEG image
    img_bytes = fig.to_image(format="jpeg")

    # Encode image to base64
    encoded_image = base64.b64encode(img_bytes).decode('ascii')

    card = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.3",
        "body": [
            {
                "type": "Image",
                "url": f"data:image/jpeg;base64,{encoded_image}" 
            }
        ]
    }
    return card