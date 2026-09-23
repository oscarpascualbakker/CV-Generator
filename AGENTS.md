# Sistema de CV a medida

Este repositorio genera candidaturas a partir de una oferta de trabajo: informe de encaje,
CV en DOCX seguro para ATS y mensajes al recruiter.

## Regla de oro

`CARRERA-EVIDENCIAS.md` es la fuente única de verdad sobre la carrera del candidato.
Nada entra en un CV, una carta o un mensaje si no tiene un identificador `EV-nn` en ese
fichero. Si falta información, se pregunta. Nunca se inventa.

Solo el candidato modifica el banco de evidencias. Tú puedes proponer cambios, no aplicarlos.

Los datos personales viven solo en ficheros que **no se versionan** (`CARRERA-EVIDENCIAS.md`,
`CANDIDATURAS.md`, `candidaturas/`). El repositorio público incluye
versiones de ejemplo ficticias (`*.example.*`). Ver `README.md`.

## Cómo se usa

El candidato pega una oferta de trabajo. Se activa la skill `cv-a-medida`
(`.agents/skills/cv-a-medida/SKILL.md`), que define el método completo en tres fases.
No improvises un proceso distinto: lee la skill y síguela. Si tu agente no carga skills
automáticamente, lee ese fichero antes de empezar.

## Estructura

```
AGENTS.md                      Estas instrucciones. Las lee cualquier agente (Codex, Cursor, Copilot...).
CLAUDE.md                      Solo importa AGENTS.md, para Claude Code.
CARRERA-EVIDENCIAS.md          Banco de evidencias (privado, no versionado). El activo real.
CARRERA-EVIDENCIAS.example.md  Banco de ejemplo ficticio, versionado.
.agents/skills/cv-a-medida/    El método. Se activa solo al pegar una oferta.
.claude/skills/cv-a-medida     Enlace simbólico a la anterior, para Claude Code.
.githooks/pre-commit           Bloquea commits con ficheros privados o datos de contacto.
tools/build-cv.js              Generador del DOCX (renderizador, sin datos). Reemplazable.
tools/cv-content.example.js    Plantilla ficticia de la fuente de un CV, versionada.
candidaturas/                  Una carpeta por candidatura, con la fuente de su CV (privado, no versionado).
```

## Convenciones de escritura

Aplican a todo lo que se produzca aquí, en cualquier idioma:

- Sin guiones largos (em-dash). Nunca.
- Español de España cuando el documento vaya en español.
- El CV va en inglés por defecto.
- Nada de señales de disponibilidad ni de urgencia en textos públicos.

## Antes de dar por bueno un CV

Las verificaciones son obligatorias y están detalladas en la skill:

0. `python3 tools/validate-cv.py <ruta-al-docx>` como pre-vuelo. Contrasta el CV contra las
   reglas del banco y produce el dossier a revisar antes de enviar. Si hay un bloqueante, no se envía.
1. `pandoc -t plain --wrap=none fichero.docx` para leer lo que ve un ATS.
