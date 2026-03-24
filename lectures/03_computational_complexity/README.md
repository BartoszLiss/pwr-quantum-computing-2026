# Lecture 03: Computational Complexity

This folder contains the notebook materials for Lecture 03 on computational complexity in the PWr quantum computing labs. The central theme of this lecture is that complexity is not only about "how long an algorithm runs." It is also about what we call the input, how that input is represented, how much memory the representation consumes, what kind of problem we are trying to solve, and what additional cost appears when we move from a clean abstract idea to an executable computational workflow.

This lecture is also the conceptual bridge into later quantum topics. Before students can interpret claims about quantum speedup, they need a stable intuition for scaling, combinatorial explosion, representation cost, problem classes, and the difference between solving a problem and verifying a proposed solution. The notebooks in this folder are designed to build that intuition visually and progressively.

## How To Use This Folder

These notebooks are designed for two complementary uses:

- live lecture presentation, where each section opens with a motivating question and then answers it with one dominant visual
- student self-study, where the same sections can be rerun cell by cell with short explanatory markdown nearby

The notebooks are intentionally lightweight. They rely only on standard scientific Python tools available in course notebooks: Python stdlib, `numpy`, `scipy`, `pandas`, and `matplotlib`. They do not require network access or `qiskit`, and they should rerun top-to-bottom on a normal student laptop.

## Recommended Notebook Order

1. `01_growth_of_complexity_search_and_sort.ipynb`
   Starts with the most concrete intuition: some growth laws scale gracefully, others collapse. Uses search and sorting to contrast theoretical counting with measured timing and to show why preprocessing can completely change the story.

2. `02_graph_traversal_and_representation_costs.ipynb`
   Shows that a graph is not only a mathematical object but also a stored data structure. Compares adjacency lists and adjacency matrices, sparse and dense graphs, and explains why time complexity and memory complexity depend on representation.

3. `03_problem_classes_and_scaling_intuition.ipynb`
   Moves from algorithmic growth to problem-class intuition. Introduces brute-force combinatorial explosion, the difference between search and verification, and a careful first map of `P`, `NP`, `NP-hard`, `NP-complete`, `BPP`, and `BQP`.

4. `04_quantum_cost_pipeline_and_topology_mapping.ipynb`
   Bridges from abstract complexity language into realistic quantum execution cost. Treats state preparation like input-loading, topology like an architectural constraint, routing like forced movement, and repeated shots like a real output cost.

5. `05_quantum_advantage_feasibility_checklist.ipynb`
   Concludes the sequence with a disciplined evaluation framework. Synthesizes structure, class, input/output assumptions, hardware overhead, and classical baselines into a reusable checklist for judging whether a claimed quantum speedup is plausible, unclear, or hype-prone.

Taken together, the sequence moves from:

- runtime growth on familiar algorithms
- to representation-dependent cost
- to classifying whole families of problems
- to quantum execution as a full-stack cost pipeline
- to a final feasibility framework for judging advantage claims

That progression matters pedagogically. Students first see complexity as "how running time changes with input size," then as "how representation changes cost," and finally as "how entire categories of problems differ in what efficient computation can realistically do."

## Learning Arc By Notebook

### `01_growth_of_complexity_search_and_sort.ipynb`

This notebook is the entry point. It starts with growth laws that students can see immediately and then grounds those curves in familiar algorithmic tasks such as search and sorting. The goal is to move students away from isolated timing numbers and toward scaling language.

The main pedagogical moves are:

- show that `n`, `n log n`, `n^2`, and `2^n` quickly separate visually
- connect asymptotic growth to concrete operation counts
- compare theory with measured timing without pretending they are the same thing
- show that preprocessing can change the whole system-level comparison

By the end of notebook 1, students should be comfortable with the idea that complexity is about how cost changes with input size, not only how long one run took on one machine.

### `02_graph_traversal_and_representation_costs.ipynb`

This notebook expands the complexity story by showing that the same abstract graph can behave differently depending on how it is stored. That shift is important because many students initially treat data structures as implementation detail rather than part of the complexity story.

The main pedagogical moves are:

- compare adjacency lists and adjacency matrices on the same graph
- show sparse and dense structure visually
- connect BFS and DFS intuition to representation-dependent traversal cost
- treat memory cost and traversal cost as parallel concerns

By the end of notebook 2, students should understand that complexity depends not only on the algorithm and the mathematical object, but also on representation and sparsity.

### `03_problem_classes_and_scaling_intuition.ipynb`

