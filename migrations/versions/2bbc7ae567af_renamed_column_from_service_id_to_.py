"""Renamed column from service_id to parent_service_id

Revision ID: 2bbc7ae567af
Revises: 04983a516a91
Create Date: 2024-10-12 22:25:14.373461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bbc7ae567af'
down_revision = '04983a516a91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('boolean_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('boolean_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('date_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('date_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('float_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('float_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('number_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('number_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('order_services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('parent_orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('select_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('select_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('text_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('text_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    with op.batch_alter_table('textarea_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_service_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('textarea_options_service_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'services', ['parent_service_id'], ['id'])
        batch_op.drop_column('service_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('textarea_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('textarea_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('text_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('text_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('select_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('select_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('parent_orders', schema=None) as batch_op:
        batch_op.drop_column('creation_date')
        batch_op.drop_column('due_date')

    with op.batch_alter_table('order_services', schema=None) as batch_op:
        batch_op.drop_column('creation_date')
        batch_op.drop_column('due_date')

    with op.batch_alter_table('number_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('number_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('float_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('float_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('date_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('date_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    with op.batch_alter_table('boolean_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('boolean_options_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.drop_column('parent_service_id')

    # ### end Alembic commands ###
