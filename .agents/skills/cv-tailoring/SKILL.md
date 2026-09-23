---
name: "cv-tailoring"
description: "Tailors the candidate's CV to a specific job posting. Use it when they paste or attach a job description or a LinkedIn posting, or ask \"am I a fit for this role?\", \"tailor my CV to this\", \"prepare my application\". Produces a fit report, an ATS-safe DOCX CV and a recruiter message, all from the evidence bank. English version: if the bank is CARRERA-EVIDENCIAS.md, use cv-a-medida."
---

# CV tailoring

A three-phase system that turns a job posting into a complete application:
fit report, tailored DOCX CV and recruiter message.

The principle behind everything: **knowledge lives in the evidence bank, not here**.
This document is only the method. The bank is in charge.

---

## Before starting: find the evidence bank

Read `CAREER-EVIDENCE.md`, at the project root. All of it, before anything else.

**System language.** This is the English version. If the bank is `CARRERA-EVIDENCIAS.md`
or its header says `lang: es`, leave this skill and use `cv-a-medida`, its Spanish twin.
If both banks exist, ask which one to use.

If there is no bank at all, **stop and ask for it**. Without a bank there is no system: you would write an invented CV.

Its sections 7 (rules of truth) and 6 (gaps) take priority over any instruction in this
document and over any request to improve the fit.

