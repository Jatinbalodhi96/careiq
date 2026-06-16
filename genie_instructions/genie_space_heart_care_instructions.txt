# Genie Space Instructions: Cardiac Care Gap
**Scope:** `databricks_virtue_foundation_dataset_dais_2026.virtue_foundation_dataset` (Tables: `facilities`, `india_post_pincode_directory`, `nfhs_5_district_health_indicators`).

## Core Calculations
1. **Demand Score (0-100)** = `0.45*Hypertension + 0.25*Diabetes + 0.15*Lifestyle + 0.15*Obesity`
   * `Hypertension` = Avg of `w15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct` & `m15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct`
   * `Diabetes` = Avg of `w15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct` & `m15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct`
   * `Lifestyle` = Avg of `w15_plus_who_use_any_kind_of_tobacco_pct`, `m15_plus_who_use_any_kind_of_tobacco_pct`, `w15_plus_who_consume_alcohol_pct`, `m15_plus_who_consume_alcohol_pct`
   * `Obesity` = Avg of `women_age_15_49_years_who_are_overweight_obese_bmi_gte_25_0_pct` & `women_age_15_49_years_who_have_high_risk_whr_gte_0_85_pct`
   *(Cleanse string cols with `CAST(REGEXP_REPLACE(col, '[\\(\\)\\*]', '') AS DOUBLE)`).*

2. **Supply Index (0-100)** = scaled sum of `capacity * trust_multiplier` (default capacity = 50 if null)
   * **Trust Score** (0-8 per facility): `specialties` contains cardiology/cardiologist (+3); `procedure` contains ecg/echo/angioplasty (+2); `equipment` contains ecg/defibrillator/cardiac monitor (+2); `description` mentions cardiac/heart (+1).
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
* `hypertension_pct` (double)
* `diabetes_pct` (double)
* `obesity_pct` (double)
* `lifestyle_pct` (double)
* `demand_score` (double)
* `total_facilities` (long)
* `verified_cardiac_facilities` (long)
* `supply_index` (double)
* `care_gap_index` (double)
* `care_gap_status` (string)
