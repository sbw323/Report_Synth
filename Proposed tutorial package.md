## Proposed tutorial package

Create the tutorial as five documents:

1. **`01_quickstart.md`**
   A shortest-path run that proves the package works.

2. **`02_structured_report_workflow.md`**
   The main tutorial showing how to generate a planned, styled, validated report.

3. **`03_report_plan_guide.md`**
   A focused guide to writing the report plan JSON.

4. **`04_style_sheet_guide.md`**
   A focused guide to style constraints and validation behavior.

5. **`05_validation_metrics_and_troubleshooting.md`**
   A guide to failed runs, retries, claim tracing, lifecycle transitions, and final metrics.

## Reader promise for the main tutorial

Use one sentence like this at the top:

> This tutorial shows how to turn a small source-document set into a structured synthesized report using a report plan, a style sheet, evidence retrieval, section-level generation, validation, claim extraction, and final run metrics.

That promise matches the architecture in the package: the report plan is the highest-authority input, the style sheet is the next control layer, prompt assembly is section-driven, and the run ends with metrics and claim tables rather than just prose output.     

## Draft outline for `01_quickstart.md`

### 1. What this package does

Goal: explain, in plain language, that the repository contains both a classic literature-review pipeline and a more advanced synthesizer. The reader should understand that the quick start is just to verify installation and show the shape of the artifacts. 

### 2. Minimum prerequisites

Goal: tell the user what must already exist before running anything:

* Python environment
* package dependencies
* model/API configuration
* a small source corpus

### 3. Repository orientation

Goal: point the user to the two main zones:

* `lit_review_pipeline/` for the older end-to-end pipeline
* `synthesizer/` for the structured generation system 

### 4. Baseline run

Goal: walk the reader through a single successful run of the baseline path so they can inspect parsed data, chunks, summaries, and review output.

### 5. What to inspect after the run

Goal: teach the reader to inspect artifacts rather than just trust that the run succeeded:

* parsed files
* chunk files
* vectorstore artifacts
* review markdown output 

### 6. Why this is only the baseline

Goal: make clear that the baseline path produces a review, but the structured synthesizer is the real system for planned report generation.

## Draft outline for `02_structured_report_workflow.md`

### 1. The control model of the synthesizer

Goal: explain the three-layer control order:

* Report Plan
* Style Sheet
* Directory Tree

This should be explicit because the loader code says the report plan is the highest authority, the style sheet is second, and the directory tree is derived rather than canonical. 

### 2. Step 1 — Prepare the report plan

Goal: teach the user that the report plan defines the report structure and section contracts. Cover:

* `section_id`
* title
* parent/child hierarchy
* `section_type`
* description
* `source_queries`
* dependency edges
* `depth_level`

The plan model and loader make this one of the most important tutorial chapters, because the plan is schema-validated and checked for missing dependency references, content cycles, and depth consistency.  

### 3. Step 2 — Prepare the style sheet

Goal: teach the user how style policy is encoded. Cover:

* tone register
* citation pattern
* heading format by level
* word limits
* forbidden phrases
* equation delimiters
* per-type overrides

This deserves its own section because style loading validates the JSON and checks citation regex validity before generation even starts. 

### 4. Step 3 — Understand section generation inputs

Goal: explain what actually goes into each generation prompt. The tutorial should say that every section prompt is assembled from five channels:

* section description and type
* retrieved evidence chunks
* upstream claim tables
* upstream summary abstracts
* style constraints

Also explain what is intentionally excluded:

* no Stage 05 answer text
* no raw upstream content markdown
* no Stage 06 paper-summary data inside generation prompts 

### 5. Step 4 — Generate sections in dependency order

Goal: show that this is not a flat loop. Section generation waits for content dependencies, and finalization waits for both content and reference dependencies. That dependency-aware behavior should be taught as a central feature, not a side note. 

### 6. Step 5 — Validate outputs

Goal: explain the first quality gate the user will encounter. Focus especially on rule-based validation:

* word count
* heading level
* citation format
* forbidden phrases
* equation delimiters
* per-type overrides

That behavior is deterministic and comes directly from the validation layer, so the tutorial should teach the user how validation failures map back to the style sheet. 

### 7. Step 6 — Extract claim tables

