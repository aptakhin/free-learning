from sqlalchemy import ForeignKey, Table, Column, Integer, MetaData, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()


organizations = Table(
    'organizations',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('slug', String, nullable=False),
    Column('title', String, nullable=False),
    UniqueConstraint('slug', name='organizations_slug_unique_idx'),
)

accounts = Table(
    'accounts',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
)

account_authentifications = Table(
    'account_authentification_types',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('type', String, nullable=False),
    Column('key', String, nullable=False),
    Column('account_id', ForeignKey('accounts.id'), nullable=False),

    UniqueConstraint('type', 'key', name='account_authentifications_type_key_unique_idx'),
)

account_authentifications = Table(
    'account_authententifications',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('account_id', ForeignKey('account_authentification_types.id'), nullable=False),
)
