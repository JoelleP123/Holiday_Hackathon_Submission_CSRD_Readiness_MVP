#hackathon demo

# CSRD Supplier Readiness MVP (Notebook Demo)
# Workflow: Intake → Tags → Calculate Readiness →Readiness Brief

# Purpose
"""
The purpose of this product is to create a lightweight Supplier Baseline Screening Tool
that helps suppliers understand buyer-driven sustainability and human-rights expectations,
specifically through a CSRD (EU) lens. This product screens supplier readiness to be onboarded
to buyer platforms, identifies weak points for triage before risk is metabolized, and
prioritizes next steps for investment of resources.
"""

## Note: This repo is illustrative; commercial use requires agreement

# Note: This repo is a logic MVP only

### Note: This notebook demonstrates the AI reasoning layer of the product

## Boundaries of this tool:
## Decision support only
## Not legal advice
## Not a compliance or reporting determination

## Design principles applied
## multiple choice only
## no legal interpretation required from the supplier
## aligned to what buyers actually screen for first under CSRD / HRDD
## safe for Global South and SME suppliers




INTAKE_QUESTIONS = {
  "Where is your company primarily operating?": ["EU", "Non-EU", "Both"],
  "Do you sell directly or indirectly to EU-based companies or investors?": ["Yes, directly", "Yes, indirectly", "Not sure"],
  "What best describes your company size?": ["Micro", "Small", "Medium", "Large"],
  "Which sector best fits your operations?": [
      "Manufacturing (components / sub-assemblies)",
      "Processing / transformation (e.g. food, materials)",
      "Agriculture / farming",
      "Forestry / timber",
      "Fisheries / aquaculture",
      "Mining / extractives",
      "Construction / infrastructure",
      "Logistics / transport (road, sea, air)",
      "Warehousing / distribution",
      "Energy production or supply",
      "Waste management / recycling",
      "Chemicals / industrial inputs",
      "Textiles / apparel / footwear",
      "Electronics / electrical equipment",
      "Packaging / materials",
      "IT / digital services",
      "Professional services",
      "Facilities management / cleaning / security",
      "Other services (non-industrial)"
  ],
  "Which best describes your role in the value chain today?": ["Primarily a supplier to other companies", "Both a supplier and a buyer", "Primarily a buyer (procures from others)"],

  "How complex is your supply chain?": ["Mostly direct suppliers", "Mix of direct and indirect", "Highly multi-tiered"],
  "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": ["Yes", "Some operations", "No", "Not sure"],
  "Are labor conditions a material issue in your operations or sourcing?": ["Yes", "Somewhat", "No"],
  "Have buyers or partners asked you about environmental or climate-related topics?": ["Yes", "Somewhat", "No"],
  "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": ["Climate / emissions", "Energy use", "Water use", "Waste / materials", "Biodiversity / land use", "Other issue", "Not applicable", "Not specified / unclear"],

  "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": ["Yes", "No", "Expected soon"],
  "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": ["Yes, significantly more detailed", "Yes, somewhat more detailed", "No change / Not applicable"],
  "What do you think prompted these requests?": ["CSRD regulations", "Other new regulation or law (not just CSRD)", "Buyer policy update", "Investor requirement", "Unclear / not explained"],
  "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": ["Yes, explicitly", "Yes, indirectly (e.g. “new EU requirements”)", "No", "Not sure"],

  "Who is primarily responsible for sustainability or social impact topics internally?": ["Dedicated role/team", "Shared responsibility", "Legal / compliance only", "No clear owner" ],
  "Do you have written policies related to the environment, sustainability and labor?": ["Yes", "Draft / informal", "No"],
  "Do you currently track any sustainability or social data?": ["Yes, structured", "Informal / ad hoc", "No"],
  "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": ["Confident", "Somewhat confident", "Not confident"],
}


## Cell — Map sentences to stable internal keys

