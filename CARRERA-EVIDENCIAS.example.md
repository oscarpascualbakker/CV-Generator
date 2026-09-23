---
lang: es
---

# Banco de evidencias de carrera - Jane Doe (EJEMPLO FICTICIO)

> EJEMPLO. Ninguna persona, empresa, métrica ni fecha de este fichero es real.
> Sirve para demostrar el método. Copia este fichero a `CARRERA-EVIDENCIAS.md` y
> sustituye su contenido por el tuyo. El real NO se versiona (ver .gitignore).
> La línea `lang: es` de la cabecera fija el idioma del sistema (skill e informes).
> Para usarlo en inglés, parte de `CAREER-EVIDENCE.example.md`.
>
> Fuente única de verdad. Ningún CV, carta o mensaje puede afirmar nada que no esté aquí.
> Si algo no está en este fichero, no existe. Se pregunta, se añade aquí, y solo entonces se usa.

---

## 0. Cómo se usa este fichero

Cada evidencia tiene un identificador (`EV-nn`). El CV adaptado se construye
seleccionando evidencias por identificador, no redactando de cero. La adaptación
consiste en **elegir, ordenar y reformular** evidencias existentes, nunca en crear
hechos nuevos.

Nivel de verificación:

- **V** (verificada): está en el CV actual o el candidato la ha confirmado explícitamente.
- **C** (confirmar): es real pero nunca se ha escrito con estas palabras o la métrica no está cerrada. Requiere una pregunta antes de usarse.
- **X** (prohibida): afirmación que NO puede hacerse. Ver sección 7.

Fuerza:

- **A**: métrica dura, cifra de negocio, resultado atribuible. Sirve de titular.
- **B**: resultado sólido pero de proceso o cualitativo.
- **C**: contexto de apoyo. Rellena, no vende.

---

## 1. Identidad

| Campo | Valor |
|---|---|
| Nombre | Jane Doe |
| Ubicación | London (United Kingdom) |
| Teléfono | +44 20 7946 0100 |
| Email | jane.doe@example.com |
| LinkedIn | linkedin.com/in/jane-doe-example |
| GitHub | github.com/jane-doe-example |
| Movilidad | London o 100% remoto. Viajes puntuales sí. Trabajo fraccional no. |
| Idiomas | Inglés (nativo), Español (full professional), Francés (nativo) |

**Formación**

- Executive MBA, Thames Business School, London
- BSc Computer Science, University of Bristol
- Postgrado en e-Commerce y Marketing Digital, Thames Business School, London

**Trayectoria en una línea**: 15+ años liderando ingeniería en e-commerce, healthtech y SaaS,
incluyendo un rol de CTO y 17 años como fundadora. Los últimos 3 años centrados en llevar IA
a producción y en rediseñar cómo trabaja la ingeniería con IA.

---

## 2. Cronología de roles

| ID | Rol | Empresa | Periodo | Sector | Alcance |
|---|---|---|---|---|---|
| R-01 | Senior Engineering Manager | Lumina Labs, London | sep 2025 - actualidad | SaaS / research platform | 1 equipo, adopción de IA en todo el SDLC |
| R-02 | Senior Engineering Manager | Meridian Health, London | sep 2023 - sep 2025 | Healthtech / marketplace | 1 equipo, producto de IA en producción a escala global |
| R-03 | Fundadora | Harbor Goods, Bristol | oct 2009 - ago 2026 (desinvertido) | E-commerce B2C/B2B | Negocio completo, P&L propio |
| R-04 | CTO | Corveo, London | nov 2021 - jun 2023 | Healthtech / telemedicina | Organización completa, 8 a 16 ingenieros |
| R-05 | R&D Manager | FreightLink, London | feb 2020 - oct 2021 | Logtech / SaaS | Capacidad de ingeniería y arquitectura |
| R-06 | Head of Development | Dermex, London | feb 2019 - feb 2020 | Farmacéutica / dermocosmética | Equipo de desarrollo |
| R-07 | Head of Development | RideNow, London | sep 2016 - ene 2019 | Movilidad / sharing | Organización de desarrollo |

**Nota de solapamiento**: R-03 (Harbor Goods) es un proyecto propio que convive con los roles
por cuenta ajena. En el CV se sitúa como emprendimiento paralelo, nunca como dedicación exclusiva.

---

## 3. Evidencias

### IA en producción (producto)

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-01 | Sistema de auto-moderación basado en IA que procesa más de 400.000 reseñas al mes | Reducción de 1M GBP anuales en costes globales de moderación | R-02 | V | A |
| EV-03 | Sistemas de IA para atención al cliente y clasificación de correo | Tiempos de respuesta -45%, satisfacción +25% | R-03 | V | A |
| EV-04 | Chatbot conversacional en producción sobre el e-commerce | Conversión +20% | R-03 | V | A |

