from flask import Blueprint, jsonify, request, abort, make_response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import validate_model


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")



@bp.post("")
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201


@bp.get("")
def get_all_goals():
    goals = Goal.query.order_by(Goal.id).all()
    return jsonify([goal.to_dict() for goal in goals]), 200


@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return jsonify(goal.to_dict()), 200




@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return jsonify(goal.to_dict()), 200



@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"message": f'Goal {goal.id} successfully deleted'}), 204


#nested
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids", [])
    
    for task in goal.tasks:
        task.goal_id = None



    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": task_ids
    }), 200
    
    
    
@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = tasks_response

    return jsonify(goal_dict), 200

    
    
