"""Add Queue and Item tables

Revision ID: 157d346f09b5
Revises: 
Create Date: 2022-05-07 02:20:41.867250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157d346f09b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_queues_id'), 'queues', ['id'], unique=False)
    op.create_index(op.f('ix_queues_name'), 'queues', ['name'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('queue_id', sa.Integer(), nullable=False),
    sa.Column('quality', sa.Integer(), nullable=True),
    sa.Column('easiness', sa.Float(), nullable=True),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.Column('repetitions', sa.Integer(), nullable=True),
    sa.Column('review_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['queue_id'], ['queues.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_queues_name'), table_name='queues')
    op.drop_index(op.f('ix_queues_id'), table_name='queues')
    op.drop_table('queues')
    # ### end Alembic commands ###
