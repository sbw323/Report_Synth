├── lit_review_pipeline
│   ├── 01_ingest.py
│   ├── 02_parse.py
│   ├── 03_chunk.py
│   ├── 04_index.py
│   ├── 05_query.py
│   ├── 06_review.py
│   ├── agent_log.jsonl
│   ├── config.py
│   ├── data
│   │   ├── manifest.json
│   │   ├── parsed
│   │   │   ├── all_chunks.json
│   │   │   ├── Stare et al. - 2007 - Comparison of control strategies for nitrogen removal in an activated sludge process in terms of ope_chunks.json
│   │   │   └── Stare et al. - 2007 - Comparison of control strategies for nitrogen removal in an activated sludge process in terms of ope_merged.md
│   │   ├── pdfs
│   │   │   └── Stare et al. - 2007 - Comparison of control strategies for nitrogen removal in an activated sludge process in terms of ope.pdf
│   │   └── summaries
│   │       ├── literature_review.md
│   │       └── Stare et al. - 2007 - Comparison of control strategies for nitrogen removal in an activated sludge process in terms of ope_summary.json
│   ├── requirements.txt
│   ├── test_pipeline.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── equation_handler.cpython-312.pyc
│   │   │   ├── figure_handler.cpython-312.pyc
│   │   │   └── metadata.cpython-312.pyc
│   │   ├── equation_handler.py
│   │   ├── figure_handler.py
│   │   └── metadata.py
│   └── vectorstore
│       ├── 43d10370-66cc-4b82-b893-a41b3dcd8280
│       │   ├── data_level0.bin
│       │   ├── header.bin
│       │   ├── length.bin
│       │   └── link_lists.bin
│       ├── bm25_index.pkl
│       └── chroma.sqlite3
├── sprint_logs
│   ├── sprint_1_meta.json
│   ├── sprint_1_response.md
│   ├── sprint_2_meta.json
│   ├── sprint_2_response.md
│   ├── sprint_3_meta.json
│   ├── sprint_3_response.md
│   ├── sprint_4_meta.json
│   ├── sprint_4_response.md
│   ├── sprint_5_meta.json
│   ├── sprint_5_response.md
│   ├── sprint_6_meta.json
│   └── sprint_6_response.md
├── synthesizer
│   ├── __init__.py
│   ├── acceptance
│   │   └── __init__.py
│   ├── assembly
│   │   └── __init__.py
│   ├── config.py
│   ├── dag.py
│   ├── extraction
│   │   ├── __init__.py
│   │   ├── claim_extractor.py
│   │   ├── claim_validator.py
│   │   └── summary_abstractifier.py
│   ├── loaders
│   │   ├── __init__.py
│   │   ├── plan_loader.py
│   │   └── style_loader.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── claims.py
│   │   ├── enums.py
│   │   ├── provenance.py
│   │   ├── report_plan.py
│   │   ├── section_output.py
│   │   ├── state.py
│   │   ├── style_sheet.py
│   │   ├── validation_models.py
│   │   └── validation.py
│   ├── observability
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── metrics.py
│   │   └── tokens.py
│   ├── orchestrator
│   │   ├── __init__.py
│   │   ├── lifecycle.py
│   │   └── model_init.py
│   ├── prompt
│   │   ├── __init__.py
│   │   ├── assembly.py
│   │   └── context_channels.py
│   ├── retrieval
│   │   ├── __init__.py
│   │   ├── adapter.py
│   │   └── planning_context.py
│   └── validation
│       ├── __init__.py
│       ├── coordinator.py
│       ├── graph_validation.py
│       ├── layer1_structural.py
│       ├── layer2_rules.py
│       └── layer3_semantic.py
└── tests
    ├── __init__.py
    └── test_retrieval_adapter.py