`tools/build-cv.js` is the tested generator (helpers + layout, nobody's data).
The content of each CV lives in `cv-content.js`, inside its application folder
(private, not versioned). Build the application by writing **only** that file, in the format
`module.exports = (h) => [ ... ]` (use `tools/cv-content.example.js` as the template).
Never touch the helpers or the layout of `build-cv.js`. If `require('docx')` fails, run
`npm install` inside `tools/`.

---

## Phase 1: Break down the posting

Do not summarize the posting. Break it down into atomic requirements and classify them.

For each requirement, extract:

- **Literal statement** (a short quote from the posting, not paraphrased)
- **Type**: technical / leadership / domain / cultural / formal
- **Weight**: critical (it appears in the title, under "responsible for" or in "success in year one") / important / secondary
- **Vocabulary signal**: the exact word the company uses

Also identify:

- **The archetype** of the posting according to section 5 of the bank (A, B, C, D or E). If it fits none, say so and suggest the closest one.
- **The knockout requirement**, if there is one. It is usually hidden in a qualifications line, not in the headline.
- **What the company is really buying**: in one sentence. It is almost never what the job title says.
- **Dates and location**: if the application window has closed or the role is on-site away from the candidate's location (section 1 of the bank), say so before anything else. It saves the rest of the work.
- **Search criteria** (section 9 of the bank): salary band and type of role. If the posting publishes a range, check it. If it does not, mark it as an unknown to resolve at the first contact. If the role clashes with a criterion (consulting, for example), say so here, before the full analysis.

### Posting vocabulary

Build a list of the exact terms in the posting and mark each one:

- **Usable**: there is real evidence behind it. It goes into the CV verbatim, in the experience or in CORE SKILLS.
- **Usable with rephrasing**: the evidence is adjacent. Describe the fact without claiming the term.
- **Forbidden**: there is nothing behind it. It appears nowhere in the document.

A parser and a recruiter search for their words, not synonyms. But a word without evidence
is a lie that has to be defended in the first interview. This list decides.

---

## Phase 2: Fit report

A table per area, with this exact structure:

| Area | What they ask for | Evidence (IDs) | Fit | Comment |
|---|---|---|---|---|

Report rules:

- **Fit is justified only with bank IDs.** If a row has no IDs, the fit is low by definition. It is not padded with adjectives.
- **Percentages with judgement**: 90-100% when there is direct strength A evidence. 70-85% when there is B or adjacent evidence. 40-60% when there is only context. Below 40% is a gap.
- **No courtesy optimism.** An inflated fit makes the candidate lose weeks in a process they will not win.

Close the report with:

1. **Verdict**: apply / apply with reservations / do not apply. With one reason, not five.
2. **The 2 or 3 gaps that will decide the process**, cross-checked with section 6 of the bank.
3. **What to ask the candidate**: evidence marked `C` that would be decisive for this posting. Concrete questions, four at most. If none is relevant, ask nothing.
4. **The lever**: the one thing that, told well, gets them into the conversation.

If there are pending questions, carry on with phase 3 anyway **using only verified
evidence**, and make clear what would improve once they are answered. Never wait blocked.

---

## Phase 3: Build the application

### 3.1 Content selection

- **Headline**: the archetype's (section 5 of the bank), adjusted to the usable vocabulary of the posting.
- **Summary**: 4 or 5 lines. It must contain the most relevant strength A evidence, with its figure, and name any asset that has no section of its own on page 1.
- **CORE SKILLS**: 4 labelled lines, right after the summary. The most relevant for the posting goes first. It is the densest keyword area of the document and the one parsers index best. Every term needs evidence (rule 5 of the bank).
- **Selected project**: include the bank's featured project (if any) when the archetype is A or B. Leave it out in C, D and E.
- **Bullets per role**: at most 5 in the two most recent roles, 4 in the middle ones, 2 in the oldest. They are chosen by relevance to this posting, not by age.
- **Reordering**: within each role, the most relevant bullet goes first. The chronological order of the roles is never touched.

### 3.2 Rephrasing

Rephrasing yes, inventing no. The boundary:

- **Allowed**: changing the verb, changing the emphasis, using the company's vocabulary when it is marked as usable, choosing which part of the evidence is told, merging two pieces of evidence from the same role into one bullet, generalizing a very local business unit for an international audience.
- **Forbidden**: changing a figure, moving evidence to another role, adding an unevidenced technology, turning "designed" into "led", turning an own project into corporate work.

Every bullet: **action verb + what + how + measurable result**. No filler adjectives.
If a bullet has no result, it goes to the end of its role or it is dropped.

### 3.3 Generate the DOCX

Write the content in `applications/<folder>/cv-content.js` and generate the DOCX with
`CV_CONTENT=applications/<folder>/cv-content.js node tools/build-cv.js applications/<folder>/CV-<First-Last>.docx`.
That way every CV keeps its source and can be tweaked and regenerated months later.

A single CV, **one column and ATS-safe**. No format variants are generated.
The constraint is not "no design", it is no structures that break linear parsing.

Read the `docx` skill and follow its method. Specification:

**Forbidden, no exceptions.** Each of these breaks or degrades parsing:

- Tables of any kind, including those used only for layout
- Columns, text boxes, shapes, `frames`
- Page headers and footers. Contact details go in the body, in the first lines
- Photo, icons, charts, skill progress bars
- Tabs to right-align dates. Dates go on the company line, separated by bars
- Odd decorative characters. The long dash is forbidden by rule 7 of the bank anyway

**Structure**, in this order and with these headings in English (parsers recognize them):

1. Name
2. Headline
3. Contact details in two plain-text lines separated by bars
4. `PROFESSIONAL SUMMARY`
5. `CORE SKILLS`
6. `PROFESSIONAL EXPERIENCE`
7. `SELECTED PROJECT` (archetypes A and B only)
8. `EDUCATION AND LANGUAGES`
9. **Closing signature**, mandatory in every CV

**Closing signature.** Every CV ends with a signature line, always, no exceptions.
It is the last element of the document, after `EDUCATION AND LANGUAGES`. It is normal
text in the document flow (italic, grey, smaller body), not a Word footer: ATS systems
ignore footers, and this line must be read. Exact text:

> *No fancy design here, and that's on purpose: this CV is ATS-optimized so a machine reads it as well as you do.*

**Each role**: job title alone on its line (bold), and below it
`Company  |  City, Country  |  Month Year - Month Year`. Title and company are never mixed
on the same line. Months in English and in full.

**Bullets**: `bullet: { level: 0 }`. Never a hand-typed `•` character.

**Typography**: Arial. Name 20pt bold blue (`1F4E79`), section headings 10.5pt
bold blue with a blue bottom border, body 9.5pt (`2B2B2B`), metadata 9pt (`5A5A5A`).
One bold per bullet, on the figure or the result. Design is done with
typography, hierarchy and white space, not with structure.

**Page**: A4 (11906 x 16838 DXA), margins 720 top, 680 bottom, 880 left and right.
2 pages at most.

File name: `CV-<First-Last>.docx`, taking the name from section 1 of the bank
(for example `CV-Jane-Doe.docx`). The same name for every application. Never add
the company name or any other suffix: the company is already in the folder name.

**Mandatory verification.** First the automatic validator, then the manual parsing test.

0. **Automatic preflight.** `python3 tools/validate-cv.py applications/.../CV-<First-Last>.docx`.
   It reads the final DOCX, the `Messages.md` in the same folder and the bank, and returns a
   dossier in three blocks: blockers (long dashes, availability signals, hard gaps and terms
   without evidence from the section 10 watchlist, companies outside section 2, Latin American
   Spanish in any Spanish text, rule 8), warnings (terms of `C` evidence from section 10,
   figures not found in the bank, ranges that may merge metrics from two roles, doubtful
   Spanish markers, mixed UK and US English) and data to review (ATS reading order, skills
   terms, trace of every figure, volume, widow lines). It writes `VALIDATION.md` in the
   application folder. If the bank has no section 10, the validator warns: hard gaps go
   unchecked. It fixes nothing: it is a checklist. **If there is a blocker, it is not
   sent.** Python 3 only, no dependencies.

1. **Parsing test.** `pandoc -t plain --wrap=none file.docx`. Read it. If the reading
   order is not exactly the visual order, if something is interleaved or if the contact
   details are not in the first lines, the document is broken for an ATS and must be fixed.

The volume hint from `validate-cv.py` warns when the document gets close to the limit. If it
goes over 2 pages: first close the **widow lines** the validator reports (a single word
dangling at the end of a paragraph takes a whole line; trimming that word pulls it up and saves
a line, with no loss of content), then tighten line spacing and margins, then merge
bullets from the same role, and only at the end drop the least relevant bullet for this posting.
Never take the body below 9.5pt. Widow detection is an estimate from character width:
the visual render rules, but it points well to where to look.

### 3.4 Recruiter message

Two versions in a single `.md` file:

- **Short letter** (200-300 words): why this company, the evidence that proves it, what they would do differently. No "to whom it may concern", no "please find my CV attached", no summary of the CV.
- **LinkedIn message** (5 lines at most): one sentence of context, one piece of evidence with a figure, one question that invites a reply.

If there is a hard gap that will decide the process, **name it yourself in the last paragraph of the letter**,
never earlier and never in the CV. Acknowledging it after four paragraphs of evidence defuses
silent rejection. Acknowledging it early triggers it.

Both in the language of the posting. Rules 6, 7 and 8 of the bank apply in full:
no availability, no long dashes, one language variant per document.

---

## Deliverables

One folder per application, in `applications/{YYYY-MM}-{company}-{short-role}/`,
with these five files (plus `VALIDATION.md`, written by the validator):

1. `job-posting.md` (the original text of the posting, as is)
2. `Fit.md`
3. `cv-content.js` (the CV source)
4. `CV-<First-Last>.docx` (same name for all of them, no company)
5. `Messages.md`

Keeping the original posting is not bureaucracy: it is what lets you reread months later
why something was said, and compare applications with each other.

---

## Feeding back into the bank

When you finish, if new information about the candidate's career came up during the process
(a metric they confirmed, a project they mentioned, a team size), **propose the
evidence bank update** with the new ID and its full row. If a new hard gap came up, or new
evidence stays marked `C`, also propose its row for section 10 (watchlist), so the
validator keeps an eye on it. Do not edit the bank
without the candidate's approval: it is the source of truth and only they change it.

That is the loop that makes the system improve. Every application should leave the bank
better than it found it.

---

## What this system does not do

- It does not decide for the candidate whether to apply. It gives the verdict and the reason; the decision is theirs.
- It does not improve the fit by inventing. If the fit is poor, the report says so and that is it.
- It does not keep parallel versions of the CV by format. Just one, in one column.
- It does not write a software architecture. The DOCX generator is a replaceable implementation detail; the value is in the bank and in the method.
- It does not touch the evidence bank without permission.
- It does not convert the CV to PDF or ask about it. The deliverable is the `.docx`. The candidate gives the
  final approval and does the PDF conversion on their own.
