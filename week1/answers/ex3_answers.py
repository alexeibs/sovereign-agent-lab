"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  I'm calling to confirm a booking

How many guests are you confirming for tonight's event?
Your input ->  160

And how many of those guests will need vegan meals?
Your input ->  50

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200

Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly."""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  I'm calling to confirm a booking

How many guests are you confirming for tonight's event?
Your input ->  160

And how many of those guests will need vegan meals?
Your input ->  50

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  3000
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £3000 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £3000 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  I'm calling to confirm a booking

How many guests are you confirming for tonight's event?
Your input ->  160

And how many of those guests will need vegan meals?
Your input ->  I'm not sure. Could you tell me about parking options near the venue?
2026-04-13 23:03:44 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is in the middle of confirming a booking. The AI asked about the number of vegan guests, and the user says they\'re not sure. Then they ask about parking options.

First, the user mentioned they\'re not sure about the vegan count. In the current flow, the required slot is vegan_count. Since they\'re unsure, maybe we should set that slot to something like "undefined" or note that it\'s not provided. But according to the instructions, we should only set slots based on user input. Since they didn\'t provide a number, maybe we don\'t set it yet. Wait, the current state already shows vegan_count is undefined. So maybe the user\'s "not sure" just confirms that it\'s still undefined. Do I need to set it again? The example says to set every mentioned value. But here, the user is saying they don\'t know. Should I set the slot to a value indicating uncertainty? But the slot type is float. Hmm, maybe not. The instructions say not to use placeholders. So perhaps we just leave it as undefined and don\'t set a slot here.

Then the user asks about parking options. Looking at the available flows, confirm_booking handles booking details like guest count, dietary needs, deposit. Parking is mentioned in handle_out_of_scope as an example. So this query about parking is out of scope. Therefore, the correct action is to start the handle_out_of_scope flow. Also, since the user is asking for info about parking, which is a factual question, but it\'s outside the booking confirmation flow. So the action would be to start handle_out_of_scope and provide info? Wait, the available actions include provide info for FAQs, but parking is listed as out of scope. The handle_out_of_scope flow is for those topics. So maybe start handle_out_of_scope and provide info? Or just start the handle_out_of_scope flow. The description says handle_out_of_scope is for those requests. So perhaps start that flow.

So the actions would be: first, since the user didn\'t provide the vegan count, maybe set the slot vegan_count to "undefined" but in the current state, it\'s already undefined. The user\'s message is "I\'m not sure." So maybe set the slot to indicate that, but since the type is float, maybe we can\'t. The instructions say to extract every mentioned value. Since the user is not sure, they didn\'t mention a value, so no set slot needed here' message='No commands were parsed from the LLM actions.'
2026-04-13 23:03:44 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  50

2026-04-13 23:04:26 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user\'s last message is "50". I need to process this in the context of the conversation.

Looking at the current state, the active flow is confirm_booking. The current step is asking for vegan_count. The user previously answered 160 for guest_count, and now they\'re providing 50 for vegan_count.

So the first action should be to set the vegan_count slot to 50. Since the user provided a number, I just need to map that to the slot. The slot is of type float, so even though it\'s a whole number, it\'s okay to input 50.0, but the user said 50, so maybe just 50. But the example shows "160.0" as the value, so maybe I should convert it to a float. But the user input is 50, so perhaps the system expects it as a string? Wait, the slot\'s type is float, so I need to make sure the value is a float. However, the user\'s message is "50", which is a string. But in the example, the value is stored as "160.0". So maybe I should convert it to a float. But the instruction says to extract text exactly as the user provided. Hmm, conflicting.

Wait, the general instructions say: "Extract text exactly as the user provided it." So even if the slot is a float, the value should be the exact text the user gave. But in the current state, the guest_count is "160.0" as a string. Wait, looking at the current state example, the guest_count value is "160.0" (a string), but the type is float. So maybe the system expects the value to be a string representation of a float. So when the user says 50, I should set it as "50.0"? Or just "50"? The example shows "160.0" for guest_count, which was provided by the user as "160". So maybe the system automatically appends .0? Or maybe the user\'s input is converted to a float and stored as a string with .0. But according to the instructions, I should extract the text exactly as the user provided. So if the user says 50, the value should be "50". But in the current state, the guest_count is "16' message='No commands were parsed from the LLM actions.'
2026-04-13 23:04:26 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  50

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200

Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The bot seemed to be confused and didn't know what to do. It repeated a question but couldn't immediately recover even after correct answer.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph didn't show any errors and didn't repeat questions. It produced nicely formatted result which didn't give user what they wanted.
Rasa CALM seemed to be a bit buggy and could be confused very easily but the outcome was essentially the same for the user.
One key difference is that Rasa agent did "insist" on the scripted scenario and therefore would be more stable in production.
Both approaches weren't ideal from user perspective. As user I'd like to get answers for such "side" questions.
For example, Claude Code recently introduced /btw tool, and I find it very helpful.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I ran the same scenario as in part B but specified the time past 16:45. The conversation went similarly but in the end the bot couldn't confirm the booking.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
In old Rasa, Python we had to use regex to parse phrases like "about 160 people" → 160.0.
In CALM, the LLM decides which flow to trigger from a natural utterance, extracts slot values
from freeform speech without regex, and handles graceful variation in phrasing
— things that previously required dozens of NLU training examples per intent.

Python STILL owns the business rules in ActionValidateBooking — the deposit
floor, the vegan ratio cap. Business rules are deterministic: "deposit must be ≥ £200"
has one right answer. An LLM has no business making that call; it would
hallucinate edge-case leniency or invent policy it was never given.

What you lose: LLM gives up transparency for flexibility and setup cost. This new
approach might be unacceptable in scenario which require higher precision and accountability
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
Altghoug CALM is simpler than the old RASA, it is still requires
a lot of setup work and YAML files.
However this extra work allows to put guardrails and limitations on LLM so
it doesn't start giving up things for free, for example.
"""
