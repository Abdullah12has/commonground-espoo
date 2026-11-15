# CommonGround

## Punchline
Company and people digital twins explore work scenarios before recruitment events, turning supplied evidence and open questions into introductions both sides choose.

## Description
CommonGround helps City of Espoo recruitment-event participants decide which conversations are worth having. A polished CV and a generic vacancy rarely reveal the actual work, the evidence behind someone's skills, or the expectations that need discussion.

A company twin represents a concrete work situation and requirements. A participant twin represents self-declared skills, preferences and supplied work examples. Owners review each representation. The participant chooses a company and explores an explicit scenario assumption. The system makes shared evidence and missing information visible, then proposes questions for a real meeting.

The working synthetic demo includes two company scenarios and three fictional participants. Northstar Commerce uses four deterministic SQLite checks to inspect an assumed revenue-repair strategy. Harbor Services explores an uncertain service incident through meeting questions. Optional Gemini 2.5 Flash dialogue lets the twins discuss the supplied context. Generated dialogue is labelled hypothetical; model failures are visible.

The result is an inspectable fit hypothesis. Evidence coverage counts skill areas with a reference, not a probability that someone will succeed. A successful toy query does not prove that a real person will perform the same way. There is no candidate leaderboard, automated rejection or hiring decision.

Before an event, participants edit and approve twins and explore connections. At the event, a shared agenda supports the conversation. Afterward, both sides can record usefulness and decide what to clarify next. The prototype implements simulated mutual opt-in, withdrawal and feedback. Editing a twin creates a new version and invalidates introductions based on old information. Saved receipts preserve the exact evidence used.

FastAPI and SQLite serve a responsive browser interface. The local scenarios work without an API key. The current demo simulates separate identities in one local session and uses fictional data only. Authentication, tenant isolation, deletion workflows, accessibility auditing and deployment controls are future work before real participant data. Live inference uses an external configured gateway; residency and retention are not established.

Our proposed Espoo pilot compares prepared introductions with the normal event process. Measure time to prepare, usefulness reported by both parties, mutual opt-in and follow-up rates. Examine whether missing evidence or non-traditional career paths lead to uneven outcomes. No measured impact or predictive accuracy is claimed.

CommonGround adapts our earlier Microsoft Prometheus digital-twin simulation concept and fixed scenario checks. The new event experience, versioned twin flow and mutual introductions focus that foundation on Espoo's challenge. The project owner confirms organiser approval for prior-code reuse. The source history and prior-work disclosure remain available.

## Submission assets

- Pitch: `CommonGround_Espoo_Pitch.pdf` and editable `.pptx`.
- Video: `CommonGround_Demo.mp4` (narrated walkthrough with actual app screenshots).
- Source: `CommonGround_Source.zip`.
- Demo: local `http://127.0.0.1:8766`.

Public demo, source and video URLs must point to real published assets. They are not filled with local paths or invented URLs. The local service is not production-ready for public shared use.
