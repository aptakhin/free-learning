from sqlalchemy import DateTime, ForeignKey, Table, Column, MetaData, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB


metadata = MetaData()


organization = Table(
    'organization',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('slug', String, nullable=False),
    Column('title', String, nullable=False),
    UniqueConstraint('slug', name='organization_slug_unique_idx'),
)

account = Table(
    'account',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
)


"""Authentification - a14n."""
account_a14n_provider = Table(
    'account_a14n_provider',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('account_id', ForeignKey('account.id'), nullable=False),
    Column('type', String, nullable=False),
    Column('value', String, nullable=False),
    UniqueConstraint('account_id', 'type', 'value', name='account_a14n_provider_account_id_type_value_idx'),
)


account_a14n_signature = Table(
    'account_a14n_signature',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column('account_a14n_provider_id', ForeignKey('account_a14n_provider.id'), nullable=False),
    Column('valid_until', DateTime, nullable=True),
    Column('signed_in_at', DateTime, nullable=True),
    Column('account_a14n_provider_type', String, nullable=False),
    Column('value', String, nullable=False),
    Column('device', JSONB, nullable=True),
)
