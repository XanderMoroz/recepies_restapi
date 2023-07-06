import sqlalchemy

from .users import users_table

metadata = sqlalchemy.MetaData()

recipes_table = sqlalchemy.Table(
    "recipes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
    sqlalchemy.Column("content", sqlalchemy.Text()),
)