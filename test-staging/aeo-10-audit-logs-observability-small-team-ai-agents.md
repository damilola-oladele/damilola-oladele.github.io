---
layout: page
title: TEST PLACEHOLDER - DO NOT PUBLISH
sitemap: false
---

# Audit logs and observability for small-team AI agents

Your agent updated a customer record, and a teammate asks who approved the change. You need a record that connects the request, the action and the result.

If you run agents that act for a small team, use this guide to decide two things: the minimum logging, storage and review setup to put in place now, and when a dedicated observability tool is worth considering.

Our recommendation is to start with a readable action history, a place to keep it and a named reviewer. Test whether a teammate can reconstruct one action. Consider a dedicated tool when your routine reviews repeatedly require records or connections your current setup cannot provide.

## What your minimum audit log must answer

Our proposed minimum is a record that answers six questions: Who requested the work? What was the agent asked to do? When did it act? Which tool did it use? What happened? Who reviewed the result?

This section describes our recommended design. For a team of two, the requester and reviewer might be the same person. Record both roles explicitly rather than leaving a future reader to infer them.

Consider a hypothetical agent asked to update a customer’s billing address. Connect the request to the particular update attempt, identify the affected record, show the reported outcome and name the person responsible for checking it. Keep “requested,” “attempted,” “reported successful” and “reviewed” as separate entries or states in your design.

Make uncertainty visible. If an action’s outcome is unknown, record “unknown” and assign a follow-up. If approval was required but you cannot find it, mark the approval as unresolved. Do not let an empty field stand in for a decision.

Use those questions as an acceptance test. Before adding another dashboard, ask a teammate to reconstruct one example action from the proposed record. Treat the minimum as complete only when they can explain the sequence and identify anything still unresolved.

## What to record and where to keep it

Our recommended starting design is one record per action, linked by a run ID. Here is a hypothetical record for the billing-address update:

| Field | Example |
|---|---|
| Run / action | run-104 / action-02 |
| Requester / agent | Maya / billing-agent |
| Task | Update the billing address for customer C-42 |
| Action time | 2026-11-10, 09:14 UTC |
| Tool / target | update_customer / C-42 |
| Approval reference | request-88, approved by Maya |
| Attempt / reported outcome | Update attempted / tool reported success |
| Review | Pending; assigned to Sam |
| Follow-up | Sam to check the resulting customer record |

OpenTelemetry’s GenAI walkthrough illustrates connected steps with a top-level `invoke_agent` span, child `chat` spans for model calls, and `execute_tool` spans for tool calls. Names may differ across frameworks. [R2] For your own record, keep the run-to-action connection even if you use different names.

Keep the task summary narrow. For the address update, our recommendation is to record the purpose and a reference to the affected customer record before considering a copy of the conversation. Decide separately whether you need any content from the request to investigate that action.

The walkthrough describes metadata capture, such as model names, token counts and durations, with full content capture switched on separately. The spec marks input messages, output messages and system instructions as opt-in and potentially sensitive. These are the described conventions and settings; other tools may have different defaults. [R3]

For your starting setup, we recommend metadata and deliberate references. Add content capture only for a defined investigation need, with an explicit decision about who can read it and when to remove it. Ask what you need to reconstruct the action before choosing what to retain.

The GenAI spec includes reference attributes, such as `gen_ai.input.messages_ref`, for content stored elsewhere. It also warns that a reference URI can expose storage metadata, including bucket names or tenant identifiers. [R4] Review the references you store, as well as the content they point to. “Stored elsewhere” should not end the discussion about access.

Choose the storage location by testing retrieval and review. Start with an existing team-controlled store where the responsible people can find records by run, time, tool and outcome. Set access and retention deliberately. Write down who owns the store and how a reviewer retrieves an older action.

## Who reviews the record

Our recommended starting default is to name the person responsible for the affected workflow as reviewer, with one named teammate as backup. For the billing-address example, choose whoever owns customer billing. Agree on this assignment before enabling the action workflow.

Start with a daily review on working days of all actions that changed external records, required approval or reported an uncertain outcome. For other completed actions, review five each week, or all of them if there were fewer than five. These are our proposed defaults. Adjust them explicitly as you learn what your actions require.

For an action your team considers consequential, set its review timing as part of the workflow before authorizing it. Do not treat a daily review as a substitute for any approval you require before the action happens.

During review, read the request, follow the linked tool steps and compare the recorded outcome with the intended task. For the example record, Sam should check the resulting customer record, then replace “pending” with a decision and review time.

Record what you checked and assign any follow-up to a person. If Sam is unavailable, record the transfer to the backup. Close the review with either a recorded disposition or an assigned follow-up; keep an uncertain result visible until someone resolves it.

## When a dedicated vendor is worth considering

Our recommendation is to evaluate a dedicated tool when one of these signs recurs during your reviews:

- A reviewer cannot find all the model and tool steps associated with an action.
- Reconstructing a run repeatedly requires manual searches across several stores.
- Your team cannot reliably retrieve the actions still awaiting review or follow-up.

Use a recent example as the evaluation task. Ask a candidate tool to show the complete run, locate its related actions and identify what remains unresolved. Record which part of your current setup failed that test. If the problem is a missing reviewer or an undefined approval rule, address that responsibility before choosing a product.

Langfuse’s own documentation describes application tracing as structured records containing prompts, model responses, token usage, latency, and tool or retrieval steps. [R8] Treat this as the vendor’s own description. Evaluate whether those views answer your review questions before adopting a tool.

Our recommendation uses recurring review problems rather than a team-size or request-volume cutoff. Treat the move as a judgment call: write down the question you cannot answer, the records needed to answer it and the person who will use the result. Move forward when a proposed setup meets that need and its access, retention and operating responsibilities are acceptable to your team.

Check the details of any implementation before committing to its field names. The OpenTelemetry GenAI conventions carry Development status, so attributes and structures may change. [R1] Document your essential questions separately from the telemetry names used to answer them.

Keep a dedicated vendor accountable to the same minimum: reconstruct the action, explain the outcome and show who reviewed it. Revisit your choice when your review needs change.

## Minimum viable audit log checklist

Our recommended minimum:

- Link every action to a run and a requester.
- Record when it happened, the tool and the affected resource.
- Distinguish the request, attempted action and reported outcome.
- Include an approval reference where your workflow requires one.
- Start with metadata; decide explicitly about content capture.
- Choose a store, access rules, retention period and owner.
- Name a reviewer, backup and review cadence.
- Record review decisions and assign unresolved follow-up.

## Claim-to-source list

- **[R1]** Development status and change caution: [OpenTelemetry GenAI agent-spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md). Living document; accessed 2026-11-10.
- **[R2]** Run, model-call and tool-call span tree: [OpenTelemetry GenAI observability walkthrough](https://opentelemetry.io/blog/2026/genai-observability/). Framework names may differ.
- **[R3]** Metadata capture and opt-in sensitive content: [OpenTelemetry walkthrough](https://opentelemetry.io/blog/2026/genai-observability/) and [agent-spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md). Defaults are scoped to the described conventions and settings.
- **[R4]** Content references and URI metadata caution: [OpenTelemetry agent-spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md).
- **[R8]** Vendor-described tracing contents: [Langfuse observability overview](https://langfuse.com/docs/observability/overview). Vendor self-description; accessed 2026-11-10.

Next step: record one agent action using the checklist today.
