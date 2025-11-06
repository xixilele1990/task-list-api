from ..models.task import Task
from flask import Blueprint, abort, make_response, request, Response,jsonify
from ..db import db
from .route_utilities import validate_model,create_model,get_models_with_filters
from datetime import datetime

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        #return jsonify({"details": "Invalid data"}), 400
        abort(make_response({"details": "Invalid data"}, 400))
    
    db.session.add(new_task)
    db.session.commit()
    return new_task.to_dict(), 201


@bp.get("")

def get_all_tasks():
    query = db.select(Task)

    id_param = request.args.get("id")
    if id_param:
        query = query.where(Task.id == int(id_param))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    title_param = request.args.get("title")
    sort_param = request.args.get("sort")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))
        
    complete_param = request.args.get("is_complete")   
    if complete_param == "true":
        
        query = query.where(Task.completed_at.is_not(None))
    
    elif complete_param == "false":
        
        query = query.where(Task.completed_at.is_(None))

    #query = query.order_by(Task.id)
    if sort_param =="asc":
            query = query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    result_list = []

    result_list =[task.to_dict()for task in tasks]
        
    return jsonify(result_list or []),200


@bp.get("/<id>")

def get_one_task(id):
    
    task =validate_model(Task,id)
    return task.to_dict()


@bp.put("/<id>")
def replace_task(id):
    task = validate_model(Task, id)
    
    request_body = request.get_json()
    
    # if request_body["is_complete"]:
    #     task.completed_at = datetime.utcnow()
    # else:
    #     task.completed_at = None
    task.title = request_body["title"]
    
    task.description = request_body["description"]
    
    db.session.commit()
    
    return Response(status = 204,mimetype ="application/json")

@bp.delete("/<id>")
def del_task(id):
    task = validate_model(Task, id)
    
    db.session.delete(task)
    
    db.session.commit()
    
    return Response(status = 204,mimetype ="application/json")




@bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_model(Task, id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.patch("/<id>/mark_incomplete")
def mark_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")
