# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from base.genai4sap import call_generate_sql, run_sql
import pandas as pd
import json

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        response = call_generate_sql(user_question=turn_context.activity.text)
        response_data = run_sql(id=response["id"], sql=response["text"])
        response_data_json = json.loads(response_data['df'])
        response_data_df = pd.DataFrame(response_data_json)
        response_data_markdown = response_data_df.to_markdown(index=False)
        await turn_context.send_activity(f"¡Gran pregunta! Déjame cumplir tu petición...")
        await turn_context.send_activity(f"""SQL:\n 
{response["text"]}""")
        await turn_context.send_activity(f"""Datos:\n 
{response_data_markdown}""")
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Hola!, soy el asistente de GenAI4SAP, ¿en qué puedo ayudarte hoy?")
