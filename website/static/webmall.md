"Website for Comparing Agent Interface Paradigms on the WebMol Benchmark"
Task
Build a scientific website for our research project that compares agent interface paradigms for web-based agents, evaluated on the WebMall benchmark. The target audience is researchers (PhD level and up). The style, tone, and depth should closely follow the scientific sample page in the repository. All technical and configuration details can be referenced or linked directly from the codebase.

Structure & Content
1. Project Motivation & Overview
Goal: Introduce the motivation—comparing agent interface paradigms for web-based agents using a rigorous and realistic evaluation framework.

WebMol Benchmark: 

https://wbsg-uni-mannheim.github.io/WebMall/

Briefly describe: four tech-focused e-commerce stores, ~1,000+ products per store.

Tasks range from: (1) simple product lookup, (2) vague/goal-oriented queries, to (3) end-to-end purchasing.

Research Focus:

The website is for a comparative study of interface paradigms—how different architectures/approaches impact agent performance on realistic web tasks.

2. Agent Interface Paradigms Compared
Section for Each Approach:
Each paradigm should be a sub-section, with deep technical detail and clear explanation:

Retrieval-Augmented Generation (RAG):

Uses site-wide scraping (with unstructured), creates a unified ElasticSearch index using compound embeddings (product titles + full page text with OpenAI’s small embedding model).

Agent setup: e.g., GPT-4.1 and FropFix SONET-4, with function access.

Retrieval workflow: agent first gets lists of titles, then can drill down to product details.

Implementation details/configuration should link to the repo.

MCP-based Interface:

Agent accesses shops through APIs using the MCP protocol (Anthropic), with one ElasticSearch index per shop.

Similar retrieval/search workflow as above.

All API, MCP config, and technical details linked to the codebase.

NLWeb + MCP:

Combines NLWeb standard with MCP servers; again, one index per shop.

Focus on differences in agent interaction, protocol, and system design.

Deep technical detail as above, with repo links.

Naming:
Use these paradigm names as section headers:

“Retrieval-Augmented Generation (RAG)”

“MCP-based Interface”

“NLWeb + MCP”

For each:

List strengths, limitations, use cases.

Provide pointers to config, prompts, and architecture diagrams in the repo as needed.

3. Technical Details
Provide implementation specifics and deep-dives as appropriate for a PhD-level reader.

For all configuration (e.g., ElasticSearch setup, prompt formats), link directly to the codebase/repo.

Diagrams, code snippets, and explanations should match the sample page in style and depth.

4. Results
A section for experimental results (performance comparisons, task success rates, etc.).

Results should be rendered from uploaded CSVs in the same style and format as the sample page (static tables, no additional interactivity required). Only add the AX+MEM results for a browser based comparison 

5. Repository & Links
Prominent links to the repository/codebase for further details, configuration files, prompt templates, and technical documentation.

6. Team & Contact
Contributors, contact info, and any acknowledgments/funding as per the sample page.

Style & Design
Audience: Researchers, assume high technical literacy.

Tone: Formal, scientific, and precise—match the sample page’s language.

Navigation: Clear, logical sectioning.

Visuals: Use diagrams/tables/code where present in the sample or repo.

Depth: Ensure all claims are reproducible via repo links/config references.

Special Instructions
The agent should explore the repository for detailed configuration, prompts, and illustrations as needed.

All technical references should point to relevant code sections/files.

All info and visual style should follow the provided sample page.

Summary for Agent:

“Build a scientific website comparing three agent interface paradigms (RAG, MCP-based, and NLWeb + MCP) for web-based agents, as evaluated on the WebMol benchmark (four e-commerce stores, multi-step shopping tasks). Use the same scientific tone, structure, and depth as the sample page in the repo. All technical details and implementation/configuration specifics should be referenced from the repository. Render results tables from uploaded CSV files in the same format as the sample page.”