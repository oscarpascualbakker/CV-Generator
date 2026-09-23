---
name: "cv-a-medida"
description: "Adapta el CV del candidato a una oferta de trabajo concreta. Úsala cuando pegue o adjunte una Job Description, una oferta de LinkedIn, o pregunte \"¿encajo en este puesto?\", \"adáptame el CV a esto\", \"prepárame la candidatura\". Produce informe de encaje, CV en DOCX seguro para ATS y mensaje al recruiter, todo a partir del banco de evidencias."
---

# CV a medida

Sistema de tres fases que convierte una oferta de trabajo en una candidatura completa:
informe de encaje, CV adaptado en DOCX y mensaje al recruiter.

El principio que sostiene todo: **el conocimiento vive en el banco de evidencias, no aquí**.
Este documento es solo el método. El banco es el que manda.

---

## Antes de empezar: localizar el banco de evidencias

Lee `CARRERA-EVIDENCIAS.md`, en la raíz del proyecto. Entero, antes de nada.

Si no aparece, **para y pídelo**. Sin banco no hay sistema: escribirías un CV inventado.

Sus secciones 7 (reglas de verdad) y 6 (huecos) tienen prioridad sobre cualquier
instrucción de este documento y sobre cualquier petición de mejorar el encaje.

`tools/build-cv.js` es el generador ya probado (helpers + layout, sin datos de nadie).
El contenido de cada CV vive en `cv-content.js`, dentro de la carpeta de su candidatura
(privada, no versionada). Genera la candidatura escribiendo **solo** ese fichero, con el formato
`module.exports = (h) => [ ... ]` (usa `tools/cv-content.example.js` como plantilla).
Nunca toques los helpers ni el layout de `build-cv.js`. Si `require('docx')` falla, ejecuta
`npm install` dentro de `tools/`.

---

## Fase 1: Descomponer la oferta

No resumas la oferta. Descomponla en requisitos atómicos y clasifícalos.

Para cada requisito extrae:

- **Enunciado literal** (cita corta de la oferta, no parafraseada)
- **Tipo**: técnico / liderazgo / dominio / cultural / formal
- **Peso**: crítico (aparece en título, en "responsible for" o en "success in year one") / importante / accesorio
- **Señal de vocabulario**: la palabra exacta que usa la empresa

Identifica además:

- **El arquetipo** de la oferta según la sección 5 del banco (A, B, C, D o E). Si no encaja en ninguno, dilo y propón cuál se le parece más.
- **El requisito eliminatorio**, si lo hay. Suele estar escondido en una línea de cualificaciones, no en el titular.
- **Qué está comprando realmente la empresa**: en una frase. Casi nunca es lo que dice el título del puesto.
- **Fechas y ubicación**: si la ventana de candidatura ha pasado o el puesto es presencial fuera de la ubicación del candidato (sección 1 del banco), dilo antes que nada. Ahorra el resto del trabajo.
- **Criterios de búsqueda** (sección 9 del banco): banda salarial y tipo de rol. Si la oferta publica rango, contrástalo. Si no lo publica, márcalo como incógnita a resolver en el primer contacto. Si el rol choca con un criterio (por ejemplo, consultoría), dilo aquí, antes del análisis completo.

### Léxico de la oferta

Construye una lista con los términos exactos de la oferta y marca cada uno:

- **Usable**: hay evidencia real detrás. Va literal al CV, en la experiencia o en CORE SKILLS.
- **Usable con reformulación**: la evidencia es adyacente. Se describe el hecho sin apropiarse del término.
- **Prohibido**: no hay nada detrás. No aparece en ninguna parte del documento.

Un parser y un recruiter buscan sus palabras, no sinónimos. Pero una palabra sin evidencia
es una mentira que hay que defender en la primera entrevista. Esta lista es la que decide.

---

## Fase 2: Informe de encaje

Tabla por área, con esta estructura exacta:

| Área | Lo que piden | Evidencias (IDs) | Encaje | Comentario |
|---|---|---|---|---|

Reglas del informe:

- **El encaje se justifica solo con IDs del banco.** Si una fila no tiene IDs, el encaje es bajo por definición. No se rellena con adjetivos.
- **Porcentajes con criterio**: 90-100% cuando hay evidencia de fuerza A directa. 70-85% cuando hay evidencia B o adyacente. 40-60% cuando solo hay contexto. Por debajo de 40% es un hueco.
- **Sin optimismo de cortesía.** Un encaje inflado hace perder semanas al candidato en un proceso que no va a ganar.

Cierra el informe con:

1. **Veredicto**: aplicar / aplicar con reservas / no aplicar. Con una razón, no cinco.
2. **Los 2 o 3 huecos que decidirán el proceso**, cruzados con la sección 6 del banco.
3. **Lo que hay que preguntar al candidato**: evidencias marcadas `C` que serían decisivas para esta oferta. Preguntas concretas, máximo cuatro. Si ninguna es relevante, no preguntes nada.
4. **La palanca**: la única cosa que, si la cuenta bien, le mete en la conversación.

