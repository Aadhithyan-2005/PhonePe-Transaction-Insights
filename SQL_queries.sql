-- ================================================
-- PhonePe Transaction Insights
-- SQL Queries for Business Case Study Analysis
-- ================================================


-- ───────────────────────────────────────────────
-- 1. TRANSACTION ANALYSIS
-- ───────────────────────────────────────────────

-- Q1. Total transaction count and amount for each year
SELECT 
    year,
    SUM(transaction_count)  AS total_transactions,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_transaction
GROUP BY year
ORDER BY year;


-- Q2. Top 10 states by total transaction amount
SELECT 
    state,
    SUM(transaction_count)  AS total_transactions,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount_crores DESC
LIMIT 10;


-- Q3. Most popular transaction type by count
SELECT 
    transaction_type,
    SUM(transaction_count)  AS total_count,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_transaction
GROUP BY transaction_type
ORDER BY total_count DESC;


-- Q4. Quarter-wise transaction trend
SELECT 
    year,
    quarter,
    SUM(transaction_count)  AS total_transactions,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;


-- Q5. Average transaction value per state
SELECT 
    state,
    ROUND(AVG(transaction_amount), 2) AS avg_transaction_amount,
    ROUND(AVG(transaction_count), 2)  AS avg_transaction_count
FROM aggregated_transaction
GROUP BY state
ORDER BY avg_transaction_amount DESC
LIMIT 10;


-- ───────────────────────────────────────────────
-- 2. USER ANALYSIS
-- ───────────────────────────────────────────────

-- Q6. Top 10 states by registered users
SELECT 
    state,
    SUM(registered_users) AS total_registered_users,
    SUM(app_opens)        AS total_app_opens
FROM aggregated_user
GROUP BY state
ORDER BY total_registered_users DESC
LIMIT 10;


-- Q7. Most popular mobile brands among PhonePe users
SELECT 
    brand,
    SUM(device_count)              AS total_users,
    ROUND(AVG(device_percentage)*100, 2) AS avg_market_share_pct
FROM aggregated_user
WHERE brand IS NOT NULL AND brand != 'Unknown'
GROUP BY brand
ORDER BY total_users DESC
LIMIT 10;


-- Q8. Year-wise user growth
SELECT 
    year,
    SUM(registered_users) AS total_registered_users,
    SUM(app_opens)        AS total_app_opens
FROM aggregated_user
GROUP BY year
ORDER BY year;


-- Q9. User engagement ratio by state (app opens per user)
SELECT 
    state,
    SUM(registered_users) AS total_users,
    SUM(app_opens)        AS total_app_opens,
    ROUND(SUM(app_opens)::NUMERIC / NULLIF(SUM(registered_users), 0), 2) AS engagement_ratio
FROM aggregated_user
GROUP BY state
ORDER BY engagement_ratio DESC
LIMIT 10;


-- ───────────────────────────────────────────────
-- 3. INSURANCE ANALYSIS
-- ───────────────────────────────────────────────

-- Q10. Top 10 states by insurance transaction amount
SELECT 
    state,
    SUM(transaction_count)  AS total_policies,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_insurance
GROUP BY state
ORDER BY total_amount_crores DESC
LIMIT 10;


-- Q11. Year-wise insurance growth
SELECT 
    year,
    SUM(transaction_count)  AS total_policies,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM aggregated_insurance
GROUP BY year
ORDER BY year;


-- ───────────────────────────────────────────────
-- 4. DISTRICT LEVEL ANALYSIS
-- ───────────────────────────────────────────────

-- Q12. Top 10 districts by transaction amount
SELECT 
    state,
    district,
    SUM(transaction_count)  AS total_transactions,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM map_transaction
GROUP BY state, district
ORDER BY total_amount_crores DESC
LIMIT 10;


-- Q13. Top 10 districts by registered users
SELECT 
    state,
    district,
    SUM(registered_users) AS total_users,
    SUM(app_opens)        AS total_app_opens
FROM map_user
GROUP BY state, district
ORDER BY total_users DESC
LIMIT 10;


-- ───────────────────────────────────────────────
-- 5. TOP PERFORMERS
-- ───────────────────────────────────────────────

-- Q14. Top 10 pincodes by transaction amount
SELECT 
    state,
    entity_name AS pincode,
    SUM(transaction_count)  AS total_transactions,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores
FROM top_transaction
WHERE entity_type = 'pincode'
GROUP BY state, entity_name
ORDER BY total_amount_crores DESC
LIMIT 10;


-- Q15. Top 10 pincodes by registered users
SELECT 
    state,
    entity_name AS pincode,
    SUM(registered_users) AS total_users
FROM top_user
WHERE entity_type = 'pincode'
GROUP BY state, entity_name
ORDER BY total_users DESC
LIMIT 10;


-- ───────────────────────────────────────────────
-- 6. BUSINESS CASE STUDY QUERIES
-- ───────────────────────────────────────────────

-- Q16. Customer Segmentation - High vs Low transaction states
SELECT 
    state,
    ROUND(SUM(transaction_amount)::NUMERIC/1e7, 2) AS total_amount_crores,
    CASE 
        WHEN SUM(transaction_amount) > 1e11 THEN 'High Value'
        WHEN SUM(transaction_amount) > 1e10 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS segment
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount_crores DESC;


-- Q17. Fraud Detection - States with unusually high avg transaction amount
SELECT 
    state,
    transaction_type,
    ROUND(AVG(transaction_amount), 2) AS avg_amount,
    ROUND(STDDEV(transaction_amount), 2) AS std_amount,
    COUNT(*) AS record_count
FROM aggregated_transaction
GROUP BY state, transaction_type
HAVING STDDEV(transaction_amount) > AVG(transaction_amount)
ORDER BY std_amount DESC
LIMIT 10;


-- Q18. Payment Performance - Growth rate of each transaction type YoY
SELECT 
    transaction_type,
    year,
    SUM(transaction_count) AS total_count,
    ROUND(
        100.0 * (SUM(transaction_count) - LAG(SUM(transaction_count)) 
        OVER (PARTITION BY transaction_type ORDER BY year)) 
        / NULLIF(LAG(SUM(transaction_count)) 
        OVER (PARTITION BY transaction_type ORDER BY year), 0)
    , 2) AS yoy_growth_pct
FROM aggregated_transaction
GROUP BY transaction_type, year
ORDER BY transaction_type, year;


-- Q19. User Engagement - States with high users but low transactions (untapped)
SELECT 
    u.state,
    SUM(u.registered_users)      AS total_users,
    SUM(t.transaction_count)     AS total_transactions,
    ROUND(SUM(t.transaction_count)::NUMERIC / 
          NULLIF(SUM(u.registered_users), 0), 4) AS tx_per_user
FROM aggregated_user u
JOIN aggregated_transaction t 
    ON u.state = t.state 
    AND u.year = t.year 
    AND u.quarter = t.quarter
GROUP BY u.state
ORDER BY tx_per_user ASC
LIMIT 10;


-- Q20. Trend Analysis - Best performing quarter historically
SELECT 
    quarter,
    ROUND(AVG(total_amount), 2) AS avg_quarterly_amount_crores
FROM (
    SELECT 
        quarter,
        SUM(transaction_amount)/1e7 AS total_amount
    FROM aggregated_transaction
    GROUP BY year, quarter
) quarterly_totals
GROUP BY quarter
ORDER BY avg_quarterly_amount_crores DESC;