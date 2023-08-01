"""empty message

Revision ID: 63df48335309
Revises: 
Create Date: 2023-08-01 11:46:31.256015

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '63df48335309'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_updated',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_updated',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###
