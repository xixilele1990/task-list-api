from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
#from sqlalchemy import Date


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    