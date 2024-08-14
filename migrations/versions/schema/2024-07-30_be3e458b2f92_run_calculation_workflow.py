"""run calculation workflow.

Revision ID: be3e458b2f92
Revises: 19f8ee4e4b0e
Create Date: 2024-07-30 13:38:48.708437

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'be3e458b2f92'
down_revision = '19f8ee4e4b0e'
branch_labels = None
depends_on = None


from orchestrator.migrations.helpers import create_workflow, delete_workflow

new_workflows = [
    {
        "name": "run_calculation",
        "target": "SYSTEM",
        "description": "Run a calculation",
        "product_type": "Calculation"
    }
]


def upgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        create_workflow(conn, workflow)


def downgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        delete_workflow(conn, workflow["name"])
