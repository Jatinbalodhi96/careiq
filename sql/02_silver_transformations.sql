-- 02_silver_transformations.sql
-- Run these queries in Databricks SQL or a Notebook to create the Silver layer

-- 1. Clean and Standardize NFHS-5 Data
CREATE OR REPLACE TABLE silver_health_indicators AS
SELECT 
    TRIM(LOWER(district_name)) AS district_name,
    TRIM(LOWER(state_ut)) AS state_name,
    -- Handle dirty data (remove parentheses and asterisks)
    CAST(REGEXP_REPLACE(institutional_birth_5y_pct, '[\\\\(\\\\)\\\\*]', '') AS DOUBLE) AS institutional_birth_pct,
    CAST(REGEXP_REPLACE(child_12_23m_fully_vaccinated_based_on_information_from_eit_pct, '[\\\\(\\\\)\\\\*]', '') AS DOUBLE) AS fully_vaccinated_pct,
    CAST(REGEXP_REPLACE(child_u5_who_are_stunted_height_for_age_18_pct, '[\\\\(\\\\)\\\\*]', '') AS DOUBLE) AS child_stunting_pct,
    CAST(REGEXP_REPLACE(hh_member_covered_health_insurance_pct, '[\\\\(\\\\)\\\\*]', '') AS DOUBLE) AS health_insurance_pct,
    CAST(REGEXP_REPLACE(fp_unmet_total_cm_w15_49_7_pct, '[\\\\(\\\\)\\\\*]', '') AS DOUBLE) AS unmet_fp_pct,
    CAST(population_below_age_15_years_pct AS DOUBLE) AS pop_below_15_pct,
    CAST(households_surveyed AS DOUBLE) AS households_surveyed
FROM bronze_health_indicators;

-- 2. Clean Facilities Data and Apply Evidence Trust Engine (Example: Maternity Care)
CREATE OR REPLACE TABLE silver_facilities_scored AS
SELECT
    unique_id,
    name,
    TRIM(LOWER(address_city)) AS city,
    TRIM(LOWER(address_stateOrRegion)) AS state_region,
    COALESCE(CAST(capacity AS INT), 50) AS estimated_capacity, -- default capacity if null
    
    -- Evidence Trust Engine Logic for Maternity Care
    -- +3 for specialty, +2 for procedure, +2 for equipment, +1 for description
    (
        CASE WHEN LOWER(specialties) LIKE '%maternity%' OR LOWER(specialties) LIKE '%obstetrics%' THEN 3 ELSE 0 END +
        CASE WHEN LOWER(procedure) LIKE '%delivery%' OR LOWER(procedure) LIKE '%caesarean%' THEN 2 ELSE 0 END +
        CASE WHEN LOWER(equipment) LIKE '%incubator%' OR LOWER(equipment) LIKE '%ultrasound%' OR LOWER(equipment) LIKE '%fetal monitor%' THEN 2 ELSE 0 END +
        CASE WHEN LOWER(description) LIKE '%maternity%' OR LOWER(description) LIKE '%delivery%' THEN 1 ELSE 0 END
    ) AS maternity_evidence_score,
    
    -- Categorize the score into Trust Signals
    CASE 
        WHEN (
            CASE WHEN LOWER(specialties) LIKE '%maternity%' OR LOWER(specialties) LIKE '%obstetrics%' THEN 3 ELSE 0 END +
            CASE WHEN LOWER(procedure) LIKE '%delivery%' OR LOWER(procedure) LIKE '%caesarean%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(equipment) LIKE '%incubator%' OR LOWER(equipment) LIKE '%ultrasound%' OR LOWER(equipment) LIKE '%fetal monitor%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(description) LIKE '%maternity%' OR LOWER(description) LIKE '%delivery%' THEN 1 ELSE 0 END
        ) >= 5 THEN 'Strong'
        WHEN (
            CASE WHEN LOWER(specialties) LIKE '%maternity%' OR LOWER(specialties) LIKE '%obstetrics%' THEN 3 ELSE 0 END +
            CASE WHEN LOWER(procedure) LIKE '%delivery%' OR LOWER(procedure) LIKE '%caesarean%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(equipment) LIKE '%incubator%' OR LOWER(equipment) LIKE '%ultrasound%' OR LOWER(equipment) LIKE '%fetal monitor%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(description) LIKE '%maternity%' OR LOWER(description) LIKE '%delivery%' THEN 1 ELSE 0 END
        ) BETWEEN 3 AND 4 THEN 'Partial'
        WHEN (
            CASE WHEN LOWER(specialties) LIKE '%maternity%' OR LOWER(specialties) LIKE '%obstetrics%' THEN 3 ELSE 0 END +
            CASE WHEN LOWER(procedure) LIKE '%delivery%' OR LOWER(procedure) LIKE '%caesarean%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(equipment) LIKE '%incubator%' OR LOWER(equipment) LIKE '%ultrasound%' OR LOWER(equipment) LIKE '%fetal monitor%' THEN 2 ELSE 0 END +
            CASE WHEN LOWER(description) LIKE '%maternity%' OR LOWER(description) LIKE '%delivery%' THEN 1 ELSE 0 END
        ) BETWEEN 1 AND 2 THEN 'Weak'
        ELSE 'No Claim'
    END AS maternity_trust_signal

FROM bronze_facilities;
