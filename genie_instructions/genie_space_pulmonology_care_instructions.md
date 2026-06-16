# Genie Space Instructions: Pulmonology Care Gap (ARI)
**Scope:** `databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset` (Tables: `facilities`, `india_post_pincode_directory`, `nfhs_5_district_health_indicators`).

## Core Calculations
1. **Demand Score (0-100)** = `0.50*ARIPrevalence + 0.50*CareSeekingGap`
   * `ARIPrevalence` = `children_prev_symptoms_of_acute_respiratory_infection_ari_2_pct`
   * `CareSeekingGap` = `100.0 - children_with_fever_or_symptoms_of_ari_2wk_taken_to_a_healt_pct`
   *(Cleanse string cols with `CAST(REGEXP_REPLACE(col, '[\\(\\)\\*]', '') AS DOUBLE)`).*

2. **Supply Index (0-100)** = scaled sum of `capacity * trust_multiplier` (default capacity = 50 if null)
   * **Trust Score** (0-8 per facility): `specialties` contains pulmonology/chest medicine/pediatrics (+3); `procedure` contains nebulization/bronchoscopy/respiratory therapy (+2); `equipment` contains oxygen cylinder/nebulizer/ventilator (+2); `description` mentions asthma/pneumonia/cough specialist (+1).
   * **Multiplier**: Score 5-8 $\rightarrow$ 1.0 (Strong); Score 3-4 $\rightarrow$ 0.5 (Partial); Score 1-2 $\rightarrow$ 0.1 (Weak); Score 0 $\rightarrow$ 0.0.

3. **Care Gap Index (0-200)** = `Demand Score + (100 - Supply Index)`
   * Status: `>=120` $\rightarrow$ **Critical Desert** | `90-119` $\rightarrow$ **High Risk** | `60-89` $\rightarrow$ **Moderate Risk** | `<60` $\rightarrow$ **Safe Zone**

## Query Rules
* **District/City Match:** Use `TRIM(LOWER(district_name)) = TRIM(LOWER(address_city))`.
* **National Average:** If no district specified, calculate averages across all rows before scoring.

## Consistent Output Schema (NO Markdown Reports or Text Visuals)
Genie must return results in a flat table format with exactly the following columns:
* `district_name` (string)
* `circle_name` (string)
* `latitude` (double)
* `longitude` (double)
* `ari_prevalence_pct` (double)
* `untreated_fever_ari_pct` (double)
* `demand_score` (double)
* `total_facilities` (long)
* `verified_pulmonology_facilities` (long)
* `supply_index` (double)
* `care_gap_index` (double)
* `care_gap_status` (string)