### IA en ingeniería (modelo operativo)

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-10 | Implantación de Spec-Driven Development alineando producto, diseño e ingeniería antes de escribir código | Cycle time de 4d 2h a 2d 6h (~45%) | R-01 | V | A |
| EV-11 | IA integrada en todo el ciclo de vida: requisitos, specs, implementación, revisión, QA y documentación | Cualitativa | R-01 | V | B |
| EV-13 | Duplicación del output de entrega redefiniendo ownership, priorización y rituales de ejecución | Output x2 | R-01 | V | A |
| EV-14 | Adopción de herramientas de ingeniería asistida por IA reduciendo fricción para los ICs | Mejora de calidad de código y velocidad de revisión | R-02 | V | B |

### Arquitectura de IA y sistemas agénticos

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-20 | Plataforma agéntica autónoma propia de 13 agentes, ejecución diaria autónoma, 3+ meses en producción continua | 13 agentes, cadencia diaria, 3+ meses en producción | Proyecto propio | V | A |
| EV-21 | Trabajo con Model Context Protocol (MCP) como estándar de integración | Cualitativa | R-01 | C | B |
| EV-23 | Evaluación de LLMs, guardrails y criterios de aceptación para salidas no deterministas | Cualitativa | R-01 | V | B |
| EV-25 | Optimización de coste de inferencia y búsqueda de salidas deterministas | Cualitativa | R-02 | V | B |

### Liderazgo y transformación de equipos

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-30 | Conversión de un grupo con bajo rendimiento en un equipo de alto rendimiento | Cualitativa con resultados asociados | R-02 | V | A |
| EV-31 | Engagement del equipo llevado al segundo nivel más alto de la compañía tras la reorganización | eNPS 40 | R-02 | V | A |
| EV-32 | Incremento del engagement cerrando huecos de liderazgo y construyendo cultura de feedback | +40% | R-01 | V | A |
| EV-33 | Reducción sostenida de cycle time con disciplina de WIP y mejor priorización | -50% | R-02 | V | A |
| EV-35 | Mejora de productividad del equipo mediante ownership más claro y mejores prácticas de revisión | +40% | R-07 | V | B |
| EV-36 | Creación de un equipo de ingeniería de alto rendimiento e introducción de prácticas ágiles | Cualitativa | R-06 | V | B |

### Dirección técnica y negocio

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-40 | Escalado de la organización de 8 a 16 ingenieros en backend, frontend, mobile y QA sin frenar la entrega | 2x organización | R-04 | V | A |
| EV-45 | Desinversión del negocio en 2026 tras convertirlo en una operación autosostenida, cerrando 17 años como fundadora | Salida completa | R-03 | V | A |

### Arquitectura, plataforma y fiabilidad

| ID | Evidencia | Métrica | Rol | Ver. | Fuerza |
|---|---|---|---|---|---|
| EV-50 | Arquitectura de la migración de monolito a microservicios sobre Kubernetes | Disponibilidad de 99,2% a 99,95%, escalabilidad 5x | R-04 | V | A |
| EV-51 | Modelo operativo de ingeniería: revisión de código, despliegue, respuesta a incidentes | Defectos en producción -35%, MTTR -40% | R-04 | V | A |
| EV-52 | Propiedad del roadmap de migración de monolito a microservicios | Menos deuda técnica, más velocidad | R-05 | V | B |
| EV-54 | Testing automatizado y rutinas de CI | Defectos de release -25% | R-06 | V | B |
| EV-55 | Mejora de productividad del equipo | +40% | R-07 | V | B |

---

## 4. Mapa de competencias

Índice inverso. La fase de encaje busca aquí antes de buscar en ningún otro sitio.

| Competencia | Evidencias |
|---|---|
| IA en producto / producción | EV-01, EV-03, EV-04, EV-20 |
| IA aplicada al SDLC | EV-10, EV-11, EV-14 |
| Sistemas agénticos y multi-agente | EV-20, EV-21, EV-23 |
| Liderazgo de personas | EV-30, EV-31, EV-32, EV-35, EV-36, EV-40 |
| Turnaround de equipos | EV-30, EV-31, EV-32, EV-35 |
| Escalado de organización | EV-40, EV-36 |
| Arquitectura / plataforma | EV-50, EV-52 |
| Fiabilidad y operación | EV-50, EV-51, EV-54 |
| Métricas de entrega | EV-10, EV-33, EV-13 |
| Emprendimiento y ownership de negocio | EV-45 |

---

## 5. Arquetipos de puesto y posicionamiento

Cada oferta se clasifica en uno de estos arquetipos. El arquetipo fija el titular,
el orden de las secciones y qué evidencias entran primero.

### A. Head of AI / AI Lead (objetivo primario)

