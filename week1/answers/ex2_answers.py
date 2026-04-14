"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability", "check_pub_availability", "calculate_catering_cost", "get_edinburgh_weather", "generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = "Had to change the model from Llama to Nemotron. Tool calls didn't work with former"   # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The model was backed up by a compatible placeholder
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
check_pub_availability: {"success": true, "pub_name": "The Bow Bar", "address": "80 West Bow, Edinburgh", "capacity": 80, "vegan": true, "status": "full", "meets_all_constraints": false}
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
After checking all four known Edinburgh venues, none can accommodate 300 people while also providing vegan options:

| Venue | Capacity | Vegan Options | Meets 300‑person + Vegan Requirement? |
|-------|----------|---------------|----------------------------------------|
| The Albanach | 180 | ✅ Yes | ❌ No (capacity too low) |
| The Haymarket Vaults | 160 | ✅ Yes | ❌ No (capacity too low) |
| The Guilford Arms | 200 | ❌ No | ❌ No (capacity too low & no vegan) |
| The Bow Bar | 80 | ✅ Yes | ❌ N...
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = """
I don't have access to real-time train schedules or National Rail information, so I can't provide the exact departure time for the last train from Edinburgh Waverley to London tonight.

For the most accurate and up-to-date train times, I'd recommend checking:
- **National Rail Enquiries** website or app
- **Trainline** or **LNER** (London North Eastern Railway) website/app
- **ScotRail** for connections to Edinburgh stations
- Station departure boards at Edinburgh Waverley

These sources will ...
"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
A real world assistant would naturally be expected to answer that question as well, since providing such details helps participants better understand the context, logistics, or purpose of an event.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The YAML assumes a task-oriented dialogue system (Rasa CALM) where the conversation structure is pre-defined — the LLM fills slots, but the skeleton is fixed.
The Mermaid graph assumes a ReAct-style agent where the LLM has full autonomy to decide what to do next and calls tools in a loop until it decides it's done. There's no prescribed slot order, no explicit out-of-scope branch — the agent reasons its way through.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
There were a lot of unexpected and surprising things in this excersise. First of all, the initial Llama model didn't invoke tools at all and had to replaced by something else e.g. Nemotron. The Nemotron response was slightly different from what was expected by exersise. These things had to be debugged.
Apart from that I didn't see much surprises.
"""