QUESTION_TO_KEY = {
  "Where is your company primarily operating?": "operates_in_eu",
  "Do you sell directly or indirectly to EU-based companies or investors?": "sells_to_eu_buyers",
  "What best describes your company size?": "company_size",
  "Which sector best fits your operations?": "sector",
  "Which best describes your role in the value chain today?": "value_chain_role",

  "How complex is your supply chain?": "supply_chain_complexity",
  "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": "hr_risk_region",
  "Are labor conditions a material issue in your operations or sourcing?": "labor_material",
  "Have buyers or partners asked you about environmental or climate-related topics?": "env_asked",
  "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": "env_topics",

  "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": "recent_esg_requests",
  "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "more_detailed_requests",
  "What do you think prompted these requests?": "request_driver",
  "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": "csrd_mentioned",

  "Who is primarily responsible for sustainability or social impact topics internally?": "internal_owner",
  "Do you have written policies related to the environment, sustainability and labor?": "policy_status",
  "Do you currently track any sustainability or social data?": "data_tracking",
  "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": "confidence",

}

answers_by_question = {
  "Where is your company primarily operating?": "Non-EU",
  "Do you sell directly or indirectly to EU-based companies or investors?": "Yes, indirectly",
  "What best describes your company size?": "Medium",
  "Which sector best fits your operations?": "Manufacturing (components / sub-assemblies)",
  "Which best describes your role in the value chain today?": "Primarily a supplier to other companies",

  "How complex is your supply chain?": "Highly multi-tiered",
  "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": "Yes",
  "Are labor conditions a material issue in your operations or sourcing?": "Somewhat",
  "Have buyers or partners asked you about environmental or climate-related topics?": "Yes",
  "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": "Not specified / unclear",

  "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": "Yes",
  "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "Yes, significantly more detailed",
  "What do you think prompted these requests?": "Unclear / not explained",
  "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": "Yes, indirectly (e.g. “new EU requirements”)",

  "Who is primarily responsible for sustainability or social impact topics internally?": "No clear owner",
  "Do you have written policies related to the environment, sustainability and labor?": "No",
  "Do you currently track any sustainability or social data?": "Informal / ad hoc",
  "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": "Not confident",
}

# Cell — Normalize into internal keys

def normalize_answers(answers_by_question: dict) -> dict:
    a = {}
    for q, ans in answers_by_question.items():
        key = QUESTION_TO_KEY.get(q)
        if key:
            a[key] = ans
    return a

a = normalize_answers(answers_by_question)
print("Normalized answers keys:", list(a.keys()))


def derive_tags(intake: dict) -> list:
    tags = []

# Cell - Logic for Intake form

# --- Section A ---

    # 1. EU-linked buyers may request more information
    if intake.get("operates_in_eu") in {"Both", "EU"}:
        tags.append("CSRD_CASCADE_SIGNAL")
    # CONTEXT NOTE: EU-linked buyers may request information due to reporting/risk expectations.

    # 2. Seller is not sure about selling to EU buyers -> opacity + confidence risk
    if intake.get("sells_to_eu_buyers") == "Not sure":
        tags.append("BUYER_OPACITY_RISK")
        tags.append("SUPPLIER_CONFIDENCE_LOW")

    # 3. Large company with EU or mixed operations -> CSRD pressure signal
    if (intake.get("company_size") == "Large"
            and intake.get("operates_in_eu") in {"Both", "EU"}):
        tags.append("CSRD_CASCADE_SIGNAL")
