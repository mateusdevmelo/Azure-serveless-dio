import logging
import azure.functions as func
from azure.data.tables import TableServiceClient, TableEntity
import os
import json

# Configurar a conexão ao Azure Table Storage
CONNECTION_STRING = os.getenv("AzureWebJobsStorage")
TABLE_NAME = "Tasks"
table_service = TableServiceClient.from_connection_string(CONNECTION_STRING)
table_client = table_service.create_table_if_not_exists(TABLE_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Identificar o método HTTP
        method = req.method
        if method == "GET":
            # Listar tarefas
            tasks = list(table_client.list_entities())
            return func.HttpResponse(json.dumps(tasks), status_code=200)
        elif method == "POST":
            # Criar tarefa
            data = req.get_json()
            task = TableEntity(partition_key="Task", row_key=data["id"], name=data["name"], status=data["status"])
            table_client.create_entity(task)
            return func.HttpResponse("Task created", status_code=201)
        elif method == "PUT":
            # Atualizar tarefa
            data = req.get_json()
            task = table_client.get_entity(partition_key="Task", row_key=data["id"])
            task["status"] = data["status"]
            table_client.update_entity(task)
            return func.HttpResponse("Task updated", status_code=200)
        elif method == "DELETE":
            # Deletar tarefa
            id = req.params.get("id")
            if not id:
                return func.HttpResponse("ID is required", status_code=400)
            table_client.delete_entity(partition_key="Task", row_key=id)
            return func.HttpResponse("Task deleted", status_code=200)
        else:
            return func.HttpResponse("Method not allowed", status_code=405)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Internal server error", status_code=500)
