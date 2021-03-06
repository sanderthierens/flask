"""dayPerformancetable

Revision ID: 20a2eec097b9
Revises: 5e8914024ce5
Create Date: 2020-04-03 00:34:55.339251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a2eec097b9'
down_revision = '5e8914024ce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('day_performance', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_day_performance_timestamp'), 'day_performance', ['timestamp'], unique=False)
    op.drop_index('ix_day_performance_amount', table_name='day_performance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_day_performance_amount', 'day_performance', ['amount'], unique=False)
    op.drop_index(op.f('ix_day_performance_timestamp'), table_name='day_performance')
    op.drop_column('day_performance', 'timestamp')
    # ### end Alembic commands ###