- **Titular**: `Head of AI | Production AI Systems & AI-First Engineering | ex-CTO`
- **Apertura**: EV-01, EV-20, EV-10

### B. Plataforma de agentes / AI infrastructure

- **Titular**: `Engineering Leader | AI Agent Platforms in Production | ex-CTO`
- **Apertura**: EV-20, EV-23, luego EV-01

### C. Director / Head of Engineering, VP

- **Titular**: `Engineering Leader | Scaling Teams & AI-First Operating Models | ex-CTO`
- **Apertura**: EV-40, EV-30, EV-13

### D. CTO en startup o scale-up

- **Titular**: `CTO | Engineering, Product Delivery & AI | 15+ years`
- **Apertura**: EV-40, EV-50, luego EV-45

### E. Engineering Manager senior

- **Titular**: `Senior Engineering Manager | Delivery Performance & AI-Assisted Engineering`
- **Apertura**: EV-13, EV-33, EV-32, EV-10

---

## 6. Huecos conocidos y cómo se tratan

Nunca se rellenan inventando. Se reconocen y se compensan con lo adyacente.

| Hueco | Realidad | Adyacencia utilizable | Qué NO se puede decir |
|---|---|---|---|
| GxP, 21 CFR Part 11, validación de sistemas | Sin experiencia | EV-50, EV-51: cultura de auditoría y trazabilidad | Que ha trabajado en entornos GxP o validados |
| Equipos de más de 16 personas | Máximo verificado: 16 | EV-40 (duplicó) | Cifras de organización que no estén en la sección 2 |

**Regla de compensación**: un hueco duro no se menciona en el CV. Se prepara una respuesta
para la entrevista y se registra en el informe de encaje. Cada hueco duro tiene además su
fila en la sección 10, para que el validador lo detecte si se cuela.

---

## 7. Reglas de verdad

Prohibiciones absolutas. Se aplican a CV, carta, mensaje y perfil.

1. **Nada fuera de este banco.** Si una evidencia no tiene ID, no se escribe.
2. **Las métricas no se redondean al alza ni se recombinan.**
3. **No se traslada una evidencia de un rol a otro.** Cada `EV` está anclada a su `R`.
4. **Las evidencias marcadas C se confirman antes de usarse.**
5. **Ninguna tecnología se lista en skills si no hay una evidencia detrás.**
6. **No se menciona disponibilidad ni urgencia.** El tono es de selectividad.
7. **Sin guiones largos (em-dash) en ningún texto.**
8. **Español de España** cuando el documento vaya en español. El CV normalmente va en inglés, con una sola variante (UK o US) en todo el documento.
9. **No se inventan fechas, títulos ni nombres de empresa.** La sección 2 es la única cronología válida.
10. **Cada bullet del CV debe poder defenderse 20 minutos en una entrevista.**

---

## 8. Deuda de este banco

Lo que falta y merece la pena cerrar, por orden de retorno:

1. Cerrar métricas de las evidencias agénticas (EV-20, EV-23) y confirmar EV-21 (MCP).
2. Tamaño de los equipos de R-01, R-02, R-05, R-06, R-07: solo R-04 tiene cifra.
3. Historias STAR para las evidencias de fuerza A más usadas.

---

## 9. Criterios de búsqueda

| Criterio | Valor |
|---|---|
| Salario actual | 95.000 GBP brutos/año |
| Objetivo | 110.000 GBP brutos/año o más. Por debajo de 95.000, descarte probable |
| Si la oferta no publica banda | Incógnita a resolver en el primer contacto con el recruiter, antes de invertir en materiales |
| Consultoría / forward-deployed | No, aunque sea en plantilla. Señales: "the client/customer/account", "forward deployed", "client travel", empresa que vende despliegues a terceros |

---

## 10. Lista de vigilancia del validador

Términos que `tools/validate-cv.py` busca en el CV y en los mensajes. Es lo único de tu
carrera que el validador necesita saber, y vive aquí, no en el código.

- **Término**: texto literal (varios, separados por comas) o una expresión regular entre
  comillas invertidas. Un literal todo en mayúsculas (`MCP`, `A2A`) distingue mayúsculas.
- **Nivel**: `hueco` (hueco duro de la sección 6: bloquea), `sin evidencia` (no hay `EV`
  detrás: bloquea), `confirmar` (evidencia marcada `C`: avisa).

| Término | Nivel | Motivo |
|---|---|---|
| GxP, 21 CFR, Part 11, computerized system validation | hueco | Sin experiencia en entornos GxP o validados (sección 6). |
| MCP, Model Context Protocol | confirmar | EV-21 marcada C. Confirmar qué se ha construido antes de enviar. |
| A2A | sin evidencia | Nunca lo ha usado: no se puede afirmar. |
