*English version at the end of this document: [read in English](#cv-tailoring-system-english).*

# Sistema de CV a medida

Convierte una oferta de trabajo en una candidatura completa. El valor no está en el código:
está en el banco de evidencias y en el método.

> [!CAUTION]
> **Revisa siempre tu CV antes de enviarlo a una empresa.** La IA puede cometer errores
> (una cifra cambiada, una fecha equivocada, un logro exagerado) que luego podrías lamentar
> en una entrevista. Lee el documento final de principio a fin y comprueba que puedes
> defender cada línea. Lo que se envía es responsabilidad tuya, no mía o de la IA.

## Puesta en marcha

> [!WARNING]
> **Windows: clona con los enlaces simbólicos activados.** Las skills de Claude Code
> (`.claude/skills/cv-a-medida` y `.claude/skills/cv-tailoring`) son enlaces simbólicos. Git en
> Windows los descarga por defecto como ficheros de texto, y entonces Claude Code no encuentra
> la skill y el sistema no se activa.
>
> Activa antes el modo desarrollador de Windows y clona así:
>
> ```bash
> git clone -c core.symlinks=true <url-del-repositorio>
> ```
>
> Si ya lo habías clonado, ejecuta `git config core.symlinks true`, borra
> `.claude/skills` y restáuralo con `git checkout -- .claude/skills`.
>
> En macOS y Linux no hace falta hacer nada.

```bash
cd tools && npm install
```

Requiere además `pandoc` para la verificación de parseo ATS.

Copia el banco de ejemplo y pon tus propios datos en la copia:

```bash
cp CARRERA-EVIDENCIAS.example.md CARRERA-EVIDENCIAS.md
```

Si prefieres usar el sistema en inglés, parte del banco en inglés: `cp CAREER-EVIDENCE.example.md CAREER-EVIDENCE.md`.

La fuente de cada CV (`cv-content.js`) la escribe la skill en la carpeta de su candidatura.
`tools/cv-content.example.js` es la plantilla ficticia que sirve de referencia.

### Atajo: crear tu banco de evidencias con IA

No hace falta rellenar `CARRERA-EVIDENCIAS.md` a mano. Abre el proyecto con tu agente
(Claude Code, Codex u otro), adjunta tu CV actual (o tu perfil de LinkedIn en texto) y pide algo como:

> "Convierte este CV al formato de `CARRERA-EVIDENCIAS.example.md`, con identificadores
> `EV-nn` y la cronología de la sección 2."

Dos avisos importantes, porque el sistema entero depende de ello:

- **La IA no debe inventar nada.** Solo puede volcar lo que ya está en tu CV. Cualquier
  métrica o logro que tu CV no diga, no entra: se marca como pendiente de confirmar (`C`).
- **Revisa el resultado antes de usarlo.** El banco es tu fuente de verdad; solo tú decides
  qué es correcto. Corrige cifras, fechas y nombres de empresa hasta que puedas defender
  cada línea en una entrevista.

El banco que genera la IA es un borrador tuyo, no un documento cerrado.

## Idioma

El sistema funciona entero en español o en inglés. Lo decide el banco, con la línea
`lang: es` o `lang: en` de su cabecera (sin ella, cuenta el nombre del fichero):

| | Español | Inglés |
|---|---|---|
| Banco | `CARRERA-EVIDENCIAS.md` | `CAREER-EVIDENCE.md` |
| Skill | `cv-a-medida` | `cv-tailoring` |
| Registro y carpetas | `CANDIDATURAS.md`, `candidaturas/` | `APPLICATIONS.md`, `applications/` |
| Ficheros de cada candidatura | `oferta.md`, `Encaje.md`, `Mensajes.md`, `VALIDACION.md` | `job-posting.md`, `Fit.md`, `Messages.md`, `VALIDATION.md` |
| Ejemplo | `candidaturas-ejemplo/` | `applications-example/` |

El idioma del sistema no es el del CV: el CV va en inglés por defecto, y la carta y el
mensaje, en el idioma de la oferta. Las reglas de texto del validador se aplican según el
idioma de cada texto: español de España en lo que se escriba en español, y una sola variante
(UK o US) en lo que se escriba en inglés.

## Privacidad: dónde viven tus datos

Todos tus datos personales viven en ficheros que **no se versionan** (están en `.gitignore`):

- `CARRERA-EVIDENCIAS.md`   el banco de evidencias, la fuente única de verdad
- `CANDIDATURAS.md`         tu registro de candidaturas
- `candidaturas/`           una carpeta por candidatura: oferta, informe, fuente del CV, CV y mensajes

Y sus equivalentes en inglés (`CAREER-EVIDENCE.md`, `APPLICATIONS.md`, `applications/`).

El repositorio público solo contiene versiones de ejemplo ficticias (`*.example.*`, persona
"Jane Doe"). Si clonas esto, empieza copiando los ejemplos como se indica arriba. Antes de
publicar tu propio fork, comprueba que `git status` no lista ninguno de los ficheros privados.

### Barrera contra fugas

`.gitignore` evita que tus ficheros privados entren por descuido, pero no impide un
`git add -f`, ni que copies tu email en un fichero público. Para eso hay un hook de pre-commit
en `.githooks/`. Actívalo una vez después de clonar:

```bash
git config core.hooksPath .githooks
```

Bloquea cualquier commit que incluya un fichero privado o que contenga tus datos de contacto
(nombre, teléfono, email, LinkedIn y GitHub), que lee de la sección 1 de tu banco.
Git no activa hooks automáticamente al clonar por seguridad: este paso es obligatorio.

## Uso

Abre el proyecto con tu agente y pega una oferta de trabajo. La skill del idioma de tu banco
(`cv-a-medida` o `cv-tailoring`) se activa sola y ejecuta las tres fases:

1. **Descomponer la oferta**: requisitos atómicos, arquetipo de puesto y léxico usable.
2. **Informe de encaje**: encaje por área justificado con identificadores del banco, huecos y veredicto.
3. **Construir**: CV en DOCX de una columna, carta y mensaje de LinkedIn.

El resultado queda en `candidaturas/{AAAA-MM}-{empresa}-{puesto}/`.

Antes de enviar nada, la skill pasa `tools/validate-cv.py`, que contrasta el CV y los mensajes
con el banco y deja un informe en la carpeta de la candidatura. Lo que depende de tu carrera
(huecos duros, términos sin evidencia, evidencias sin confirmar) no está en el código: lo lee
de la sección 10 del banco, la **lista de vigilancia**. Si tu banco no la tiene, el validador
lo avisa. Mira la del banco de ejemplo para ver el formato.

## Los tres principios

**El conocimiento vive fuera del código.** El banco de evidencias y la skill son el sistema.
`build-cv.js` es un generador que se puede tirar y reescribir sin perder nada.

**Nada sin evidencia.** Cada afirmación del CV apunta a un identificador `EV-nn`. Los huecos
se reconocen, no se rellenan. Un CV que no puedas defender veinte minutos en una entrevista
es peor que no enviar nada.

**Un solo CV, seguro para ATS.** Una columna, sin tablas, sin cuadros de texto, sin cabeceras.
El diseño se hace con tipografía y espacio en blanco.

## Compatibilidad entre agentes

El proyecto no depende de ninguna herramienta concreta:

- `AGENTS.md` tiene las instrucciones del proyecto. Es el estándar que leen Codex, Cursor,
  GitHub Copilot y otros agentes.
- `CLAUDE.md` solo contiene `@AGENTS.md`, porque Claude Code lee su propio fichero y no `AGENTS.md`.
- Las skills viven en `.agents/skills/` (`cv-a-medida` y `cv-tailoring`), donde las busca Codex.
  `.claude/skills/` tiene un enlace simbólico a cada una, porque Claude Code solo busca skills
  ahí. Se edita un único fichero por skill.
- En Windows hay que clonar con los enlaces simbólicos activados. Ver el aviso de
  [Puesta en marcha](#puesta-en-marcha).

## Mantenimiento

Cada candidatura debería dejar el banco mejor de lo que lo encontró. La sección 8 del banco
lleva la lista de lo que falta por documentar, ordenada por retorno, y la sección 10, lo que
el validador tiene que vigilar.

Las dos skills y los dos bancos de ejemplo son gemelos: un cambio en el método se hace en los
dos idiomas. Los textos del validador tienen sus dos versiones juntas en
`tools/cvcheck/messages.py`.

---

# CV Tailoring System (English)

*[Versión en español](#sistema-de-cv-a-medida) al principio de este documento.*

Turns a job posting into a complete application. The value is not in the code:
it is in the evidence bank and the method.

> [!CAUTION]
> **Always review your CV before sending it to a company.** AI can make mistakes
> (a changed figure, a wrong date, an exaggerated achievement) that you might regret
> in an interview. Read the final document from start to finish and check that you can
> defend every line. What gets sent is your responsibility, not mine or the AI's.

## Getting started

> [!WARNING]
> **Windows: clone with symbolic links enabled.** The Claude Code skills
> (`.claude/skills/cv-tailoring` and `.claude/skills/cv-a-medida`) are symbolic links. By default,
> Git on Windows checks symlinks out as plain text files, and then Claude Code cannot find the
> skill and the system does not activate.
>
> Enable Windows Developer Mode first and clone like this:
>
> ```bash
> git clone -c core.symlinks=true <repository-url>
> ```
>
> If you had already cloned it, run `git config core.symlinks true`, delete
> `.claude/skills` and restore it with `git checkout -- .claude/skills`.
>
> On macOS and Linux there is nothing to do.

```bash
cd tools && npm install
```

It also requires `pandoc` for the ATS parsing check.

Copy the example bank and put your own data in the copy:

```bash
cp CAREER-EVIDENCE.example.md CAREER-EVIDENCE.md
```

That runs the whole system in English. To use it in Spanish, start from `CARRERA-EVIDENCIAS.example.md` instead.

The source of each CV (`cv-content.js`) is written by the skill into its application folder.
`tools/cv-content.example.js` is the fictional template used as a reference.

### Shortcut: build your evidence bank with AI

You don't need to fill in `CAREER-EVIDENCE.md` by hand. Open the project with your agent
(Claude Code, Codex or another), attach your current CV (or your LinkedIn profile as text) and ask something like:

> "Convert this CV to the format of `CAREER-EVIDENCE.example.md`, with `EV-nn`
> identifiers and the timeline from section 2."

Two important warnings, because the whole system depends on them:

- **The AI must not invent anything.** It can only transfer what is already in your CV. Any
  metric or achievement your CV does not state stays out: it is marked as pending confirmation (`C`).
- **Review the result before using it.** The bank is your source of truth; only you decide
  what is correct. Fix figures, dates and company names until you can defend
  every line in an interview.

The bank the AI generates is your draft, not a finished document.

## Language

The whole system works in English or in Spanish. The bank decides, with the `lang: en`
or `lang: es` line in its header (without it, the file name counts):

| | English | Spanish |
|---|---|---|
| Bank | `CAREER-EVIDENCE.md` | `CARRERA-EVIDENCIAS.md` |
| Skill | `cv-tailoring` | `cv-a-medida` |
| Log and folders | `APPLICATIONS.md`, `applications/` | `CANDIDATURAS.md`, `candidaturas/` |
| Files in each application | `job-posting.md`, `Fit.md`, `Messages.md`, `VALIDATION.md` | `oferta.md`, `Encaje.md`, `Mensajes.md`, `VALIDACION.md` |
| Example | `applications-example/` | `candidaturas-ejemplo/` |

The system language is not the CV language: the CV is in English by default, and the letter
and message follow the language of the posting. The validator applies its text rules by the
language of each text: one variant (UK or US) in anything written in English, and Spain
Spanish in anything written in Spanish.

## Privacy: where your data lives

All your personal data lives in files that are **not versioned** (they are in `.gitignore`):

- `CAREER-EVIDENCE.md`      the evidence bank, the single source of truth
- `APPLICATIONS.md`         your application log
- `applications/`           one folder per application: job posting, report, CV source, CV and messages

And their Spanish equivalents (`CARRERA-EVIDENCIAS.md`, `CANDIDATURAS.md`, `candidaturas/`).

The public repository only contains fictional example versions (`*.example.*`, persona
"Jane Doe"). If you clone this, start by copying the examples as described above. Before
publishing your own fork, check that `git status` does not list any of the private files.

### Leak barrier

`.gitignore` keeps your private files from slipping in by accident, but it does not stop a
`git add -f`, or you pasting your email into a public file. That is what the pre-commit hook
in `.githooks/` is for. Enable it once after cloning:

```bash
git config core.hooksPath .githooks
```

It blocks any commit that includes a private file or contains your contact details
(name, phone, email, LinkedIn and GitHub), which it reads from section 1 of your bank.
For security reasons, Git does not enable hooks automatically on clone: this step is mandatory.

## Usage

Open the project with your agent and paste a job posting. The skill for your bank's language
(`cv-tailoring` or `cv-a-medida`) activates on its own and runs three phases:

1. **Break down the posting**: atomic requirements, role archetype and usable vocabulary.
2. **Fit report**: fit per area, backed by bank identifiers, gaps and a verdict.
3. **Build**: single-column DOCX CV, cover letter and LinkedIn message.

The output lands in `applications/{YYYY-MM}-{company}-{role}/`.

Before anything is sent, the skill runs `tools/validate-cv.py`, which checks the CV and the
messages against the bank and leaves a report in the application folder. Whatever depends on
your career (hard gaps, terms without evidence, unconfirmed evidence) is not in the code: it
reads it from section 10 of the bank, the **watchlist**. If your bank does not have one, the
validator warns you. See the example bank's for the format.

## The three principles

**Knowledge lives outside the code.** The evidence bank and the skill are the system.
`build-cv.js` is a generator you can throw away and rewrite without losing anything.

**Nothing without evidence.** Every claim in the CV points to an `EV-nn` identifier. Gaps
are acknowledged, not filled. A CV you cannot defend for twenty minutes in an interview
is worse than sending nothing.

**One CV, ATS-safe.** One column, no tables, no text boxes, no headers.
The design is done with typography and white space.

## Cross-agent compatibility

The project does not depend on any specific tool:

- `AGENTS.md` holds the project instructions. It is the standard read by Codex, Cursor,
  GitHub Copilot and other agents.
- `CLAUDE.md` only contains `@AGENTS.md`, because Claude Code reads its own file and not `AGENTS.md`.
- The skills live in `.agents/skills/` (`cv-tailoring` and `cv-a-medida`), where Codex looks for them.
  `.claude/skills/` has a symbolic link to each, because Claude Code only looks for skills
  there. A single file is edited per skill.
- On Windows you must clone with symbolic links enabled. See the warning in
  [Getting started](#getting-started).

## Maintenance

Every application should leave the bank better than it found it. Section 8 of the bank
keeps the list of what is still to be documented, ordered by payoff, and section 10 what the
validator has to watch.

The two skills and the two example banks are twins: a change to the method is made in both
languages. The validator strings keep their two versions side by side in
`tools/cvcheck/messages.py`.