## CONTEXT NOTE (non-EU + EU exposure): EU-linked buyers may request more information from larger suppliers  to meet evolving sustainability reporting and risk expectations.

 # 4. Sector-based logic placeholder (unimplemented)
    # if intake.get("sector") == "Some sector":
    #     tags.append("...")

    # 5. Dual role pressure if the supplier has both supplier and buyer roles
    if intake.get("value_chain_role") == "Both a supplier and a buyer":
        tags.append("DUAL_ROLE_PRESSURE")

    # --- Section B ---

    # 6. Supply chain complexity signals multi-tier pressure/opacities
    complexity = intake.get("supply_chain_complexity")
    if complexity == "Mix of direct and indirect":
        tags.append("DUAL_ROLE_PRESSURE")
    if complexity == "Highly multi-tiered":
        tags.append("BUYER_OPACITY_RISK")
        tags.append("HRDD_RELEVANCE_HIGH")

    # 7. High risk sourcing areas drive HRDD relevance and opacity risks
    if intake.get("hr_risk_region") in {"Yes", "Some operations", "Not sure"}: # Corrected key
        tags.append("HRDD_RELEVANCE_HIGH")
        tags.append("BUYER_OPACITY_RISK")

    # 8. Labor issues materiality drives HRDD relevance
    if intake.get("labor_material") in {"Yes", "Somewhat"}: # Corrected key and comparison
        tags.append("HRDD_RELEVANCE_HIGH")

    # --- Section C ---

    # 9. No environmental requests -> documentation light
    if intake.get("env_asked") == "No": # Corrected key
        tags.append("DOCUMENTATION_LIGHT")
## to add in later as a note in the intake:
## Use whenever buyer pressure = Yes or Expected soon:
## WHY YOU’RE BEING ASKED:
## These requests often increase when buyers update internal policies, respond to investor expectations, or adapt to changing EU sustainability requirements. Suppliers are frequently not given clear explanations—so uncertainty itself becomes a risk factor.

# 10. Unspecified environmental topics -> opacity risk
    if intake.get("env_topics") in {"Not specified / unclear", "Not Specified/Unclear"}: # Corrected key
        tags.append("BUYER_OPACITY_RISK")
# if intake.get("which_topic_environment") ==

 # 11. No recent info request -> governance gap
    if intake.get("recent_esg_requests") == "No": # Corrected key
        tags.append("GOVERNANCE_OWNER_GAP")
## to add in later as a note for the intake:
## Use whenever buyer pressure = Yes or Expected soon:
## WHY YOU’RE BEING ASKED:
## These requests often increase when buyers update internal policies, respond to investor expectations, or adapt to changing EU sustainability requirements. Suppliers are frequently not given clear explanations—so uncertainty itself becomes a risk factor.

# 12. More detailed requests lower supplier confidence
    if intake.get("more_detailed_requests") in {
        "Yes, significantly more detailed", "Yes, somewhat more detailed"
    }: # Corrected key
        tags.append("SUPPLIER_CONFIDENCE_LOW")
## TBD check later = if intake.get("info_request_more_detailed") == "Yes, more detailed" or "Yes, somewhat more detailed":
## TBD check later = tags.append("CSRD_CASCADE_SIGNAL")

# 13. Reason for requests: CSRD vs unclear explanations
    prompt = intake.get("request_driver") # Corrected key
    if prompt == "CSRD regulations": # Corrected string value
        tags.append("CSRD_CASCADE_SIGNAL")
    if prompt == "Unclear / not explained": # Corrected string value
        tags.append("BUYER_OPACITY_RISK")
        tags.append("SUPPLIER_CONFIDENCE_LOW")
## “Assume that suppliers may be receiving requests influenced by regulatory changes even when legal obligations do not formally apply to them.”

# 14. CSRD mentioned or not
    csrd_req = intake.get("csrd_mentioned") # Corrected key
    if csrd_req in {"Yes, explicitly", "Yes, indirectly (e.g. “new EU requirements”)", "Yes, indirectly"}:
        tags.append("CSRD_CASCADE_SIGNAL")
    if csrd_req == "Not sure":
        tags.append("SUPPLIER_CONFIDENCE_LOW")

    # --- Section D ---

    # 15. Owner gaps drive low confidence
    owner_status = intake.get("internal_owner") # Correct key
    if owner_status == "No clear owner":
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if owner_status in {"Shared responsibility", "Legal / compliance only", "No clear owner"}: # Corrected set
        tags.append("SUPPLIER_CONFIDENCE_LOW")

