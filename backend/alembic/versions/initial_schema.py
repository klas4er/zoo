"""initial schema

Revision ID: 1
Revises:
Create Date: 2025-08-30 01:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create animals table
    op.create_table('animals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('species', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_animals_id'), 'animals', ['id'], unique=False)
    op.create_index(op.f('ix_animals_species'), 'animals', ['species'], unique=False)

    # Create observations table
    op.create_table('observations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('animal_id', sa.Integer(), nullable=True),
        sa.Column('watcher_id', sa.Integer(), nullable=True),
        sa.Column('ts', sa.DateTime(), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['animal_id'], ['animals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_observations_id'), 'observations', ['id'], unique=False)
    op.create_index(op.f('ix_observations_animal_id'), 'observations', ['animal_id'], unique=False)
    op.create_index(op.f('ix_observations_watcher_id'), 'observations', ['watcher_id'], unique=False)
    op.create_index(op.f('ix_observations_ts'), 'observations', ['ts'], unique=False)

    # Create observation_entities table
    op.create_table('observation_entities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('observation_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('payload_json', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['observation_id'], ['observations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_observation_entities_id'), 'observation_entities', ['id'], unique=False)
    op.create_index(op.f('ix_observation_entities_observation_id'), 'observation_entities', ['observation_id'], unique=False)
    op.create_index(op.f('ix_observation_entities_type'), 'observation_entities', ['type'], unique=False)

    # Create relations table
    op.create_table('relations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('src_animal_id', sa.Integer(), nullable=True),
        sa.Column('dst_animal_id', sa.Integer(), nullable=True),
        sa.Column('relation_type', sa.String(), nullable=True),
        sa.Column('ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['dst_animal_id'], ['animals.id'], ),
        sa.ForeignKeyConstraint(['src_animal_id'], ['animals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_relations_id'), 'relations', ['id'], unique=False)
    op.create_index(op.f('ix_relations_src_animal_id'), 'relations', ['src_animal_id'], unique=False)
    op.create_index(op.f('ix_relations_dst_animal_id'), 'relations', ['dst_animal_id'], unique=False)

def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('relations')
    op.drop_table('observation_entities')
    op.drop_table('observations')
    op.drop_table('animals')