import sqlalchemy as sa

from .users import users_table
from .deserts import desert_table


metadata = sa.MetaData()

order_table = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.ForeignKey(users_table.c.id)),
    sa.Column("created_at", sa.DateTime()),
    sa.Column("is_active",
        sa.Boolean(),
        server_default=sa.sql.expression.true(),
        nullable=False,
    ),
)


order_lines_table = sa.Table(
    "order_lines",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("order_id", sa.ForeignKey("orders.id")),
    sa.Column("desert_id", sa.ForeignKey(desert_table.c.id)),
    sa.Column("quantity", sa.Integer()),
    sa.Column("created_at", sa.DateTime()),
)
