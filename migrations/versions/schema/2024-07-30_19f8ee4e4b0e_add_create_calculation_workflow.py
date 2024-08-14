"""add create calculation workflow.

Revision ID: 19f8ee4e4b0e
Revises: 5006b6f72e34
Create Date: 2024-07-30 08:36:30.905643

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '19f8ee4e4b0e'
down_revision = '5006b6f72e34'
branch_labels = None
depends_on = None


from orchestrator.migrations.helpers import create_workflow, delete_workflow

new_workflows = [
    {
        "name": "create_calculation",
        "target": "CREATE",
        "description": "Create Calculation Subscription",
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
