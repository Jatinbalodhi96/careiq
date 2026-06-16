# Genie Space Instructions: Immunization Care Gap
**Scope:** `databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset` (Tables: `facilities`, `india_post_pincode_directory`, `nfhs_5_district_health_indicators`).

## Core Calculations
1. **Demand Score (0-100)** = `100.0 - (0.40*Polio3 + 0.30*Measles1 + 0.30*BCG)`
   * `Polio3` = `child_12_23m_who_have_received_3_doses_of_polio_vaccine_pct`
   * `Measles1` = `child_12_23m_who_have_received_the_first_dose_of_mcv_mcv_pct`
   * `BCG` = `child_12_23m_who_have_received_bcg_pct`
   *(Cleanse string cols with `CAST(REGEXP_REPLACE(col, '[\\(\\)\\*]', '') AS DOUBLE)`).*

2. **Supply Index (0-100)** = scaled sum of `capacity * trust_multiplier` (default capacity = 50 if null)
   * **Trust Score** (0-8 per facility): `specialties` contains pediatrics/immunization/vaccination center (+3); `procedure` contains vaccine administration/cold chain monitoring (+2); `equipment` contains vaccine refrigerator/cold chain cabinet (+2); `description` mentions child vaccination/immunization clinic (+1).
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
* `polio3_pct` (double)
* `measles1_pct` (double)
* `bcg_pct` (double)
* `demand_score` (double)
* `total_facilities` (long)
* `verified_vaccination_facilities` (long)
* `supply_index` (double)
* `care_gap_index` (double)
* `care_gap_status` (string)
