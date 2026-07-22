-- ====================================================================
-- FINTECH DATA PLATFORM - TRANSACTIONAL WAREHOUSE AD-HOC ANALYTICS
-- ====================================================================

-- 1. Daily Ingestion Integrity Check
-- Verifies that rows have loaded cleanly and separates volume states
SELECT 
    status, 
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_volume_usd,
    ROUND(AVG(amount), 2) AS average_ticket_size
FROM transactions
GROUP BY status
ORDER BY total_volume_usd DESC;

-- 2. Channel Processing Velocity Profile
-- Identifies transaction traffic density across different systems
SELECT 
    channel,
    COUNT(*) AS processing_hits,
    ROUND(SUM(amount), 2) AS aggregated_volume,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions)), 2) AS channel_market_share_percentage
FROM transactions
GROUP BY channel
ORDER BY processing_hits DESC;

-- 3. Top 10 High-Value Whale Account Profiles
-- Flags accounts driving the highest transaction values across the ledger
SELECT 
    customer_id,
    COUNT(*) AS execution_count,
    ROUND(SUM(amount), 2) AS gross_spend_volume_usd
FROM transactions
GROUP BY customer_id
ORDER BY gross_spend_volume_usd DESC
LIMIT 10;

-- 4. Critical Risk Management Alert Matrix
-- Instantly captures accounts attempting very high transaction values on failed channels
SELECT 
    transaction_id,
    customer_id,
    amount,
    currency,
    channel,
    transaction_date
FROM transactions
WHERE amount > 1400.00 AND status = 'Failed'
ORDER BY amount DESC;