Goal: explain that finalized sections are not the end state. The package then extracts structured claim tables from finalized section text and the retrieved chunks. The tutorial should show:

* what a claim entry contains
* how source chunk IDs are attached
* what confidence tags mean
* what “partial” means when extraction retries are exhausted 

### 8. Step 7 — Inspect lifecycle state and propagation

Goal: explain the operational behavior after a change:

* sections must meet dependency prerequisites
* content changes can invalidate downstream sections
* deep cascades can escalate rather than continue invalidating
* reference changes trigger re-validation rather than re-generation
* final assembly only happens when all sections are ready 

### 9. Step 8 — Inspect final metrics

Goal: explain how to judge run quality. The tutorial should explicitly walk through:

* structural compliance rate
* style compliance rate
* dependency completeness
* unsupported claim rate
* revision churn
* claim-table completeness
* evidence-claim agreement

This is important because the package writes `run_metrics.json` as a formal output, and the metrics define success much better than “the run finished.” 

## Draft outline for `03_report_plan_guide.md`

### 1. What a report plan is

Goal: explain that the report plan is the authoritative blueprint for the report. 

### 2. Required fields in each section node

Goal: document every field the user must supply in a section node. 

### 3. Section types and when to use them

Goal: explain how section type changes prompt behavior and output schema.

### 4. Dependency edges

Goal: explain content versus reference relationships and why they matter downstream. 

### 5. Common report-plan failures

Goal: document:

* invalid JSON
* unknown section IDs in dependencies
* content cycles
* bad depth levels
* malformed section identifiers  

## Draft outline for `04_style_sheet_guide.md`

### 1. What the style sheet controls

Goal: show that the style sheet is a real enforcement layer, not just advisory text.  

### 2. Citation pattern design

Goal: teach users how to define a citation regex that matches their target output style.

### 3. Word-count and heading rules

Goal: show how per-level constraints work and where per-type overrides take precedence. 

### 4. Forbidden phrases and equation delimiters

Goal: explain how these are enforced and why they belong in the style policy rather than ad hoc prompt wording. 

### 5. Common style-sheet failures

Goal: document:

* invalid JSON
* invalid citation regex
* unrealistic word limits
* heading mismatch
* equation delimiter mismatch  

## Draft outline for `05_validation_metrics_and_troubleshooting.md`

### 1. How retries should be interpreted

Goal: explain that failed validation can feed retry errors back into regeneration prompts, so users should inspect validation output before changing the plan or style sheet. 

### 2. How to read lifecycle transitions

Goal: teach users to interpret states such as queued, generating, finalized, stable, invalidated, and escalated. 

### 3. How to debug claim-table problems

Goal: explain missing claims, unsupported claims, partial claim tables, and confidence-tag mismatches.  

### 4. How to debug downstream dependency problems

Goal: teach users when a downstream section should be regenerated, when it should only be revalidated, and when a cascade has exceeded its depth limit. 

### 5. How to interpret the final run metrics

Goal: give a practical reading of each metric and its threshold targets. 

## Example artifacts the tutorial should ship with

The tutorial will be much stronger if it includes a working example bundle:

* `examples/tutorial_corpus/`
* `examples/example_report_plan.json`
* `examples/example_style_sheet.json`
* `examples/example_env.md`
* `examples/expected_outputs/`
* `examples/troubleshooting_cases/`

The most important artifacts are the plan and style examples, because those are the controlling inputs to the synthesizer workflow.  

## Best drafting order

Write the tutorial in this sequence:

1. `01_quickstart.md`
2. `02_structured_report_workflow.md`
3. `03_report_plan_guide.md`
4. `04_style_sheet_guide.md`
5. `05_validation_metrics_and_troubleshooting.md`

That order gets a usable tutorial in place quickly while keeping the more reference-heavy chapters aligned to the actual package behavior. The quick start proves the environment, and the structured workflow then introduces the report plan, style sheet, prompt assembly, lifecycle, claim extraction, and metrics in the order the software uses them.      

## Immediate next drafting target

The strongest next document to write is `02_structured_report_workflow.md`, because it becomes the backbone for the other four documents.

The opening sections of that document should be:

1. Overview of the synthesizer control model
2. Preparing the report plan
3. Preparing the style sheet
4. Running section generation
5. Validating and retrying
6. Extracting claim tables
7. Inspecting lifecycle and metrics