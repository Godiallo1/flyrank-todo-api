from fastapi import FastAPI, Response, Body

app = FastAPI()

#Returns a simple message when the root endpoint is accessed
@app.get("/")
def read_root():
    return {"message": "Hello, server!"}


#In-memory storage for tasks
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Commit code", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int, response: Response):
    for task in tasks:
        if task["id"] == task_id:
            return task
            
    response.status_code = 404
    return {"error": f"Task {task_id} not found"}

#Stage 3
@app.post("/tasks")
def create_task(response: Response, payload: dict = Body(default={})):
    # 1. Validate the input
    title = payload.get("title", "").strip()
    if not title:
        response.status_code = 400
        return {"error": "Title is missing or empty"}
    
    # 2. Find the next available ID
    if len(tasks) > 0:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1
        
    # 3. Create the new task and add it to our list
    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    
    # 4. Return the 201 Created status and the task
    response.status_code = 201
    return new_task

#STAGE 4

@app.put("/tasks/{task_id}")
def update_task(task_id: int, response: Response, payload: dict = Body(default={})):
    # 1. Find the task
    task_to_update = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_update = task
            break
            
    if not task_to_update:
        response.status_code = 404
        return {"error": f"Task {task_id} not found"}
        
    # 2. Validate the input (Empty body = 400)
    if not payload:
        response.status_code = 400
        return {"error": "Empty request body"}
        
    # 3. Update the fields if they were provided
    if "title" in payload:
        title = payload["title"].strip()
        if not title:
            response.status_code = 400
            return {"error": "Title cannot be empty"}
        task_to_update["title"] = title
        
    if "done" in payload:
        task_to_update["done"] = payload["done"]
        
    return task_to_update

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, response: Response):
    # Enumerate gives us both the index (i) and the task
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            # 204 No Content means we return nothing but the status
            response.status_code = 204
            return Response(status_code=204)
            
    response.status_code = 404
    return {"error": f"Task {task_id} not found"}