This notebook moves from individual algorithms to families of problems. It uses brute-force subset enumeration and solve-versus-verify comparisons to prepare students for the language of problem classes without forcing theorem-heavy formalism too early.

The main pedagogical moves are:

- make combinatorial explosion visible through subset enumeration
- show why verification may be much cheaper than search
- introduce `P`, `NP`, `NP-hard`, and `NP-complete` as organizational tools
- build a cautious bridge to `BPP` and `BQP` without overclaiming

By the end of notebook 3, students should have a usable conceptual map: some problems are efficiently solvable, some are efficiently checkable, some look explosively hard, and quantum computing changes some boundaries but does not magically erase hardness.

### `04_quantum_cost_pipeline_and_topology_mapping.ipynb`

This notebook makes the first serious systems bridge into quantum computing. It keeps the models intentionally lightweight, but it insists that students treat a quantum algorithm as one stage inside a larger workflow rather than as an isolated circuit diagram.

The main pedagogical moves are:

- draw a clean execution pipeline from classical input to classical output
- connect state preparation to input-loading and preprocessing cost
- separate logical interactions from physical device constraints
- visualize routing overhead under different topologies

By the end of notebook 4, students should understand that an attractive logical core can still lose force once encoding, mapping, routing, and repeated measurements are included in the cost model.

### `05_quantum_advantage_feasibility_checklist.ipynb`

This notebook closes the lecture arc by training judgment rather than introducing a new computational mechanism. It asks students to evaluate claims of quantum advantage with the same discipline they used earlier for scaling, representation, and end-to-end workflow cost.

The main pedagogical moves are:

- turn earlier lecture ideas into a staged checklist
- compare strong and weak reasoning about problem structure
- connect class labels to realistic limits rather than slogans
- use toy case studies to separate plausible, unclear, and hype-prone claims

By the end of notebook 5, students should be able to challenge a speedup claim systematically instead of reacting only to asymptotic notation or presentation style.

## Lecture-Wide Pedagogical Focus

The notebooks in this lecture are built around a few recurring messages:

### 1. Growth Is A Story About Scaling, Not Single Numbers

A runtime like "0.01 seconds" is not very informative by itself. Complexity becomes meaningful when we ask how the cost changes as the input grows. That is why the notebooks keep returning to growth laws such as `log n`, `n`, `n log n`, `n^2`, and `2^n`.

The key question is not "is this algorithm fast right now?" but rather:

- what does the input size mean?
- what happens when that size doubles?
- does the work grow gently, steadily, or explosively?

### 2. Representation Changes The Cost Of Working With Data

Two mathematically identical objects can lead to very different computational behavior when stored differently. In Lecture 03, this is made explicit with graphs:

- adjacency lists are usually natural for sparse structure
- adjacency matrices can be convenient for dense structure or constant-time edge checks

This is one of the lecture's most important messages: complexity is partly about the problem, but also partly about how the problem instance is encoded.

### 3. Brute Force Fails Because Search Spaces Explode

In later sections, the notebooks move from familiar algorithms to combinatorial search. Subset enumeration is used as a clean teaching model because it exposes where exponential growth comes from.

Suppose the input is a list called `values` with length `n`. For each element, we make a yes/no decision:

- include this item in the subset
- or do not include it

That means each position contributes two possibilities. Across `n` positions, that creates `2^n` candidate subsets.

This is the core idea behind combinatorial explosion:

- one additional item does not add a small fixed amount of work
- it doubles the number of candidate subsets that brute force may need to inspect

In the notebook code, a candidate subset is represented by a variable such as `mask`, because a binary pattern is a natural way to encode "include" versus "exclude." The binary representation is not the real concept students must remember; it is only a convenient computational encoding of a deeper idea:

- combinatorial problems often consist of many yes/no choices
- the number of complete choice patterns can grow exponentially

That is why subset enumeration is important for this lecture. It gives a concrete, executable example of why some search problems become unrealistic even when each individual check is simple.

### 4. Solving And Verifying Are Not The Same Task

One of the most important conceptual transitions in the lecture is the shift from:

- finding a good candidate
- to checking a proposed candidate

These can be very different computational tasks.

For example, if someone gives us a proposed subset and asks whether its sum matches a target, we can usually check that candidate directly. But if nobody gives us the subset, and we must discover it ourselves by brute force, we may need to inspect a very large search space.

This distinction is the intuition behind why the lecture introduces problem classes. Students do not need full theorem-level formalism at this stage, but they do need a stable conceptual distinction between:

- efficiently solvable problems
- problems whose solutions can be efficiently checked
- problems that appear to resist efficient solution

