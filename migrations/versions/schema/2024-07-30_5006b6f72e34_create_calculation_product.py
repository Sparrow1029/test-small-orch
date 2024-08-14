"""create calculation product.

Revision ID: 5006b6f72e34
Revises:
Create Date: 2024-07-30 07:58:39.906673

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5006b6f72e34'
down_revision = None
branch_labels = ('data',)
depends_on = '048219045729'


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
INSERT INTO products (name, description, product_type, tag, status) VALUES ('Calculation', 'A Calculation to be run', 'Calculation', 'CALC', 'active') RETURNING products.product_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_blocks (name, description, tag, status) VALUES ('Calculation Metadata', 'Metadata describing parameters of Calculation', 'CALCDATA', 'active') RETURNING product_blocks.product_block_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('engine', 'Engine which will run calculation process') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('calculation_id', 'Unique ID for Calculation') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('script_path', 'Filepath of calculation script') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_product_blocks (product_id, product_block_id) VALUES ((SELECT products.product_id FROM products WHERE products.name IN ('Calculation')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('engine')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('calculation_id')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('script_path')))
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('engine'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('engine'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('calculation_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('calculation_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('script_path'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('script_path'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values WHERE subscription_instance_values.resource_type_id IN (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('engine', 'calculation_id', 'script_path'))
    """))
    conn.execute(sa.text("""
DELETE FROM resource_types WHERE resource_types.resource_type IN ('engine', 'calculation_id', 'script_path')
    """))
    conn.execute(sa.text("""
DELETE FROM product_product_blocks WHERE product_product_blocks.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Calculation')) AND product_product_blocks.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_blocks WHERE product_blocks.name IN ('Calculation Metadata')
    """))
    conn.execute(sa.text("""
DELETE FROM processes WHERE processes.pid IN (SELECT processes_subscriptions.pid FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Calculation'))))
    """))
    conn.execute(sa.text("""
DELETE FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Calculation')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Calculation')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Calculation'))
    """))
    conn.execute(sa.text("""
DELETE FROM products WHERE products.name IN ('Calculation')
    """))
