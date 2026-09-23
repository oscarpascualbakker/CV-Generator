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
> **Windows: clona con los enlaces simbólicos activados.** La skill de Claude Code
> (`.claude/skills/cv-a-medida`) es un enlace simbólico. Git en Windows los descarga por defecto
> como ficheros de texto, y entonces Claude Code no encuentra la skill y el sistema no se activa.
>
> Activa antes el modo desarrollador de Windows y clona así:
>
> ```bash
> git clone -c core.symlinks=true <url-del-repositorio>
> ```
>
> Si ya lo habías clonado, ejecuta `git config core.symlinks true`, borra
> `.claude/skills/cv-a-medida` y restáuralo con `git checkout -- .claude/skills/cv-a-medida`.
>
> En macOS y Linux no hace falta hacer nada.

```bash
cd tools && npm install
```

Requiere además `pandoc` para la verificación de parseo ATS.

Copia los ficheros de ejemplo y pon tus propios datos en las copias:

```bash
cp CARRERA-EVIDENCIAS.example.md CARRERA-EVIDENCIAS.md
```

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

## Privacidad: dónde viven tus datos

Todos tus datos personales viven en ficheros que **no se versionan** (están en `.gitignore`):

- `CARRERA-EVIDENCIAS.md`   el banco de evidencias, la fuente única de verdad
- `CANDIDATURAS.md`         tu registro de candidaturas
- `candidaturas/`           una carpeta por candidatura: oferta, informe, fuente del CV, CV y mensajes

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
(nombre, teléfono, email, LinkedIn y GitHub), que lee de la sección 1 de tu `CARRERA-EVIDENCIAS.md`.
Git no activa hooks automáticamente al clonar por seguridad: este paso es obligatorio.

## Uso

Abre el proyecto con tu agente y pega una oferta de trabajo. La skill `cv-a-medida` se
activa sola y ejecuta las tres fases:

1. **Descomponer la oferta**: requisitos atómicos, arquetipo de puesto y léxico usable.
2. **Informe de encaje**: encaje por área justificado con identificadores del banco, huecos y veredicto.
3. **Construir**: CV en DOCX de una columna, carta y mensaje de LinkedIn.

El resultado queda en `candidaturas/{AAAA-MM}-{empresa}-{puesto}/`.

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
- La skill vive en `.agents/skills/cv-a-medida/`, donde la busca Codex.
  `.claude/skills/cv-a-medida` es un enlace simbólico a esa carpeta, porque Claude Code solo
  busca skills en `.claude/skills/`. Se edita un único fichero.
- En Windows hay que clonar con los enlaces simbólicos activados. Ver el aviso de
  [Puesta en marcha](#puesta-en-marcha).

## Mantenimiento

Cada candidatura debería dejar el banco mejor de lo que lo encontró. La sección 8 de
`CARRERA-EVIDENCIAS.md` lleva la lista de lo que falta por documentar, ordenada por retorno.