# 16. Policy status
    policy_status = intake.get("policy_status") # Corrected key
    if policy_status == "Draft / informal":
        tags.append("HRDD_RELEVANCE_HIGH")
    if policy_status in {"Draft / informal", "No"}: # Corrected set
        tags.append("DOCUMENTATION_LIGHT")
    if policy_status == "No":
        tags.append("ENVIRONMENTAL_BASELINE_GAP")
        tags.append("GOVERNANCE_OWNER_GAP")
## Note: to ammend logic of question later:
## No, if other questions are flagged: HRDD_RELEVANCE_HIGH

# 17. Data tracking
    data_status = intake.get("data_tracking") # Correct key
    if data_status in {"No", "Informal / ad hoc"}: # Corrected set
        tags.append("ENVIRONMENTAL_BASELINE_GAP")
    if data_status == "No":
        tags.append("GOVERNANCE_OWNER_GAP")
        tags.append("DOCUMENTATION_LIGHT")

 # 18. Confidence level
    if intake.get("confidence") == "Not confident": # Corrected key
        tags.append("GOVERNANCE_OWNER_GAP")

    # Example rule for future use:
    # if intake.get("has_written_policies") == "No" and intake.get("tracks_sustainability_data") == "No":
    #     tags.append("ENVIRONMENTAL_BASELINE_GAP")
    return tags


# Example usage:
# normalized_intake = {
#     "operates_in_eu": "EU",
#     "sells_to_eu_buyers": "Yes, directly",
#     "company_size": "Large",
#     "value_chain_role": "Both a supplier and a buyer",
#     "supply_chain_complexity": "Highly multi-tiered",
#     "hr_risk_region": "Yes",
#     "labor_material": "Yes",
#     "env_asked": "No",
#     "env_topics": "Not specified / unclear",
#     "recent_esg_requests": "No",
#     "more_detailed_requests": "Yes, significantly more detailed",
#     "request_driver": "CSRD regulations",
#     "csrd_mentioned": "Yes, explicitly",
#     "internal_owner": "No clear owner",
#     "policy_status": "No",
#     "data_tracking": "No",
#     "confidence": "Not confident",
# }
# tags = derive_tags(normalized_intake)
# for tag in tags:
#     print(f"{tag}: {TAG_DEFS.get(tag, '(no definition)')}")


# --- Run tag derivation ---
applied_tags = derive_tags(a)

#Additional Notes:
# Print tag descriptions  (won't crash if TAG_DEFS missing a key)
# Removed the reference to TAG_DEFS which is defined in a later cell, to avoid NameError if run out of order.
# Assuming TAG_DEFS will be defined globally or passed. For now, just print the tags.

for t in applied_tags:
    print(f"{t}") # Removed TAG_DEFS.get to avoid NameError for now

print("\nApplied tags list:", applied_tags)




# --- Convert list -> dict for scoring (True/False flags) ---
tags = {t: True for t in applied_tags}

# --- Scoring + reasons ---
score = 0
reasons = []

if tags.get("CSRD_CASCADE_SIGNAL"):
    score += 2
    reasons.append("explanation 1")

if tags.get("BUYER_OPACITY_RISK"):
    score += 2
    reasons.append("explanation 2")

if tags.get("HRDD_RELEVANCE_HIGH"):
    score += 1
    reasons.append("explanation 3")

if tags.get("GOVERNANCE_OWNER_GAP"):
    score += 1
    reasons.append("explanation 4")

if tags.get("ENVIRONMENTAL_BASELINE_GAP"):
    score += 1
    reasons.append("explanation 5")

if tags.get("POLICY_LIGHT"):
    score += 1
    reasons.append("explanation 6")

if tags.get("DUAL_ROLE_PRESSURE"):
    score += 1
    reasons.append("explanation 7")

if tags.get("SUPPLIER_CONFIDENCE_LOW"):
    score += 1
    reasons.append("explanation 8")

# --- Band logic ---
if score >= 4:
    band = "HIGH: CSRD readiness triage recommended"
elif score >= 2:
    band = "MEDIUM: Some CSRD-driven pressure likely"
