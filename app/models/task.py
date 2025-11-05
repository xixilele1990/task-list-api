from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from sqlalchemy import String, Date
from datetime import datetime
from flask import Blueprint, abort, make_response, request, Response,jsonify

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    completed_at:Mapped[datetime.date] = mapped_column(Date, nullable=True)


    def to_dict(self): # json
        
        
        return {"id": self.id,
                "title":self.title,
                "description":self.description,
                #"is_complete":self.completed_at if self.completed_at else False
                "is_complete": self.completed_at is not None}
        


    @classmethod
    def from_dict(cls, data_dict):
        if "title" not in data_dict:
            #abort(make_response({"details": "Invalid data"}, 400))
            raise KeyError("title")
        if "description" not in data_dict:
            #abort(make_response({"details": "Invalid data"}, 400))
            raise KeyError("description")
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=None  # default to None when creating
        )
        
    
    