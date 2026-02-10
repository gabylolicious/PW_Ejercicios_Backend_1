from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field  # field para validaciones 1-5
from fastapi import APIRouter, HTTPException, Query # PARA ENRUTAMIENTO Y ERRORES

# Para que converse main con ejercicio1
router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]  # para documentacion
)

# un diccionario; la id no será un num, será str
tasks_repertory : dict[str,"Task"] = {}

# todas las clases son heredadas de BaseModel
class Task(BaseModel):
    id : str
    title : str
    description : Optional[str] = None
    priority : int = Field(..., ge = 1, le = 5) # entre 1-5, min_length y max_length tmb
    completed : bool = False # por defecto está en falso

class TaskCreate(BaseModel):
    title : str
    description : Optional[str] = None
    priority : int = Field(..., ge = 1, le = 5)     

@router.post("/")
async def create_Task(payload : TaskCreate):
    # EL argumento será un payload de tipo Task
    task_id = str(uuid4()) # parseando la UUID4 en string

    task = Task(
        id = task_id,
        title = payload.title,
        description = payload.description,
        priority = payload.priority,
        completed = False
    )
    
    tasks_repertory[task_id] = task
    return {
        "msg" : "Task creada",
        "data" : task
    }

@router.get("/{task_id}")
async def get_Task(task_id : str):
    task = tasks_repertory.get(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task no encontrada en este repositorio"
        )
    return {
        "msg" : "",
        "data" : task
    }

@router.get("/")
async def getListTask(
    completed : Optional[bool] = Query(default = None),
    min_priority : Optional[int] = Query(default = None, ge = 1, le = 5)
    #,
    #skip : Optional[int] = Query(default = 0, ge = 0),
    #limit : Optional[int] = Query(default = 20, ge = 1, le = 100)
):
    tasks = []
    # Tenemos que recorrer la lista
    for t in tasks_repertory.values() :
        tasks.append(t)
    if completed != None :
        # Queremos mantener la tarea en el mismo arreglo
        filterTasks = []
        for t in tasks:
            if t.completed == completed : 
                filterTasks.append(t)
        tasks = filterTasks
    
    # Hasta ahora solo los hemos filtrado por prioridad minima
    if min_priority != None :
        # Queremos mantener la tarea en el mismo arreglo
        filterTasks = []
        for t in tasks:
            if t.priority >= min_priority : 
                filterTasks.append(t)
        tasks = filterTasks

    # Faltan el skip y el limit

    paginated_tasks = []

    # Le ponemos el argumento start y skip; 
    # a partir de donde inicia el arreglo? 
    # a partir de donde deja de mostrarme los elementos?

    #start = skip
    #end = skip + limit

    total = len(tasks)

    return {
        "msg" : "",
        "meta" : {
            "total" : total
        },
        "data" : tasks
    }