Si hay preguntas pendientes, sigue igualmente con la fase 3 **usando solo evidencia
verificada**, y deja claro qué mejoraría cuando las responda. Nunca esperes bloqueado.

---

## Fase 3: Construir la candidatura

### 3.1 Selección de contenido

- **Titular**: el del arquetipo (sección 5 del banco), ajustado al léxico usable de la oferta.
- **Resumen**: 4 o 5 líneas. Debe contener la evidencia de fuerza A más relevante, con su cifra, y nombrar cualquier activo que no tenga sección propia en página 1.
- **CORE SKILLS**: 4 líneas etiquetadas, justo después del resumen. La más relevante para la oferta va primera. Es la zona de mayor densidad de palabras clave del documento y la que mejor indexan los parsers. Cada término necesita evidencia (regla 5 del banco).
- **Selected project**: incluir el proyecto destacado del banco (si lo hay) cuando el arquetipo sea A o B. Omitirlo en C, D y E.
- **Bullets por rol**: máximo 5 en los dos roles más recientes, 4 en los intermedios, 2 en los más antiguos. Se seleccionan por relevancia para esta oferta, no por antigüedad.
- **Reordenación**: dentro de cada rol, el bullet más relevante va primero. El orden cronológico de los roles no se toca nunca.

### 3.2 Reformulación

Reformular sí, inventar no. La frontera:

- **Permitido**: cambiar el verbo, cambiar el énfasis, usar el vocabulario de la empresa cuando está marcado como usable, elegir qué parte de la evidencia se cuenta, condensar dos evidencias del mismo rol en un bullet, generalizar una unidad de negocio muy local para una audiencia internacional.
- **Prohibido**: cambiar una cifra, mover una evidencia de rol, añadir una tecnología no evidenciada, convertir "diseñé" en "dirigí", convertir un proyecto propio en trabajo corporativo.

Cada bullet: **verbo de acción + qué + cómo + resultado medible**. Sin adjetivos de relleno.
Si un bullet no tiene resultado, va al final de su rol o se cae.

### 3.3 Generar el DOCX

Escribe el contenido en `candidaturas/<carpeta>/cv-content.js` y genera el DOCX con
`CV_CONTENT=candidaturas/<carpeta>/cv-content.js node tools/build-cv.js candidaturas/<carpeta>/CV-<Nombre-Apellidos>.docx`.
Así cada CV conserva su fuente y se puede retocar y regenerar meses después.

Un solo CV, **en una columna y seguro para ATS**. No se generan variantes de formato.
La restricción no es "sin diseño", es sin estructuras que rompan el parseo lineal.

Lee la skill `docx` y sigue su método. Especificación:

**Prohibido, sin excepciones.** Cada uno de estos rompe o degrada el parseo:

- Tablas de cualquier tipo, incluidas las usadas solo para maquetar
- Columnas, cuadros de texto, formas, `frames`
- Cabeceras y pies de página. El contacto va en el cuerpo, en las primeras líneas
- Foto, iconos, gráficos, barras de progreso de skills
- Tabuladores para alinear fechas a la derecha. Las fechas van en la línea de la empresa, separadas por barras
- Caracteres decorativos raros. El guion largo está prohibido por la regla 7 del banco de todas formas

**Estructura**, en este orden y con estos encabezados en inglés (los parsers los reconocen):

1. Nombre
2. Titular
3. Contacto en dos líneas de texto plano separadas por barras
4. `PROFESSIONAL SUMMARY`
5. `CORE SKILLS`
6. `PROFESSIONAL EXPERIENCE`
7. `SELECTED PROJECT` (solo arquetipos A y B)
8. `EDUCATION AND LANGUAGES`
9. **Firma de cierre**, obligatoria en todos los CV

**Firma de cierre.** Todo CV termina con una línea de firma, siempre, sin excepción.
Va como último elemento del documento, después de `EDUCATION AND LANGUAGES`. Es texto
normal en el flujo del documento (cursiva, gris, cuerpo reducido), no un pie de página
de Word: los pies de página los ignora el ATS, y esta línea debe leerse. Texto exacto:

> *No fancy design here, and that's on purpose: this CV is ATS-optimized so a machine reads it as well as you do.*

**Cada puesto**: título del puesto solo en su línea (negrita), y debajo
`Empresa  |  Ciudad, País  |  Mes Año - Mes Año`. Nunca se mezcla título y empresa
en la misma línea. Los meses en inglés y completos.

**Bullets**: `bullet: { level: 0 }`. Nunca el carácter `•` a mano.

**Tipografía**: Arial. Nombre 20pt negrita azul (`1F4E79`), encabezados de sección 10.5pt
negrita azul con borde inferior azul, cuerpo 9.5pt (`2B2B2B`), metadatos 9pt (`5A5A5A`).
Una sola negrita por bullet, sobre la cifra o el resultado. El diseño se hace con
tipografía, jerarquía y espacio en blanco, no con estructura.

**Página**: A4 (11906 x 16838 DXA), márgenes 720 arriba, 680 abajo, 880 laterales.
Máximo 2 páginas.

