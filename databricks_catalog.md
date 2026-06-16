# Databricks Tables Catalog

Catalog: `databricks_virtue_foundation_dataset_dais_2026`\
Schema: `virtue_foundation_dataset`

## Table: `facilities`

| Column Name | Data Type | Description | Sample Value |
| --- | --- | --- | --- |
| `unique_id` | `string` | Unique identifier for the facility | `fa8ffca9-cb88-4ce6-b4f5-04ee5be45592` |
| `source_types` | `string` | Types of data sources indicating where this facility info was gathered | `null` |
| `source_ids` | `string` | Identifiers from original source datasets | `null` |
| `source_content_id` | `string` | Content ID associated with the source entry | `e135a955-3bc1-4d20-8f34-2b6cc14ce817` |
| `name` | `string` | Name of the healthcare facility | `Dr Satish Jindal's Child Care Clinic` |
| `organization_type` | `string` | Type of organization (e.g., facility, organization) | `facility` |
| `content_table_id` | `string` | ID of the content table referencing this facility | `e135a955-3bc1-4d20-8f34-2b6cc14ce817` |
| `phone_numbers` | `string` | List of phone numbers for the facility | `["+919988485101","+919988485101","+919988485101"]` |
| `officialPhone` | `string` | Primary/official phone number | `+919988485101` |
| `email` | `string` | Contact email address | `drsatishj@yahoo.com` |
| `websites` | `string` | List of websites or social media page URLs | `["http://drsatishjindal.com/","drsatishjindal.com","https://www.facebook.com/1369953236450419","h...` |
| `officialWebsite` | `string` | Primary official website URL | `drsatishjindal.com` |
| `yearEstablished` | `string` | The year the facility was established | `null` |
| `acceptsVolunteers` | `string` | Indicates if the facility accepts volunteer workers | `null` |
| `facebookLink` | `string` | Link to the official Facebook page | `https://www.facebook.com/1369953236450419` |
| `address_line1` | `string` | Primary street address details | `Sco 9` |
| `address_line2` | `string` | Secondary address details/landmarks | `Adjoining Bda Complex, Near Gurudwara Sahib` |
| `address_line3` | `string` | Additional address/neighborhood details | `Phase 1, Model Town` |
| `address_city` | `string` | City where the facility is located | `Bathinda` |
| `address_stateOrRegion` | `string` | State or region of the facility | `Punjab` |
| `address_zipOrPostcode` | `string` | ZIP or postal code | `151001` |
| `address_country` | `string` | Country name | `India` |
| `address_countryCode` | `string` | Two-letter country code (e.g., IN) | `IN` |
| `countries` | `string` | Associated countries list | `null` |
| `facilityTypeId` | `string` | Type of facility (e.g., clinic, hospital) | `clinic` |
| `operatorTypeId` | `string` | Operation model (e.g., private, public) | `private` |
| `affiliationTypeIds` | `string` | Identifiers for affiliations or parent organizations | `null` |
| `description` | `string` | Narrative description of services/facilities offered | `Offers consultations, day care services, and vaccinations.` |
| `area` | `string` | Area coverage details | `null` |
| `numberDoctors` | `string` | Number of registered doctors at the facility | `null` |
| `capacity` | `string` | Estimated patient or bed capacity | `null` |
| `specialties` | `string` | Specialized medical departments or areas of focus | `["pediatrics","familyMedicine","familyMedicine","pediatrics"]` |
| `procedure` | `string` | Procedures and services performed at the facility | `["Provides routine pediatric consultations","Administers pediatric vaccinations","Performs routin...` |
| `equipment` | `string` | Medical equipment and apparatus available | `["Stethoscope is used by clinicians during pediatric examinations"]` |
| `capability` | `string` | Facility capabilities and clinical services | `null` |
| `recency_of_page_update` | `string` | Recency or date of the last profile update | `null` |
| `distinct_social_media_presence_count` | `string` | Number of distinct social media networks where the facility has a presence | `2` |
| `affiliated_staff_presence` | `string` | Flag indicating if staff affiliation is documented | `true` |
| `custom_logo_presence` | `string` | Flag indicating if a custom logo is uploaded/present | `true` |
| `number_of_facts_about_the_organization` | `string` | Count of validated facts about the organization | `null` |
| `post_metrics_most_recent_social_media_post_date` | `string` | Date of the most recent social media post | `2024-10-26` |
| `post_metrics_post_count` | `string` | Count of social media posts | `1` |
| `engagement_metrics_n_followers` | `string` | Number of social media followers | `506` |
| `engagement_metrics_n_likes` | `string` | Number of social media page likes | `298` |
| `engagement_metrics_n_engagements` | `string` | Total social media engagement actions | `45` |
| `source` | `string` | Data ingestion source/pipeline | `kie` |
| `coordinates` | `string` | Geographic coordinates in GeoJSON format | `{"coordinates":[74.9603271484375,30.197689056396484],"type":"Point"}` |
| `latitude` | `double` | Geographic latitude coordinate | `30.197689056396484` |
| `longitude` | `double` | Geographic longitude coordinate | `74.9603271484375` |
| `cluster_id` | `string` | De-duplication or geographic cluster identifier | `08f42494965910b40313da1a4aad0adb` |
| `source_urls` | `string` | URLs of the sources used to verify the facility | `["http://drsatishjindal.com/","https://www.facebook.com/1369953236450419",null]` |

