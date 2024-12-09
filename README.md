# Serverless Task Manager API 🚀

Este é um aplicativo **serverless** desenvolvido em **Python** usando o **Azure Functions**. O projeto é uma API simples para gerenciamento de tarefas, que permite criar, listar, atualizar e excluir tarefas. Ele utiliza o **Azure Table Storage** como banco de dados para armazenar os dados de forma escalável e confiável.

---

## **Diagrama do Projeto**
O diagrama abaixo representa a arquitetura do aplicativo:

```mermaid
graph TD
    A[Usuário/Cliente] -->|HTTP Requests| B[Azure Function App]
    B -->|POST, GET, PUT, DELETE| C[Azure Table Storage]
    C -->|Dados das Tarefas| B
