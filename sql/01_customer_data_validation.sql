-- =====================================================
-- PROJECT: CUSTOMER RETENTION INTELLIGENCE PLATFORM
-- DATABASE: telco_retention_db
-- MODULE: CUSTOMER DATA VALIDATION
-- =====================================================

-- -----------------------------------------------------
-- 1. CUSTOMER ID UNIQUENESS CHECK
-- Objective: Identify duplicate customer IDs.
-- -----------------------------------------------------

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT "Customer ID") AS unique_customers,
    COUNT(*) - COUNT(DISTINCT "Customer ID") AS duplicate_ids
FROM public.telco_customers_raw;


-- -----------------------------------------------------
-- 2. MISSING VALUE ANALYSIS
-- Objective: Identify NULL values in important columns.
-- -----------------------------------------------------

SELECT
    COUNT(*) FILTER (WHERE "Customer ID" IS NULL) AS missing_customer_id,
    COUNT(*) FILTER (WHERE "Offer" IS NULL) AS missing_offer,
    COUNT(*) FILTER (WHERE "Internet Type" IS NULL) AS missing_internet_type,
    COUNT(*) FILTER (WHERE "Churn Category" IS NULL) AS missing_churn_category,
    COUNT(*) FILTER (WHERE "Churn Reason" IS NULL) AS missing_churn_reason
FROM public.telco_customers_raw;


-- -----------------------------------------------------
-- 3. EMPTY STRING ANALYSIS
-- Objective: Identify blank values that are not SQL NULL.
-- -----------------------------------------------------

SELECT
    COUNT(*) FILTER (
        WHERE NULLIF(TRIM("Offer"), '') IS NULL
    ) AS blank_offer,

    COUNT(*) FILTER (
        WHERE NULLIF(TRIM("Internet Type"), '') IS NULL
    ) AS blank_internet_type

FROM public.telco_customers_raw;

-- -----------------------------------------------------
-- 4. OFFER COLUMN VALUE INSPECTION
-- Objective: Inspect actual values and identify missing markers.
-- -----------------------------------------------------

SELECT
    COALESCE(
        NULLIF(TRIM("Offer"), ''),
        '[NULL / BLANK]'
    ) AS offer_value,
    COUNT(*) AS customer_count
FROM public.telco_customers_raw
GROUP BY 1
ORDER BY customer_count DESC;