---

## Table: `india_post_pincode_directory`

| Column Name | Data Type | Description | Sample Value |
| --- | --- | --- | --- |
| `circlename` | `string` | Postal circle name | `Telangana Circle` |
| `regionname` | `string` | Postal region name | `Hyderabad Region` |
| `divisionname` | `string` | Postal division name | `Adilabad Division` |
| `officename` | `string` | Post office name | `Kothimir B.O` |
| `pincode` | `bigint` | 6-digit postal PIN code | `504273` |
| `officetype` | `string` | Type of post office (e.g. BO, SO, HO) | `BO` |
| `delivery` | `string` | Delivery status (e.g. Delivery, Non-Delivery) | `Delivery` |
| `district` | `string` | District where the post office is situated | `KUMURAM BHEEM ASIFABAD` |
| `statename` | `string` | State name in uppercase | `TELANGANA` |
| `latitude` | `string` | Geographic latitude coordinate | `19.3638689` |
| `longitude` | `string` | Geographic longitude coordinate | `79.5376658` |

---

## Table: `nfhs_5_district_health_indicators`

| Column Name | Data Type | Description | Sample Value |
| --- | --- | --- | --- |
| `district_name` | `string` | District name | `Nicobars` |
| `state_ut` | `string` | State ut | `Andaman & Nicobar Islands` |
| `households_surveyed` | `double` | Households surveyed | `882.0` |
| `women_15_49_interviewed` | `double` | Women 15 49 interviewed | `764.0` |
| `men_15_54_interviewed` | `double` | Men 15 54 interviewed | `125.0` |
| `female_population_age_6_years_and_above_ever_schooled_pct` | `double` | Percentage of female population age 6 years and above ever schooled (%) | `78.0` |
| `population_below_age_15_years_pct` | `double` | Percentage of population below age 15 years (%) | `23.0` |
| `sex_ratio_total_f_per_1000_m` | `double` | Sex ratio total f per 1000 m | `973.0` |
| `sex_ratio_at_birth_5y_f_per_1000_m` | `string` | Sex ratio at birth 5y f per 1000 m | `927 ` |
| `child_u5_whose_birth_was_civil_reg_pct` | `double` | Percentage of children under age 5 years_whose_birth_was_civil_reg (%) | `98.0` |
| `deaths_in_the_last_3_years_civil_reg_pct` | `string` | Percentage of deaths in the last 3 years civil reg (%) | `83.2 ` |
| `hh_electricity_pct` | `double` | Percentage of household electricity (%) | `97.9` |
| `hh_improved_water_pct` | `double` | Percentage of household improved_water (%) | `98.8` |
| `hh_use_improved_sanitation_pct` | `double` | Percentage of household use_improved_sanitation (%) | `83.5` |
| `households_using_clean_fuel_for_cooking_pct` | `double` | Percentage of households using clean fuel for cooking (%) | `56.9` |
| `households_using_iodized_salt_pct` | `double` | Percentage of households using iodized salt (%) | `99.4` |
| `hh_member_covered_health_insurance_pct` | `double` | Percentage of household member_covered_health_insurance (%) | `2.7` |
| `child_5y_who_attended_pre_primary_school_during_the_school_pct` | `string` | Percentage of child 5y who attended pre primary school during the school (%) | `(29.5)` |
| `women_age_15_49_who_are_literate_pct` | `double` | Percentage of women age 15 49 who are literate (%) | `87.5` |
| `women_age_15_49_with_10_or_more_years_of_schooling_pct` | `double` | Percentage of women age 15 49 with 10 or more years of schooling (%) | `53.5` |
| `w20_24_married_before_age_18_years_pct` | `string` | Percentage of women age 20-24 years_married_before_age_18_years (%) | `11.4 ` |
| `births_in_the_5_years_preceding_the_survey_that_are_birth_3_pct` | `string` | Percentage of births in the 5 years preceding the survey that are birth 3 (%) | `0.0 ` |
| `w15_19_who_were_already_mothers_or_pregnant_at_the_time_of_pct` | `string` | Percentage of women age 15-19 years_who_were_already_mothers_or_pregnant_at_the_time_of (%) | `1.8 ` |
| `w15_24_who_use_menstrual_hygiene_pct` | `double` | Percentage of w15 24 who use menstrual hygiene (%) | `100.0` |
| `fp_cm_w15_49_any_method_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: any_method (%) | `65.3` |
| `fp_cm_w15_49_modern_method_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: modern_method (%) | `57.2` |
| `fp_cm_w15_49_f_steril_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: f_steril (%) | `46.4` |
| `fp_cm_w15_49_m_steril_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: m_steril (%) | `0.0` |
| `fp_cm_w15_49_iud_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: iud (%) | `2.7` |
| `fp_cm_w15_49_pill_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: pill (%) | `2.0` |
| `fp_cm_w15_49_condom_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: condom (%) | `4.9` |
| `fp_cm_w15_49_injectables_pct` | `double` | Percentage of currently married women age 15-49 years using family planning: injectables (%) | `1.2` |
| `fp_unmet_total_cm_w15_49_7_pct` | `double` | Percentage of unmet need for family planning (total) among currently married women age 15-49 years (%) | `9.5` |
| `fp_unmet_spacing_cm_w15_49_7_pct` | `double` | Percentage of unmet need for family planning (spacing) among currently married women age 15-49 years (%) | `3.3` |
| `health_worker_ever_talked_to_female_non_users_about_family_pct` | `double` | Percentage of health worker ever talked to female non users about family (%) | `40.4` |
| `current_users_ever_told_about_side_effects_of_current_metho_pct` | `string` | Percentage of current users of modern family planning methods ever told about side effects (%) | `49.4 ` |
| `mothers_who_had_an_anc_visit_in_the_first_trimester_lb5y_pct` | `string` | Percentage of mothers who had an anc visit in the first trimester lb5y (%) | `62.8 ` |
| `mothers_who_had_at_least_4_anc_visits_lb5y_pct` | `string` | Percentage of mothers who had at least 4 anc visits lb5y (%) | `71.7 ` |
| `mothers_whose_last_birth_was_protected_against_neo_tetanus_pct` | `string` | Percentage of mothers whose last birth was protected against neo tetanus (%) | `78.0 ` |
| `mothers_who_consumed_ifa_for_100_days_or_more_when_they_wer_pct` | `string` | Percentage of mothers who consumed ifa for 100 days or more when they wer (%) | `72.6 ` |
| `mothers_who_consumed_ifa_for_180_days_or_more_when_they_wer_pct` | `string` | Percentage of mothers who consumed ifa for 180 days or more when they wer (%) | `43.9 ` |
| `registered_pregnancies_for_which_the_mother_received_a_mcp_pct` | `string` | Percentage of registered pregnancies for which the mother received a mcp (%) | `97.9 ` |
| `mothers_who_received_pnc_from_a_doctor_nurse_lhv_anm_midwif_pct` | `string` | Percentage of mothers who received pnc from a doctor nurse lhv anm midwif (%) | `85.1 ` |
| `average_out_of_pocket_expenditure_per_delivery_in_a_public_fac` | `string` | Average out-of-pocket expenditure per delivery in a public health facility (INR) | `2278 ` |
| `children_born_at_home_who_were_taken_to_a_health_facility_f_pct` | `string` | Percentage of children born at home who were taken to a health facility f (%) | `*` |
| `children_who_received_pnc_from_a_doctor_nurse_lhv_anm_midwi_pct` | `string` | Percentage of children who received pnc from a doctor nurse lhv anm midwi (%) | `92.5 ` |
| `institutional_birth_5y_pct` | `double` | Percentage of institutional births in the 5 years preceding the survey (%) | `97.8` |
| `institutional_birth_in_public_facility_5y_pct` | `double` | Percentage of institutional births in a public health facility in the 5 years preceding the survey (%) | `96.7` |
| `home_birth_that_were_conducted_by_skilled_hp_5y_10_pct` | `double` | Percentage of home births conducted by skilled health personnel in the 5 years preceding the survey (%) | `0.8` |
| `births_attended_by_skilled_hp_5y_10_pct` | `double` | Percentage of births attended by skilled health personnel in the 5 years preceding the survey (%) | `98.6` |
| `births_delivered_by_csection_5y_pct` | `double` | Percentage of births delivered by caesarean section in the 5 years preceding the survey (%) | `11.5` |
| `births_in_a_private_fac_that_were_delivered_by_csection_5y_pct` | `string` | Percentage of births in a private health facility delivered by caesarean section in the 5 years preceding the survey (%) | `*` |
| `births_in_a_public_fac_that_were_delivered_by_csection_5y_pct` | `string` | Percentage of births in a public health facility delivered by caesarean section in the 5 years preceding the survey (%) | `10.7 ` |
| `child_12_23m_fully_vaccinated_based_on_information_from_eit_pct` | `string` | Percentage of children age 12-23 months_fully_vaccinated_based_on_information_from_eit (%) | `(64.2)` |
| `child_12_23m_fully_vaccinated_based_on_information_from_vax_pct` | `string` | Percentage of children age 12-23 months_fully_vaccinated_based_on_information_from_vax (%) | `(94.1)` |
| `child_12_23m_who_have_received_bcg_pct` | `string` | Percentage of children age 12-23 months_who_have_received_bcg (%) | `(80.4)` |
| `child_12_23m_who_have_received_3_doses_of_polio_vaccine_pct` | `string` | Percentage of children age 12-23 months_who_have_received_3_doses_of_polio_vaccine (%) | `(69.1)` |
| `child_12_23m_who_have_received_3_doses_of_penta_or_dpt_vacc_pct` | `string` | Percentage of children age 12-23 months_who_have_received_3_doses_of_penta_or_dpt_vacc (%) | `(71.9)` |
| `child_12_23m_who_have_received_the_first_dose_of_mcv_mcv_pct` | `string` | Percentage of children age 12-23 months_who_have_received_the_first_dose_of_mcv_mcv (%) | `(67.3)` |
| `child_24_35m_who_have_received_a_second_dose_of_mcv_mcv_pct` | `string` | Percentage of children age 24-35 months_who_have_received_a_second_dose_of_mcv_mcv (%) | `(20.7)` |
| `child_12_23m_who_have_received_3_doses_of_rotavirus_vaccine_pct` | `string` | Percentage of children age 12-23 months_who_have_received_3_doses_of_rotavirus_vaccine (%) | `(3.1)` |
| `child_12_23m_who_have_received_3_doses_of_penta_or_hepatiti_pct` | `string` | Percentage of children age 12-23 months_who_have_received_3_doses_of_penta_or_hepatiti (%) | `(68.6)` |
| `child_9_35m_who_received_a_vit_a_in_the_last_6_months_pct` | `string` | Percentage of children age 9-35 months_who_received_a_vit_a_in_the_last_6_months (%) | `94.9 ` |
| `child_12_23m_who_received_most_of_their_vaccinations_in_a_p_pct` | `string` | Percentage of children age 12-23 months_who_received_most_of_their_vaccinations_in_a_p (%) | `(100.0)` |
| `child_12_23m_who_received_most_of_their_vaccinations_in_a_2_pct` | `string` | Percentage of children age 12-23 months_who_received_most_of_their_vaccinations_in_a_2 (%) | `(0.0)` |
| `prev_diarrhoea_2wk_child_u5_pct` | `double` | Percentage of prevalence of diarrhoea in the 2 weeks preceding the survey among children under age 5 years (%) | `5.7` |
| `children_with_diarrhoea_2wk_who_received_oral_rehydration_s_pct` | `string` | Percentage of children with diarrhoea 2wk who received oral rehydration s (%) | `*` |
| `children_with_diarrhoea_2wk_who_received_zinc_child_u5_pct` | `string` | Percentage of children with diarrhoea 2wk who received zinc child u5 (%) | `*` |
| `children_with_diarrhoea_2wk_taken_to_a_health_facility_or_h_pct` | `string` | Percentage of children with diarrhoea 2wk taken to a health facility or h (%) | `*` |
| `children_prev_symptoms_of_acute_respiratory_infection_ari_2_pct` | `double` | Percentage of children prev symptoms of acute respiratory infection ari 2 (%) | `1.8` |
| `children_with_fever_or_symptoms_of_ari_2wk_taken_to_a_healt_pct` | `string` | Percentage of children with fever or symptoms of ari 2wk taken to a healt (%) | `(85.7)` |
| `children_under_age_3_years_breastfed_within_one_hour_of_bir_pct` | `string` | Percentage of children under age 3 years breastfed within one hour of bir (%) | `55.4 ` |
| `child_u6m_exclusively_breastfed_pct` | `string` | Percentage of infants under age 6 months_exclusively_breastfed (%) | `*` |
| `child_6_8m_receiving_solid_or_semi_solid_food_and_breastmil_pct` | `string` | Percentage of children age 6-8 months_receiving_solid_or_semi_solid_food_and_breastmil (%) | `*` |
| `breastfeeding_child_6_23m_receiving_an_adequate_diet16_17_pct` | `string` | Percentage of breastfeeding child 6 23m receiving an adequate diet16 17 (%) | `(19.4)` |
| `non_breastfeeding_child_6_23m_receiving_an_adequate_diet16_pct` | `string` | Percentage of non breastfeeding child 6 23m receiving an adequate diet16 (%) | `*` |
| `total_child_6_23m_receiving_an_adequate_diet16_17_pct` | `string` | Percentage of total child 6 23m receiving an adequate diet16 17 (%) | `(18.7)` |
| `child_u5_who_are_stunted_height_for_age_18_pct` | `string` | Percentage of children under age 5 years_who_are_stunted_height_for_age_18 (%) | `21.6 ` |
| `child_u5_who_are_wasted_weight_for_height_18_pct` | `string` | Percentage of children under age 5 years_who_are_wasted_weight_for_height_18 (%) | `15.7 ` |
| `child_u5_who_are_severe_wasted_weight_for_height_19_pct` | `string` | Percentage of children under age 5 years_who_are_severe_wasted_weight_for_height_19 (%) | `7.8 ` |
| `child_u5_who_are_underweight_weight_for_age_18_pct` | `string` | Percentage of children under age 5 years_who_are_underweight_weight_for_age_18 (%) | `24.6 ` |
| `child_u5_who_are_overweight_weight_for_height_20_pct` | `string` | Percentage of children under age 5 years_who_are_overweight_weight_for_height_20 (%) | `1.5 ` |
| `women_age_15_49_years_whose_bmi_bmi_is_underweight_bmi_lt_1_pct` | `double` | Percentage of women age 15 49 years whose bmi bmi is underweight bmi lt 1 (%) | `8.2` |
| `women_age_15_49_years_who_are_overweight_obese_bmi_gte_25_0_pct` | `double` | Percentage of women age 15 49 years who are overweight obese bmi gte 25 0 (%) | `39.1` |
| `women_age_15_49_years_who_have_high_risk_whr_gte_0_85_pct` | `double` | Percentage of women age 15 49 years who have high risk whr gte 0 85 (%) | `62.5` |
| `child_6_59m_who_are_anaemic_lt_11_0_g_dl_22_pct` | `string` | Percentage of child 6 59m who are anaemic lt 11 0 g dl 22 (%) | `37.7 ` |
| `non_pregnant_w15_49_who_are_anaemic_lt_12_0_g_dl_22_pct` | `double` | Percentage of non pregnant w15 49 who are anaemic lt 12 0 g dl 22 (%) | `38.4` |
| `pregnant_w15_49_who_are_anaemic_lt_11_0_g_dl_22_pct` | `string` | Percentage of pregnant w15 49 who are anaemic lt 11 0 g dl 22 (%) | `*` |
| `all_w15_49_who_are_anaemic_pct` | `double` | Percentage of all w15 49 who are anaemic (%) | `38.3` |
| `all_w15_19_who_are_anaemic_pct` | `string` | Percentage of all w15 19 who are anaemic (%) | `48.0 ` |
| `women_age_15_years_and_above_with_high_141_160_mg_dl_blood_pct` | `double` | Percentage of women age 15 years and above with high 141 160 mg dl blood (%) | `7.4` |
| `w15_plus_with_very_high_gt_160_mg_dl_blood_sugar_pct` | `double` | Percentage of women age 15 years and above with very high (>160 mg/dl) blood sugar (%) | `3.9` |
| `w15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct` | `double` | Percentage of women age 15 years and above with high or very high (>140 mg/dl) blood sugar or taking medicine to control blood sugar (%) | `13.1` |
| `m15_plus_with_high_141_160_mg_dl_blood_sugar_pct` | `double` | Percentage of men age 15 years and above_with_high_141_160_mg_dl_blood_sugar (%) | `9.6` |
| `men_age_15_years_and_above_with_very_high_gt_160_mg_dl_bloo_pct` | `double` | Percentage of men age 15 years and above with very high gt 160 mg dl bloo (%) | `4.4` |
| `m15_plus_with_high_or_very_high_gt_140_mg_dl_blood_sugar_or_pct` | `double` | Percentage of men age 15 years and above with high or very high (>140 mg/dl) blood sugar or taking medicine to control blood sugar (%) | `15.4` |
| `w15_plus_with_mildly_high_bp_sys_140_159_mmhg_and_or_dia_90_pct` | `double` | Percentage of women age 15 years and above with mildly high blood pressure (Systolic 140-159 mmHg and/or Diastolic 90-99 mmHg) (%) | `23.2` |
| `w15_plus_with_moderately_or_severely_high_bp_sys_gte_160_mm_pct` | `double` | Percentage of women age 15 years and above with moderately or severely high blood pressure (Systolic >=160 mmHg and/or Diastolic >=100 mmHg) (%) | `8.5` |
| `w15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct` | `double` | Percentage of women age 15 years and above with high blood pressure (Systolic >=140 mmHg and/or Diastolic >=90 mmHg) or taking medicine to control blood pressure (%) | `35.4` |
| `m15_plus_with_mildly_high_bp_sys_140_159_mmhg_and_or_dia_90_pct` | `double` | Percentage of men age 15 years and above with mildly high blood pressure (Systolic 140-159 mmHg and/or Diastolic 90-99 mmHg) (%) | `32.9` |
| `m15_plus_with_moderately_or_severely_high_bp_sys_gte_160_mm_pct` | `double` | Percentage of men age 15 years and above with moderately or severely high blood pressure (Systolic >=160 mmHg and/or Diastolic >=100 mmHg) (%) | `11.1` |
| `m15_plus_with_high_bp_sys_gte_140_mmhg_and_or_dia_gte_90_mm_pct` | `double` | Percentage of men age 15 years and above with high blood pressure (Systolic >=140 mmHg and/or Diastolic >=90 mmHg) or taking medicine to control blood pressure (%) | `47.0` |
| `women_age_30_49_years_ever_undergone_a_cervical_screen_pct` | `double` | Percentage of women age 30 49 years ever undergone a cervical screen (%) | `13.4` |
| `women_age_30_49_years_ever_undergone_a_breast_exam_pct` | `double` | Percentage of women age 30 49 years ever undergone a breast exam (%) | `13.2` |
| `women_age_30_49_years_ever_undergone_an_oral_cancer_exam_pct` | `double` | Percentage of women age 30 49 years ever undergone an oral cancer exam (%) | `5.4` |
| `w15_plus_who_use_any_kind_of_tobacco_pct` | `double` | Percentage of women age 15 years and above who use any kind of tobacco (%) | `63.5` |
| `m15_plus_who_use_any_kind_of_tobacco_pct` | `double` | Percentage of men age 15 years and above who use any kind of tobacco (%) | `76.8` |
| `w15_plus_who_consume_alcohol_pct` | `double` | Percentage of women age 15 years and above who consume alcohol (%) | `29.6` |
| `m15_plus_who_consume_alcohol_pct` | `double` | Percentage of men age 15 years and above who consume alcohol (%) | `64.5` |

---

