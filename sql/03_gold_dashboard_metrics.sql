-- 03_gold_dashboard_metrics.sql
-- Use these queries in your Databricks SQL Dashboard to power the visualizations

-- Widget 1: Regional Supply Index & Data Confidence (Table or Map)
-- Calculates trust-weighted capacity and confidence percentage for Maternity Care
CREATE OR REPLACE VIEW gold_maternity_supply AS
SELECT 
    city AS district_name,
    state_region AS state_name,
    COUNT(*) AS total_facilities_claiming_maternity,
    
    -- Sum of capacity weighted by trust
    SUM(
        CASE 
            WHEN maternity_trust_signal = 'Strong' THEN estimated_capacity * 1.0
            WHEN maternity_trust_signal = 'Partial' THEN estimated_capacity * 0.5
            ELSE 0 
        END
    ) AS regional_supply_index,
    
    -- Data Confidence: % of facilities with Strong or Partial claims
    ROUND(
        SUM(CASE WHEN maternity_trust_signal IN ('Strong', 'Partial') THEN 1 ELSE 0 END) / COUNT(*) * 100
    , 1) AS data_confidence_pct

FROM silver_facilities_scored
WHERE maternity_trust_signal != 'No Claim'
GROUP BY city, state_region;


-- Widget 2: Care Gap Severity & Risk Categories (Bar Chart or Map)
-- Combines Supply with NFHS-5 Demand Indicators
CREATE OR REPLACE VIEW gold_maternity_care_gap AS
SELECT 
    n.district_name,
    n.state_name,
    n.institutional_birth_pct,
    COALESCE(s.regional_supply_index, 0) AS maternity_supply_index,
    COALESCE(s.data_confidence_pct, 0) AS data_confidence_pct,
    
    -- Calculate Base Severity Score (Scaled 0-150)
    (100 - n.institutional_birth_pct) + 
    (CASE WHEN COALESCE(s.regional_supply_index, 0) < 100 THEN 50 ELSE 0 END) AS care_gap_severity_score,

    -- Risk Categorization Logic
    CASE 
        -- If data confidence is too low, we can't accurately assess the risk; it's a data problem.
        WHEN COALESCE(s.data_confidence_pct, 0) < 30 AND COALESCE(s.regional_supply_index, 0) > 0 THEN 'Data Blindspot (Audit Required)'
        
        -- High Demand + Low Supply
        WHEN ((100 - n.institutional_birth_pct) + (CASE WHEN COALESCE(s.regional_supply_index, 0) < 100 THEN 50 ELSE 0 END)) >= 120 THEN 'Critical Risk Desert'
        
        -- Moderate Demand + Low Supply OR High Demand + Moderate Supply
        WHEN ((100 - n.institutional_birth_pct) + (CASE WHEN COALESCE(s.regional_supply_index, 0) < 100 THEN 50 ELSE 0 END)) >= 90 THEN 'High Risk Desert'
        
        -- Some unmet need but adequate supply
        WHEN ((100 - n.institutional_birth_pct) + (CASE WHEN COALESCE(s.regional_supply_index, 0) < 100 THEN 50 ELSE 0 END)) >= 60 THEN 'Moderate Risk'
        
        -- Low unmet need + good supply
        ELSE 'Low Risk / Adequate Coverage'
    END AS care_gap_risk_category
    
FROM silver_health_indicators n
LEFT JOIN gold_maternity_supply s 
    ON n.district_name = s.district_name;


-- Widget 3: AI Review Queue Priority (Table)
-- Flags high-capacity facilities with weak/suspicious evidence for manual review
SELECT 
    name AS facility_name,
    city,
    state_region,
    estimated_capacity,
    maternity_trust_signal,
    maternity_evidence_score
FROM silver_facilities_scored
WHERE estimated_capacity > 100 
  AND maternity_trust_signal = 'Weak'
ORDER BY estimated_capacity DESC
LIMIT 50;
