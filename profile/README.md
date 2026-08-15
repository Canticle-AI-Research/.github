<p align="center">
  <a href="https://canticle.cc">
    <picture>
      <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canticle-hero-ghost.png" />
      <source type="image/gif" srcset="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canticle-hero-ghost.gif" />
      <img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canticle-hero-ghost.png" width="100%" alt="Open Canticle — Ghost in the SEAM, an experimental cybernetic agent shell backed by source-linked memory" />
    </picture>
  </a>
</p>

## Open Canticle

<p><a href="https://canticle.cc"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/website.png" width="100%" alt="Open the Canticle website" /></a></p>
<p><a href="https://canticle.cc/research"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/research.png" width="100%" alt="Open Canticle Research" /></a></p>
<p><a href="https://canticle.cc/documentation"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/documentation.png" width="100%" alt="Open the SEAM documentation" /></a></p>
<p><a href="https://canticle.cc/lab-notes"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/lab-notes.png" width="100%" alt="Open Canticle Lab Notes" /></a></p>
<p><a href="https://canticle.cc/projects"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/projects.png" width="100%" alt="Open the Canticle projects index" /></a></p>
<p><a href="https://canticle.cc/benchmarks"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/benchmarks.png" width="100%" alt="Open Canticle benchmarks and evidence" /></a></p>
<p><a href="https://canticle.cc/documentation"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/python-sdk.png" width="100%" alt="Open the SEAM Python SDK documentation" /></a></p>
<p><a href="https://canticle.cc/contact"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/links/contact.png" width="100%" alt="Contact Canticle Research" /></a></p>

## Memory is infrastructure

Canticle Research is an independent AI lab building machine-first layers for the next generation of agents. Our work asks a practical question: how can an agent preserve evidence, retrieve the right context, and improve without losing the record of what it knows?

Our primary system is **SEAM — Semantic Encoding for Agent Memory**: a local-first memory runtime for AI agents. SEAM compiles untrusted source material into readable semantic records, keeps durable truth in SQLite, derives rebuildable retrieval indexes, and emits token-bounded context through a shared runtime.

## The canonical memory path

<p align="center">
  <a href="https://canticle.cc/documentation"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/canonical-memory.png" width="100%" alt="Open the SEAM documentation — canonical memory architecture from source evidence to token-bounded PACK context" /></a>
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
| **Ghost desktop companion** | An expressive conversational avatar is in development; voice and permissioned file/folder actions remain planned rather than available surfaces. |

## One runtime, four surfaces

<p align="center">
  <a href="https://canticle.cc/documentation"><img src="https://raw.githubusercontent.com/Canticle-AI-Research/.github/main/profile/assets/runtime-interfaces.png" width="100%" alt="Open the SEAM documentation — TUI, WebUI, MCP, and SDK interfaces connected to one shared runtime" /></a>
</p>

| Interface | Purpose |
|---|---|
| **TUI** | The terminal operator surface for navigating and controlling the runtime. |
| **WebUI** | The browser-based operator surface for observation and control. |
| **MCP** | A bounded stdio bridge for compatible agent clients. |
| **SDK** | The public Python integration surface for building agents with SEAM memory. |

Every current interface calls the same memory behavior rather than creating a second source of truth. **Ghost's desktop avatar, voice surface, and operating-system action bridge are in development** and are not presented here as available interfaces.

## Trust invariants

1. RAW preserves the source detail required for exact recovery.
2. MIRL preserves meaning, structure, uncertainty, contradiction, time, and provenance.
3. SQLite remains canonical; search, vector, and graph indexes remain rebuildable acceleration layers.
4. Retrieved content never automatically receives tool or operator authority.
5. PACK is derived, token-bounded, and linked back to its source records.
6. Lossless claims require exact reconstruction and integrity verification.
7. Benchmark claims stay attached to their workload, method, and auditable evidence.
8. System improvement remains gated by explicit operator review.

---

<p align="center">
  <strong>Canticle Research</strong><br />
  Machine-first layers for the next generation of agents.<br /><br />
  canticle.cc · Founded by BlackhatShiftey
</p>
