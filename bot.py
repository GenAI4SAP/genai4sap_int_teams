# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import (
    Activity,
    ChannelAccount,
    Attachment)
from botframework.connector import ConnectorClient
from botframework.connector.auth import MicrosoftAppCredentials
from base.genai4sap import call_generate_sql, run_sql, generate_graph, create_adaptive_card_with_plotly
import pandas as pd
import json

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        user_question = turn_context.activity.text
        try:
            #Generate SQL code
            response = call_generate_sql(user_question=user_question)
            #Execute SQL
            sql_results = run_sql(id=response["id"], sql=response["text"])
            #Process Results
            sql_results_json = json.loads(sql_results['df'])
            sql_results_df = pd.DataFrame(sql_results_json)
            #Format Results
            results_markdown = sql_results_df.to_markdown(index=False)
            #Generate Graph
            plotly_response = generate_graph(id=response["id"], df=sql_results["df"], question=user_question, sql=["text"])
            card = create_adaptive_card_with_plotly(plotly_response)
             # Create an Activity object
            card_response = Activity(
                type="message",
                text="Y aquí el gráfico:",
                attachments=[Attachment(content_type="application/vnd.microsoft.card.adaptive", content=card)])
            #Send Response
            await turn_context.send_activity(f"¡Gran pregunta! Déjame cumplir tu petición...")
            await turn_context.send_activity(f"Aquí está el SQL que generé:\n\n``{response['text']}``")
            await turn_context.send_activity(f"Y aquí están los resultados:\n```\n{results_markdown}```")
            await turn_context.send_activity(card_response)
        except Exception as e:
            # Handle exceptions with a user-friendly message
            await turn_context.send_activity(f"Lo siento, encontré un error al procesar su solicitud. Inténtelo de nuevo más tarde.")
            print(f"Error processing request: {e}")  # Log the error for debugging

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Hola!, soy el asistente de GenAI4SAP, ¿en qué puedo ayudarte hoy?")