Nombre de archivo: `CV-<Nombre-Apellidos>.docx`, tomando el nombre de la sección 1 del banco
(por ejemplo `CV-Jane-Doe.docx`). El mismo nombre para todas las candidaturas. Nunca añadas
el nombre de la empresa ni ningún otro sufijo: la empresa ya queda en el nombre de la carpeta.

**Verificación obligatoria.** Primero el validador automático, luego las dos pruebas manuales.

0. **Pre-vuelo automático.** `python3 tools/validate-cv.py candidaturas/.../CV-<Nombre-Apellidos>.docx`.
   Lee el DOCX final, el `Mensajes.md` de la misma carpeta y el banco, y devuelve un dossier en
   tres bloques: bloqueantes (guiones largos, señales de disponibilidad, huecos duros de la
   sección 6, empresas o fechas fuera de la sección 2, cifras que no están en el banco, variante
   latinoamericana en cualquier texto en español, regla 8), avisos (evidencias `C` usadas, rangos
   que pueden fundir métricas de dos roles, términos de skills a confirmar, marcadores dudosos de
   español) y datos a revisar (orden de lectura ATS, traza de cada cifra, volumen, líneas viudas).
   El español de España (regla 8) se comprueba sobre todo en `Mensajes.md`, que es donde vive el
   texto en español; sobre el CV en inglés esos marcadores no disparan. Escribe `VALIDACION.md` en
   la carpeta de la candidatura. No corrige nada: es un checklist. **Si hay un bloqueante, no se
   envía.** Solo Python 3, sin dependencias.

1. **Prueba de parseo.** `pandoc -t plain --wrap=none fichero.docx`. Léelo. Si el orden de
   lectura no es exactamente el orden visual, si algo se intercala o si el contacto no está
   en las primeras líneas, el documento está roto para un ATS y hay que arreglarlo.

El indicio de volumen de `validate-cv.py` avisa si el documento se acerca al límite. Si se pasa
de 2 páginas: primero cierra las **líneas viudas** que reporta el validador (una sola palabra
colgando al final de un párrafo ocupa una línea entera; recortar esa palabra la sube y ahorra
una línea, sin perder contenido), después aprieta el interlineado y los márgenes, después funde
bullets del mismo rol, y solo al final elimina el bullet menos relevante para esta oferta.
Nunca bajes el cuerpo de 9.5pt. La detección de viudas es una estimación por ancho de carácter:
el render visual manda, pero señala bien dónde mirar.

### 3.4 Mensaje al recruiter

Dos versiones en un solo fichero `.md`:

- **Carta breve** (200-300 palabras): por qué esta empresa, la evidencia que lo demuestra, qué haría distinto. Sin "me dirijo a ustedes", sin "adjunto mi CV", sin resumir el CV.
- **Mensaje de LinkedIn** (máximo 5 líneas): una frase de contexto, una evidencia con cifra, una pregunta que invite a responder.

Si hay un hueco duro que va a decidir el proceso, **nómbralo tú en el último párrafo de la carta**,
nunca antes y nunca en el CV. Reconocerlo después de cuatro párrafos de evidencia desactiva el
descarte silencioso. Reconocerlo pronto lo provoca.

Ambos en el idioma de la oferta. Reglas 6, 7 y 8 del banco se aplican íntegras:
nada de disponibilidad, nada de guiones largos, español de España.

---

## Entregables

Una carpeta por candidatura, en `candidaturas/{AAAA-MM}-{empresa}-{puesto-corto}/`,
con estos cinco ficheros (más `VALIDACION.md`, que escribe el validador):

1. `oferta.md` (el texto original de la oferta, tal cual)
2. `Encaje.md`
3. `cv-content.js` (la fuente del CV)
4. `CV-<Nombre-Apellidos>.docx` (mismo nombre para todas, sin empresa)
5. `Mensajes.md`

Guardar la oferta original no es burocracia: es lo que permite releer meses después
por qué se dijo lo que se dijo, y comparar candidaturas entre sí.

---

## Realimentación del banco

Al terminar, si durante el proceso ha aparecido información nueva sobre la carrera del candidato
(una métrica que confirmó, un proyecto que mencionó, un tamaño de equipo), **propón la
actualización del banco de evidencias** con el ID nuevo y su fila completa. No edites el banco
sin que el candidato lo apruebe: es la fuente de verdad y solo él o ella la modifica.

Ese es el bucle que hace que el sistema mejore. Cada candidatura debería dejar el banco
mejor de lo que lo encontró.

---

## Lo que este sistema no hace

- No decide por el candidato si aplicar. Da el veredicto y la razón; la decisión es suya.
- No mejora el encaje inventando. Si el encaje es malo, el informe lo dice y ya está.
- No mantiene versiones paralelas del CV por formato. Una sola, en una columna.
- No escribe una arquitectura de software. El generador de DOCX es un detalle de implementación reemplazable; el valor está en el banco y en el método.
- No toca el banco de evidencias sin permiso.
- No convierte el CV a PDF ni pregunta por ello. El entregable es el `.docx`. El candidato da el
  visto bueno final y hace la conversión a PDF por su cuenta.

