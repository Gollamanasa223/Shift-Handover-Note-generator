# AI Usage Documentation

## Model Used

Provider:

* Groq

Model:

* Llama 3.3 70B Versatile

---

## Purpose of AI

The AI model is responsible for:

* Understanding operational events
* Summarizing incidents
* Deduplicating issues
* Categorizing activities
* Generating structured handover reports

---

## Why AI Was Used

Traditional rule-based systems struggle to:

* Understand conversational context
* Merge duplicate incident descriptions
* Produce human-readable summaries

Large Language Models provide:

* Better summarization
* Context understanding
* Improved report quality

---

## Validation Process

After generation:

1. Output is checked for required sections:

   * Open Issues
   * Watch Items
   * Recent Fixes
   * Pending Actions

2. If validation fails:

   * The report is regenerated using a stricter prompt.

This creates a feedback loop that improves reliability.

---

## Limitations

* AI output may occasionally require human review.
* Quality depends on input data quality.
* The model does not access external operational systems.

---

## Human Oversight

Generated reports should be reviewed by support engineers before operational use in production environments.

AI assists decision-making but does not replace human judgment.
