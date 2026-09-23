# Example application (fictional)

This folder shows the system's output for an invented job posting, using Jane Doe's
fictional bank (`CAREER-EVIDENCE.example.md`). It shows the format of the deliverables
without exposing real data. The Spanish version of this example is in `candidaturas-ejemplo/`.

`2026-01-northwind-head-of-ai/` holds the text deliverables:

- `job-posting.md` the original job posting
- `Fit.md`         the fit report
- `Messages.md`    the letter and the LinkedIn message

In a real application, the folder also keeps `cv-content.js` (the CV source) and the DOCX
CV. Here the source is the `tools/cv-content.example.js` template, and the DOCX is not versioned
(`.docx` files are in `.gitignore`). To generate it, from the project root:

```bash
CV_CONTENT=tools/cv-content.example.js node tools/build-cv.js applications-example/2026-01-northwind-head-of-ai/CV-Jane-Doe.docx
```

Your real applications go in `applications/`, which is not versioned.
