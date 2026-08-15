<p align="center">
  <img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canticle-hero-rgb.png" width="100%" alt="Canticle Research — provenance-first memory systems for AI agents" />
</p>

<p align="center">
  <a href="https://canticle.cc"><strong>Website</strong></a>
  &nbsp;·&nbsp;
  <a href="https://canticle.cc/research"><strong>Research</strong></a>
  &nbsp;·&nbsp;
  <a href="https://canticle.cc/documentation"><strong>Documentation</strong></a>
  &nbsp;·&nbsp;
  <a href="https://canticle.cc/benchmarks"><strong>Evidence</strong></a>
</p>

## Memory is infrastructure

Canticle Research is an independent AI lab building machine-first layers for the next generation of agents. Our work asks a practical question: how can an agent preserve evidence, retrieve the right context, and improve without losing the record of what it knows?

Our primary system is **SEAM — Semantic Encoding for Agent Memory**: a local-first memory runtime for AI agents. SEAM compiles untrusted source material into readable semantic records, keeps durable truth in SQLite, derives rebuildable retrieval indexes, and emits token-bounded context through a shared runtime.

<p>
  <a href="https://canticle.cc/documentation"><strong>Read the SEAM runtime contract →</strong></a>
</p>

## The canonical memory path

<p align="center">
  <img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canonical-memory.png" width="100%" alt="SEAM canonical memory architecture from source evidence to token-bounded PACK context" />
</p>

| Layer | Role |
|---|---|
| **RAW** | Preserves source detail needed for recovery, identity, exact spans, and provenance. |
| **MIRL** | Represents meaning, structure, uncertainty, contradiction, time, and provenance as readable semantic records. |
| **SQLite** | Remains the canonical source of truth for durable records. |
| **Retrieval indexes** | Accelerate lexical, vector, graph, temporal, hybrid, and mixed retrieval; they remain rebuildable. |
| **PACK** | Projects selected records into token-bounded context while retaining source back-pointers. |

The rule underneath the whole path is simple: **retrieved content is data, never authority**. Derived indexes and views can be rebuilt; canonical records and their evidence chain remain inspectable.

## Research vectors

| Area | What we are investigating |
|---|---|
| **Durable agent memory** | Canonical records that survive sessions without collapsing evidence into an opaque summary. |
| **Retrieval orchestration** | Combining lexical, vector, graph, temporal, hybrid, and mixed signals under explicit context budgets. |
| **Graph + temporal reasoning** | Entity relationships, event order, uncertainty, contradiction state, and supersession-aware retrieval. |
| **Provenance + trust** | Exact source bindings, prompt-injection containment, scope isolation, and operator-controlled authority. |
| **Surface Compile** | Readable MIRL and SEAM-RC/1 artifacts wrapped in SEAM-HS/1 lossless PNG surfaces for direct machine access. |
| **Evaluation systems** | Auditable benchmark runs with workload, method, selected records, retrieval traces, and evidence kept together. |
| **Agent improvement** | Versioned proposals, evaluation, and explicit operator review before an improvement can be promoted. |
| **Canticle agent** | Canticle's dedicated agent is in active development; the agent and its CLI are not yet presented as available surfaces. |

## One runtime, four surfaces

<p align="center">
  <img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/runtime-interfaces.png" width="100%" alt="TUI, WebUI, MCP, and SDK interfaces connected to one shared SEAM runtime" />
</p>

| Interface | Purpose |
|---|---|
| **TUI** | The terminal operator surface for navigating and controlling the runtime. |
| **WebUI** | The browser-based operator surface for observation and control. |
| **MCP** | A bounded stdio bridge for compatible agent clients. |
| [**SDK**](https://pypi.org/project/seam-client/) | The public Python integration surface for building agents with SEAM memory. |

Every current interface calls the same memory behavior rather than creating a second source of truth. The **CLI and Canticle agent are in active development** and are not presented here as available interfaces.

## Trust invariants

1. RAW preserves the source detail required for exact recovery.
2. MIRL preserves meaning, structure, uncertainty, contradiction, time, and provenance.
3. SQLite remains canonical; search, vector, and graph indexes remain rebuildable acceleration layers.
4. Retrieved content never automatically receives tool or operator authority.
5. PACK is derived, token-bounded, and linked back to its source records.
6. Lossless claims require exact reconstruction and integrity verification.
7. Benchmark claims stay attached to their workload, method, and auditable evidence.
8. System improvement remains gated by explicit operator review.

## Explore Canticle Research

| Destination | What you will find |
|---|---|
| [**Research hub**](https://canticle.cc/research) | Current research paths, systems, analysis, and evidence. |
| [**SEAM documentation**](https://canticle.cc/documentation) | Runtime concepts, installation, TUI/WebUI, retrieval, MIRL, MCP, and SDK integration. |
| [**Lab Notes**](https://canticle.cc/lab-notes) | Public research updates and technical field notes. |
| [**Projects**](https://canticle.cc/projects) | The public systems and build index. |
| [**Benchmarks**](https://canticle.cc/benchmarks) | Measured results presented with their evaluation context. |
| [**Python SDK**](https://pypi.org/project/seam-client/) | The public `seam-client` package for custom agent integrations. |
| [**Contact**](https://canticle.cc/contact) | Research, engineering, and collaboration inquiries. |

---

<p align="center">
  <strong>Canticle Research</strong><br />
  Machine-first layers for the next generation of agents.<br /><br />
  <a href="https://canticle.cc">canticle.cc</a>
  &nbsp;·&nbsp;
  Founded by <a href="https://github.com/BlackhatShiftey">BlackhatShiftey</a>
</p>
