## Implementation Strategy: Optimal Generation Sequence

The generation sequence below is organized into three phases. Each phase produces artifacts that the next phase consumes, so the ordering minimizes backtracking and revision.

### Phase 1 — Foundation Artifacts (generate first, before any tutorial prose)

**Step 1a: `examples/example_report_plan.json`** — A minimal 4–5 section report plan with at least one content dependency, one reference dependency, and one thematic dependency. This gives every tutorial document a concrete artifact to point at. The plan should use the `SectionNode` schema exactly (section_id, title, parent_id, section_type, description, source_queries, depth_level) and include dependency edges that exercise all four `DependencyKind` values.

**Step 1b: `examples/example_style_sheet.json`** — A working style sheet that covers tone register, citation pattern (with a realistic regex), per-level constraints, forbidden phrases, equation delimiters, and at least one per-type override. This must be valid against the `StyleSheet` Pydantic model so the tutorial can honestly say "this file loads without errors."

**Step 1c: `examples/example_env.md`** — A short environment-setup reference: Python version, key dependencies (anthropic, chromadb, sentence-transformers, rank-bm25, pydantic), the `ANTHROPIC_API_KEY` and `REPORT_PLAN_PATH` / `STYLE_SHEET_PATH` config keys, and a note about the corpus.

**Why this phase comes first:** Every tutorial document from `01` through `05` references these artifacts. Writing prose that says "your report plan should look like this" is dramatically more effective when "this" is a real file the reader can open.

### Phase 2 — Core Tutorial Documents (generate in dependency order)

**Step 2a: `01_quickstart.md`** — The shortest-path document. It depends only on the example env and the `lit_review_pipeline/` code. Its job is to prove the environment works and show the shape of baseline artifacts (parsed files, chunks, vectorstore, review markdown). It ends with the bridge sentence: the baseline pipeline produces a review, but the structured synthesizer is where planned report generation happens. This document should be self-contained and runnable.

**Step 2b: `02_structured_report_workflow.md`** — The backbone tutorial. This is the longest and most important document. It walks through the full synthesizer workflow using the example plan and style sheet from Phase 1. The generation sequence *within* this document should follow the software's own execution order: control model → report plan preparation → style sheet preparation → prompt assembly channels (including the five included and three excluded inputs) → dependency-ordered generation → three-layer validation → claim extraction → lifecycle and propagation → final metrics. Each step should reference the example artifacts by filename and show what the user should expect to see in the output directory.

**Why `02` comes after `01`:** The quickstart establishes that the reader has a working environment. The structured workflow can then assume the reader has already run the baseline and knows where the pipeline outputs live.

### Phase 3 — Reference Guides (generate last, with cross-references back to `02`)

**Step 3a: `03_report_plan_guide.md`** — Deep-dive into every `SectionNode` field, section types and their prompt behavior differences, dependency edge semantics (content blocks generation, reference blocks finalization, thematic is soft, source is informational), and common plan-validation failures (dangling references, content cycles, depth mismatches). This guide should show the example plan from Phase 1 and annotate each field. It can forward-reference `05` for troubleshooting specific failure modes.

**Step 3b: `04_style_sheet_guide.md`** — Deep-dive into the `StyleSheet` model: tone register, citation pattern regex design, per-level constraints (heading_format, min_words, max_words), forbidden phrases, equation delimiters, and per-type overrides. This guide should explain how each field maps to a specific Layer 2 validation check, because that's the enforcement mechanism. Common failures (invalid regex, unrealistic word limits, heading mismatch) should be documented with the exact error messages the validator produces.

**Step 3c: `05_validation_metrics_and_troubleshooting.md`** — The diagnostic reference. Organized around the questions a user asks when something goes wrong: how to read retry output, how to interpret lifecycle states (queued → generating → drafted → validated → finalized → stable, plus invalidated and escalated), how to debug claim-table issues (partial extraction, missing source_chunk_ids, confidence tag mismatches), how to understand cascade propagation and depth limits, and how to read the seven `run_metrics.json` values (structural compliance, style compliance, dependency completeness, unsupported claim rate, revision churn, claim-table completeness, evidence-claim agreement).

**Why Phase 3 comes last:** These three documents are reference material. They're most accurate when written after the walkthrough (`02`) has already been drafted, because `02` reveals the natural teaching order and the places where readers will need to "go deeper." Writing `03`–`05` first would risk front-loading detail that doesn't land until the reader has seen the workflow in action.

### Summary Table

| Step | Artifact | Depends On | Primary Purpose |
|------|--------|-----------|-----------------|
| 1a | `examples/example_report_plan.json` | Codebase schemas | Concrete reference for all tutorials |
| 1b | `examples/example_style_sheet.json` | Codebase schemas | Concrete reference for all tutorials |
| 1c | `examples/example_env.md` | Config surface (§16) | Setup reference |
| 2a | `01_quickstart.md` | Phase 1 artifacts | Prove environment, show baseline |
| 2b | `02_structured_report_workflow.md` | Phase 1 + `01` | Backbone walkthrough |
| 3a | `03_report_plan_guide.md` | Phase 1 + `02` | Deep-dive reference |
| 3b | `04_style_sheet_guide.md` | Phase 1 + `02` | Deep-dive reference |
| 3c | `05_validation_metrics_and_troubleshooting.md` | `02` + `03` + `04` | Diagnostic reference |