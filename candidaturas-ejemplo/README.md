# Candidatura de ejemplo (ficticia)

Esta carpeta muestra la salida del sistema para una oferta inventada, usando el banco
ficticio de Jane Doe (`CARRERA-EVIDENCIAS.example.md`). Sirve para ver el formato de los
entregables sin exponer datos reales. La versión en inglés de este ejemplo está en
`applications-example/`.

`2026-01-northwind-head-of-ai/` contiene los entregables de texto:

- `oferta.md`   la oferta original
- `Encaje.md`   el informe de encaje
- `Mensajes.md` la carta y el mensaje de LinkedIn

En una candidatura real, la carpeta también guarda `cv-content.js` (la fuente del CV) y el CV
en DOCX. Aquí la fuente es la plantilla `tools/cv-content.example.js`, y el DOCX no se versiona
(los `.docx` están en `.gitignore`). Para generarlo, desde la raíz del proyecto:

```bash
CV_CONTENT=tools/cv-content.example.js node tools/build-cv.js candidaturas-ejemplo/2026-01-northwind-head-of-ai/CV-Jane-Doe.docx
```

Tus candidaturas reales van en `candidaturas/`, que no se versiona.
