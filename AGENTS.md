*English version at the end of this document: [read in English](#cv-tailoring-system-english).*

# Sistema de CV a medida

Este repositorio genera candidaturas a partir de una oferta de trabajo: informe de encaje,
CV en DOCX seguro para ATS y mensajes al recruiter. Funciona en español o en inglés.

## Regla de oro

El banco de evidencias es la fuente única de verdad sobre la carrera del candidato:
`CARRERA-EVIDENCIAS.md` en español, `CAREER-EVIDENCE.md` en inglés. Nada entra en un CV,
una carta o un mensaje si no tiene un identificador `EV-nn` en ese fichero. Si falta
información, se pregunta. Nunca se inventa.

Solo el candidato modifica el banco de evidencias. Tú puedes proponer cambios, no aplicarlos.

Los datos personales viven solo en ficheros que **no se versionan** (el banco,
`CANDIDATURAS.md` / `APPLICATIONS.md`, `candidaturas/` / `applications/`). El repositorio
público incluye versiones de ejemplo ficticias (`*.example.*`). Ver `README.md`.

## Idioma

El idioma del sistema lo fija el banco: la línea `lang: es` o `lang: en` de su cabecera
(sin ella, se deduce del nombre del fichero). Decide qué skill se usa, los nombres de los
ficheros de cada candidatura y el idioma del informe del validador. No depende del idioma
de la oferta: el CV va en inglés por defecto, y la carta y el mensaje, en el de la oferta.

## Cómo se usa

El candidato pega una oferta de trabajo. Se activa la skill del idioma del banco, que define
el método completo en tres fases:

- `cv-a-medida` (`.agents/skills/cv-a-medida/SKILL.md`) si el banco está en español.
- `cv-tailoring` (`.agents/skills/cv-tailoring/SKILL.md`) si está en inglés.

No improvises un proceso distinto: lee la skill y síguela. Si tu agente no carga skills
automáticamente, lee ese fichero antes de empezar. Si existen los dos bancos, pregunta cuál usar.

## Estructura

```
AGENTS.md                      Estas instrucciones. Las lee cualquier agente (Codex, Cursor, Copilot...).
CLAUDE.md                      Solo importa AGENTS.md, para Claude Code.
CARRERA-EVIDENCIAS.md          Banco de evidencias en español (privado, no versionado). El activo real.
CAREER-EVIDENCE.md             Lo mismo, si el sistema va en inglés.
*.example.md                   Bancos de ejemplo ficticios, versionados, uno por idioma.
.agents/skills/cv-a-medida/    El método en español. Se activa solo al pegar una oferta.
.agents/skills/cv-tailoring/   El mismo método en inglés.
.claude/skills/                Enlaces simbólicos a las dos anteriores, para Claude Code.
.githooks/pre-commit           Bloquea commits con ficheros privados o datos de contacto.
tools/build-cv.js              Generador del DOCX (renderizador, sin datos). Reemplazable.
tools/cv-content.example.js    Plantilla ficticia de la fuente de un CV, versionada.
tools/validate-cv.py           Validador del CV antes de enviarlo.
tools/cvcheck/                 Lectura del banco, reglas de texto por idioma y textos del informe.
candidaturas/, applications/   Una carpeta por candidatura, con la fuente de su CV (privado, no versionado).
candidaturas-ejemplo/,
applications-example/          Una candidatura de ejemplo ficticia, en cada idioma.
```

## Convenciones de escritura

Aplican a todo lo que se produzca aquí, en cualquier idioma:

- Sin guiones largos (em-dash). Nunca.
- Español de España cuando el documento vaya en español.
- En inglés, una sola variante (UK o US) por documento.
- El CV va en inglés por defecto.
- Nada de señales de disponibilidad ni de urgencia en textos públicos.

## Si modificas el sistema

Las dos skills y los dos bancos de ejemplo son gemelos: un cambio en el método se hace en los
dos idiomas. Los textos del validador tienen sus dos versiones juntas en
`tools/cvcheck/messages.py`.

## Antes de dar por bueno un CV

Las verificaciones son obligatorias y están detalladas en la skill:

0. `python3 tools/validate-cv.py <ruta-al-docx>` como pre-vuelo. Contrasta el CV contra las
   reglas del banco (incluida su lista de vigilancia, sección 10) y produce el dossier a
   revisar antes de enviar. Si hay un bloqueante, no se envía.
1. `pandoc -t plain --wrap=none fichero.docx` para leer lo que ve un ATS.

---

# CV Tailoring System (English)

*[Versión en español](#sistema-de-cv-a-medida) al principio de este documento.*

This repository builds job applications from a job posting: a fit report, an ATS-safe
DOCX CV and messages to the recruiter. It works in Spanish or in English.

## Golden rule

The evidence bank is the single source of truth about the candidate's career:
`CAREER-EVIDENCE.md` in English, `CARRERA-EVIDENCIAS.md` in Spanish. Nothing goes into a CV,
a letter or a message unless it has an `EV-nn` identifier in that file. If information is
missing, ask. Never invent.

Only the candidate changes the evidence bank. You may propose changes, not apply them.

Personal data lives only in files that are **not versioned** (the bank,
`APPLICATIONS.md` / `CANDIDATURAS.md`, `applications/` / `candidaturas/`). The public
repository includes fictional example versions (`*.example.*`). See `README.md`.

## Language

The bank sets the system language: the `lang: en` or `lang: es` line in its header
(without it, the file name decides). It picks the skill, the file names in each application
and the language of the validator report. It does not depend on the language of the
posting: the CV is in English by default, and the letter and message follow the posting.

## How it is used

The candidate pastes a job posting. The skill for the bank's language activates and
defines the full three-phase method:

- `cv-tailoring` (`.agents/skills/cv-tailoring/SKILL.md`) if the bank is in English.
- `cv-a-medida` (`.agents/skills/cv-a-medida/SKILL.md`) if it is in Spanish.

Do not improvise a different process: read the skill and follow it. If your agent does not
load skills automatically, read that file before starting. If both banks exist, ask which one to use.

## Structure

```
AGENTS.md                      These instructions. Any agent reads them (Codex, Cursor, Copilot...).
CLAUDE.md                      Only imports AGENTS.md, for Claude Code.
CAREER-EVIDENCE.md             Evidence bank in English (private, not versioned). The real asset.
CARRERA-EVIDENCIAS.md          The same, if the system runs in Spanish.
*.example.md                   Fictional example banks, versioned, one per language.
.agents/skills/cv-tailoring/   The method in English. Activates on its own when a posting is pasted.
.agents/skills/cv-a-medida/    The same method in Spanish.
.claude/skills/                Symbolic links to both, for Claude Code.
.githooks/pre-commit           Blocks commits with private files or contact details.
tools/build-cv.js              DOCX generator (renderer, no data). Replaceable.
tools/cv-content.example.js    Fictional template for a CV source, versioned.
tools/validate-cv.py           CV validator, run before sending.
tools/cvcheck/                 Bank reader, per-language text rules and report strings.
applications/, candidaturas/   One folder per application, with its CV source (private, not versioned).
applications-example/,
candidaturas-ejemplo/          A fictional example application, in each language.
```

## Writing conventions

They apply to everything produced here, in any language:

- No long dashes (em-dash). Ever.
- Spain Spanish when the document is in Spanish.
- In English, one variant (UK or US) per document.
- The CV is in English by default.
- No availability or urgency signals in public texts.

## If you change the system

The two skills and the two example banks are twins: a change to the method is made in both
languages. The validator strings keep their two versions side by side in
`tools/cvcheck/messages.py`.

## Before accepting a CV

These checks are mandatory and detailed in the skill:

0. `python3 tools/validate-cv.py <path-to-docx>` as a preflight. It checks the CV against the
   bank's rules (including its watchlist, section 10) and produces the dossier to review
   before sending. If there is a blocker, it is not sent.
1. `pandoc -t plain --wrap=none file.docx` to read what an ATS sees.