else:
    band = "LOW: Limited signal of CSRD-driven pressure"

# --- Output ---
print("\nScore:", score)
print("Band:", band)
print("Why:")
if reasons:
    for r in reasons:
        print("-", r)
else:
    print("- (no reasons triggered; check whether applied_tags is empty)")


## Additional tags to be given scores later (note)
## "EU_EXPOSURE_NON_EU": "Non-EU supplier exposed to EU buyer/investor requests.",
## "RISING_BUYER_DEMAND": "Requests are increasing in detail/frequency.",
## "OWNER_GAP": "No clear internal owner for ESG/HR topics.",
## "DATA_GAP": "Sustainability/social data tracking is missing or ad hoc.",
## "ENV_RISK": "Environmental topics are being requested by buyers.",

              ## Cell: Run screenings


def run_screening(tags: dict) -> dict:
    """
    tags: dict like {"CSRD_CASCADE_SIGNAL": True, "DATA_GAP": False, ...}
    returns: dict with keys: readiness_level, tags, interpretation, next_steps
    """

    # Keep only tags that are True
    active_tags = [k for k, v in tags.items() if v is True]

    # ---- Simple scoring model (edit weights TBD) ----
    weights = {
        "CSRD_CASCADE_SIGNAL": 1,
        "EU_EXPOSURE_NON_EU": 1,
        "RISING_BUYER_DEMAND": 1,
        "POLICY_GAP": 2,
        "DATA_GAP": 2,
        "LABOR_RISK_CONTEXT": 2,
        "OWNER_GAP": 2,
    }

    score = sum(weights.get(t, 0) for t in active_tags)

    # ---- Readiness level thresholds ----
    # Lower score = more ready; higher score = more gaps/pressure
    if score <= 2:
        readiness_level = "GREEN — Low risk / early readiness"
        interpretation = (
            "You have limited immediate pressure signals and/or only minor capability gaps. "
            "Focus on documentation hygiene and staying ahead of buyer requests."
        )
    elif score <= 6:
        readiness_level = "AMBER — Moderate risk / needs structuring"
        interpretation = (
            "You’re seeing buyer/regulatory pressure signals and some internal gaps. "
            "Prioritize ownership, policy basics, and minimum viable data tracking."
        )
    else:
        readiness_level = "RED — High risk / likely exposure"
        interpretation = (
            "You have multiple pressure signals and several internal capability gaps. "
            "This is where suppliers often get caught flat-footed during buyer requests, audits, or tender processes. "
            "Move quickly to establish ownership, baseline policies, and auditable evidence."
        )

    # Next steps generator (based on which gaps are active)
    next_steps = []

    if "OWNER_GAP" in active_tags:
        next_steps.append("Assign a single accountable owner for sustainability/compliance requests (name + role).")

    if "POLICY_GAP" in active_tags:
        next_steps.append("Draft a minimum policy set (environment + labor/human rights) with approval + version control.")

    if "DATA_GAP" in active_tags:
        next_steps.append("Start a basic data baseline (energy, emissions scope assumptions, water, waste) in a simple tracker.")

    if "LABOR_RISK_CONTEXT" in active_tags:
        next_steps.append("Map labor risk in sourcing (countries/commodities) and set a lightweight supplier due diligence checklist.")

    if "CSRD_CASCADE_SIGNAL" in active_tags or "RISING_BUYER_DEMAND" in active_tags:
        next_steps.append("Create a buyer-response pack: 1-page overview + evidence folder + standard Q&A.")

    if "EU_EXPOSURE_NON_EU" in active_tags:
        next_steps.append("Identify EU-linked customers and expected reporting asks; align your evidence to what they request most.")

    # Always include an “artifact” step so this becomes reusable IP
    next_steps.append("Package outputs into a reusable 'Readiness Folder' (policies, tracker, evidence, Q&A) for future requests.")

#note : to review / ammend "next steps" list

    return {
        "readiness_level": readiness_level,
        "tags": active_tags,
        "interpretation": interpretation,
        "next_steps": next_steps,
    }
