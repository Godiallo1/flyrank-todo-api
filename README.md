# FlyRank To-Do API

## 1. Introduction
This is a small backend API that manages a simple to-do list. Built using Python and FastAPI, it supports full CRUD operations (Create, Read, Update, and Delete) allowing users to manage tasks. The data for this API lives entirely in-memory.

## 2. How to Run It
To start the server locally, open your terminal in the project folder and run the following command:

```bash
uvicorn main:app --reload

## 3 Endpoints:
| CRUD Operation | HTTP Method | Endpoint | Meaning |
| :--- | :--- | :--- | :--- |
| **Read** | `GET` | `/` | Returns the API description and version info. |
| **Read** | `GET` | `/health` | Returns a simple status check to ensure the server is alive[cite: 1]. |
| **Create** | `POST` | `/tasks` | Add a new task[cite: 1]. |
| **Read** | `GET` | `/tasks` | List all tasks[cite: 1]. |
| **Read** | `GET` | `/tasks/{id}` | Get a specific task by its ID[cite: 1]. |
| **Update** | `PUT` | `/tasks/{id}` | Change a specific task's details[cite: 1]. |
| **Delete** | `DELETE` | `/tasks/{id}` | Remove a task from the list[cite: 1]. |

## 4. Example Request
Here is the output of fetching the task list via curl:

HTTP/1.1 200 OK
date: Mon, 20 Jul 2026 18:06:58 GMT
server: uvicorn
content-length: 131
content-type: application/json


## 5. Swagger UI Testing
Here are the results from testing the endpoints directly in the UI:

<p align="center">
  <img src="swagger-UI-1.png" width="45%" />
  <img src="swagger-UI-2.png" width="45%" />
</p>

## 6. The AI Rematch

**What did the AI do better than me?**
The AI wrote more modular code by creating a reusable `get_task_by_id` helper function. It also utilized Pydantic models to strictly define the data structures instead of relying on loose dictionaries.

**What did it get wrong or quietly ignore from the prompt?**
The AI failed the strict 400 Bad Request validation rule for empty titles[cite: 1]. It used Pydantic validators that raise a ValueError, which causes FastAPI to automatically return a 422 Unprocessable Entity before the 400 error logic can ever be triggered. 

**What did my prompt forget to specify, leaving the AI to decide?**
I forgot to specify the starting data and the exact dictionary keys. Left to decide for itself, the AI started with a completely empty list and used "completed" as the boolean key instead of "done".

**The Rematch:**
I explicitly told ChatGPT: "Your Pydantic validator returns a 422 error, but I strictly need a 400 Bad Request when the title is empty. Please adjust the validation to return a 400, use 'done' instead of 'completed', and pre-fill the list with three dummy tasks." The second version successfully captured the 400 error manually without the Pydantic validator blocking it.