### 5. Quantum Speedup Still Lives Inside Complexity Theory

This lecture is a setup for later quantum content, not a replacement for it. The goal is to prevent two common misunderstandings before they take root:

- "quantum computing makes all hard problems easy"
- "`BQP` means any difficult problem belongs to quantum advantage"

The notebooks instead prepare a more careful view:

- some models of computation gain power on some kinds of problems
- bounded-error computation is a meaningful idea in both randomized and quantum settings
- none of this erases the need to think carefully about scaling, representation, verification, or hardness

## Compact Glossary

- `P`
  Problems for which we know algorithms that solve the task efficiently, usually with polynomial scaling.

- `NP`
  Problems for which a proposed solution can be checked efficiently. The key intuition is "easy to verify," not "necessarily easy to solve."

- `NP-hard`
  Problems at least as hard as the hardest problems in `NP`. This is a hardness statement, not a promise that the problem itself belongs to `NP`.

- `NP-complete`
  Problems that are both in `NP` and `NP-hard`. These are the canonical "easy to state, hard to solve, easy to check" examples in classical complexity.

- `BPP`
  Problems solvable efficiently by randomized algorithms with bounded probability of error.

- `BQP`
  Problems solvable efficiently by quantum algorithms with bounded probability of error.

## Notebook Structure Standard

Each notebook in this folder follows the same lecture-first structure:

1. title, learning goals, and Lecture 03 note
2. a motivating section question
3. a minimal algorithm or model cell
4. a dedicated visualization cell
5. a theoretical comparison or compact table
6. a measured or estimated experiment
7. a takeaway box
8. an audience-facing question block

This rhythm is deliberate. It keeps the notebooks from becoming long mixed cells where algorithm definition, plotting code, and interpretation are tangled together.

## Visual Narrative Style

The lecture materials use a restrained, projection-friendly visual system shared through `utilities/complexity_utils.py`.

The style rules are:

- wide main figures, typically around `11 x 6` inches
- readable font sizes for projector use, not paper-scale density
- slightly heavier line widths and marker sizes than matplotlib defaults
- restrained academic palette: navy, teal, rust, gold, and gray accents
- plain-language titles and explicit axis labels
- one visual centerpiece per major section
- short interpretation immediately after the visual
- takeaway boxes and audience questions used as recurring visual rhythm

This is not only a cosmetic choice. The lecture emphasizes visual narrative, so every notebook should be understandable from a projected slide without requiring students to parse long walls of markdown.

## Shared Helper Module

The lecture notebooks use:

- `utilities/complexity_utils.py`

This helper module keeps the notebook cells focused on concepts rather than plotting mechanics. It provides:

- consistent matplotlib style setup
- reusable comparison plots and diagrams
- lightweight timing helpers
- formatting helpers for takeaway boxes and prompt blocks

The intention is not to hide logic from students. The intention is to keep visual plumbing out of the main teaching flow so the cells in the notebooks stay readable.

## Scope And Deliberate Simplifications

The lecture is intentionally intuition-first. That means some details are simplified on purpose:

- definitions are course-appropriate and visual, not proof-oriented
- measured timings are illustrative, not benchmarking-grade
- memory-cost estimates are educational proxies, not byte-accurate systems measurements
- class maps are conceptual guides, not complete formal relationship diagrams

These simplifications are not shortcuts around rigor. They are teaching decisions that make the core complexity ideas visible before later lectures demand more formal machinery.

## Current Status

Files currently present in this folder:

- `01_growth_of_complexity_search_and_sort.ipynb`
- `02_graph_traversal_and_representation_costs.ipynb`
- `03_problem_classes_and_scaling_intuition.ipynb`
- `04_quantum_cost_pipeline_and_topology_mapping.ipynb`
- `05_quantum_advantage_feasibility_checklist.ipynb`
- `README.md`

What has been implemented so far:

- lecture scaffold and style system
- notebook 1 on growth, search, sorting, and preprocessing
- notebook 2 on graph representation and traversal cost
- notebook 3 on brute force, verification, problem classes, and a cautious bridge to randomness and quantum
- notebook 4 on quantum execution workflow, topology, routing, and measurement cost
- notebook 5 on feasibility checklists for judging quantum advantage claims

What still remains:

- any later extensions or refinements requested for this lecture folder

Pedagogical simplifications currently in use:

- small, stable teaching examples rather than fully general datasets
- matrix-first visuals where graph drawings would become cluttered
- bounded-error intuition without formal quantum circuit machinery
