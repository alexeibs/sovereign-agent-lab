"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = """
I searched the available Edinburgh venue database for venues that can accommodate **at least 300 guests** and offer **vegan menu options**. Unfortunately, **no venues currently meet both criteria**.

The database only shows smaller venues with vegan options (e.g., The Albanach – capacity 180, The Haymarket Vaults – capacity 160). If you’re flexible on either the guest count or the vegan requirem...
"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
For query 1 the model recommended the same venue but it did less tool calls.
For some reason it didn't call get_venue_details during the experiment.
Looking at the source code, it seems that we could also change capacity and vegan fields.
Address field shouldn't affect filtering
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 303   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 292   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
1. MCP allow us to dynamically discover tools rather than hardcode them
2. MCP enforces standards which makes tools reusable
3. Schema allows us to validate data
4. Standardised protocol and schemas allow us to run the tool "remotely" either via RPC or CLI
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.

# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)

# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.

# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model that turns an ambiguous task into ordered subgoals, and it lives in the autonomous-loop half of PyNanoClaw.
- The Executor is the ReAct-style worker that carries out tool calls and step-by-step reasoning, and it lives in the autonomous-loop half of PyNanoClaw
- The Handoff bridge routes work between the two halves, sending research tasks to the loop and confirmation tasks to the structured agent, and it lives in the shared layer.
- The MCP tool server is the common capability surface for web search, venue lookups, calendar access, and email, and it lives in the shared layer
- The CALM flow controller is the deterministic business-rule engine for confirmations and guardrails, and it lives in the structured-agent half
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The research (planner+executor) should live in the autonomous-loop half, and the call (CALM flow) should live in the structured-agent half.
Swapping feels wrong because the call has to follow some scenario similar to what we had in excercise 3. We get more freedom on the research side.
If you put the call in the loop, it would improvise where it should not, and if you put research in the structured agent, it would be boxed into flows that cannot find relevant information.
"""