"""Database Initialisation

Revision ID: 4dde9161923e
Revises: 
Create Date: 2022-12-27 10:05:06.536757

"""
import sqlalchemy as sa
from alembic import op


# Revision identifiers, used by Alembic
revision: str | tuple[str, ...] | None = '4dde9161923e'
down_revision: str | tuple[str, ...] | None = None
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('access_code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_code')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('family_id', sa.BigInteger(), nullable=True),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('account',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('currency', sa.Enum('RUB', 'USD', name='currencytype'), nullable=False),
    sa.Column('opening_balance', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_name'), 'account', ['name'], unique=False)
    op.create_table('budget',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('joint', 'personal', name='budgettype'), nullable=False),
    sa.Column('planned_outcomes', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_budget_name'), 'budget', ['name'], unique=False)
    op.create_table('category',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('base_category_id', sa.BigInteger(), nullable=True),
    sa.Column('budget_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('Income', 'Outcome', name='categorytype'), nullable=False),
    sa.ForeignKeyConstraint(['base_category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=False)
    op.create_table('transaction',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.Column('category_id', sa.BigInteger(), nullable=True),
    sa.Column('type', sa.Enum('Income', 'Outcome', 'Transfer', name='transactiontype'), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('due_time', sa.Time(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('note', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_budget_name'), table_name='budget')
    op.drop_table('budget')
    op.drop_index(op.f('ix_account_name'), table_name='account')
    op.drop_table('account')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('family')
    # ### end Alembic commands ###
