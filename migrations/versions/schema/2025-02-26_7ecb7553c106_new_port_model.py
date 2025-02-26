"""new port model.

Revision ID: 7ecb7553c106
Revises: be3e458b2f92
Create Date: 2025-02-26 23:18:44.719179

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7ecb7553c106'
down_revision = 'be3e458b2f92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
INSERT INTO products (name, description, product_type, tag, status) VALUES ('Port', 'Physical Port Configuration', 'Port', 'PORT', 'active') RETURNING products.product_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_blocks (name, description, tag, status) VALUES ('Port Block', 'Physical Port Block config - can contain LAG infor', 'PORTBLK', 'active') RETURNING product_blocks.product_block_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_blocks (name, description, tag, status) VALUES ('Port Configuration', 'Common L2 Port configs', 'PORTCONFBLK', 'active') RETURNING product_blocks.product_block_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('iface_id', 'uuid of iface in IMS') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('device_id', 'int id of device in IMS') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('speed', 'int speed of interface in MB/s') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_product_blocks (product_id, product_block_id) VALUES ((SELECT products.product_id FROM products WHERE products.name IN ('Port')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Block')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_relations (in_use_by_id, depends_on_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Block')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('iface_id')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('device_id')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('speed')))
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('iface_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('iface_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('device_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('device_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('speed'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('speed'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values WHERE subscription_instance_values.resource_type_id IN (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('iface_id', 'device_id', 'speed'))
    """))
    conn.execute(sa.text("""
DELETE FROM resource_types WHERE resource_types.resource_type IN ('iface_id', 'device_id', 'speed')
    """))
    conn.execute(sa.text("""
DELETE FROM product_product_blocks WHERE product_product_blocks.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Port')) AND product_product_blocks.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Block'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_relations WHERE product_block_relations.in_use_by_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Block')) AND product_block_relations.depends_on_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('Port Configuration', 'Port Block'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_blocks WHERE product_blocks.name IN ('Port Configuration', 'Port Block')
    """))
    conn.execute(sa.text("""
DELETE FROM processes WHERE processes.pid IN (SELECT processes_subscriptions.pid FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Port'))))
    """))
    conn.execute(sa.text("""
DELETE FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Port')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Port')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('Port'))
    """))
    conn.execute(sa.text("""
DELETE FROM products WHERE products.name IN ('Port')
    """))
