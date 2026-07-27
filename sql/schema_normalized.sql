-- 1. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 2. Accounts Table
CREATE TABLE IF NOT EXISTS accounts (
    account_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    account_number VARCHAR(34) UNIQUE NOT NULL, -- Supports IBAN formats
    account_type VARCHAR(20) NOT NULL,          -- e.g., CHECKING, SAVINGS
    balance NUMERIC(15, 2) DEFAULT 0.00 NOT NULL,
    currency VARCHAR(3) NOT NULL,                -- ISO 4217 Currency Code
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE RESTRICT
);

-- 3. Merchants Table
CREATE TABLE IF NOT EXISTS merchants (
    merchant_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,              -- MCC Description (e.g., GROCERY, RETAIL)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 4. Transactions Table (Core Fact Table)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    merchant_id UUID NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,                -- e.g., COMPLETED, PENDING, DECLINED
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT fk_account FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE,
    CONSTRAINT fk_merchant FOREIGN KEY (merchant_id) REFERENCES merchants (merchant_id) ON DELETE RESTRICT
);

-- 5. Performance Optimizations (Covering Indexes)
CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions (account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions (timestamp);
CREATE INDEX IF NOT EXISTS idx_accounts_customer_id ON accounts (customer_id);
