# Prompt Design Documentation

## Objective

Generate a structured shift handover report from Discord messages and ticketing system records.

---

## Prompt Strategy

The model receives:

1. Discord chat messages
2. Ticket system data

The prompt instructs the model to:

* Analyze only provided data
* Merge duplicate incidents
* Avoid repeated issues
* Produce concise professional summaries
* Include references where possible

---

## Required Output Structure

```markdown
## Open Issues

## Watch Items

## Recent Fixes

## Pending Actions
```

---

## Watch Item Guidelines

Watch Items should:

* Identify systems requiring monitoring
* Explain why monitoring is necessary
* Provide actionable recommendations

Example:

* Monitor database stability after restart to ensure timeout issues do not recur.
* Monitor CPU utilization because usage exceeded safe thresholds.

---

## Deduplication Strategy

The AI merges incidents appearing in both:

* Discord exports
* Ticket records

into a single issue description.

---

## Validation Loop

Generated output is validated for required markdown sections.

If any section is missing:

1. Validation fails
2. Prompt is strengthened
3. Generation is retried

This creates a lightweight agent loop.
