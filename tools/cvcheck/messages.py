"""Textos del validador en los dos idiomas del sistema.

Cada clave lleva sus dos versiones juntas, para que una traducción que falta se vea
a simple vista. El idioma lo decide el banco (`lang: es|en`), no el texto analizado.
"""

MESSAGES = {
    # --- Informe --------------------------------------------------------------
    "title": {"es": "# Validación del CV", "en": "# CV validation"},
    "bank": {"es": "Banco", "en": "Evidence bank"},
    "intro": {"es": "Este validador comprueba lo automatizable. No corrige nada. La decisión es del candidato.",
              "en": "This validator checks what can be automated. It fixes nothing. The decision is the candidate's."},
    "blockers": {"es": "Bloqueantes", "en": "Blockers"},
    "blockers_intro": {"es": "No enviar hasta resolverlos.", "en": "Do not send until they are resolved."},
    "blockers_none": {"es": "Ninguno detectado por comprobación automática.",
                      "en": "None detected by automated checks."},
    "warnings": {"es": "Avisos", "en": "Warnings"},
    "warnings_intro": {"es": "No bloquean, pero hay que mirarlos uno a uno.",
                       "en": "They do not block, but each one needs a look."},
    "none": {"es": "Ninguno.", "en": "None."},
    "data": {"es": "Datos a revisar", "en": "Data to review"},
    "manual": {"es": "Verificación manual pendiente", "en": "Pending manual check"},
    "manual_intro": {"es": "Esta es obligatoria en la skill y este validador NO la cubre.",
                     "en": "The skill makes this one mandatory and this validator does NOT cover it."},
    "manual_parse": {"es": "1. Prueba de parseo ATS (orden de lectura real):",
                     "en": "1. ATS parsing test (actual reading order):"},
    "pandoc_ok": {"es": "pandoc disponible.", "en": "pandoc available."},
    "pandoc_missing": {"es": "pandoc NO instalado: brew install pandoc",
                       "en": "pandoc NOT installed: brew install pandoc"},
    "written": {"es": "(informe escrito en: {path})", "en": "(report written to: {path})"},

    # --- Errores de uso ---------------------------------------------------------
    "cli_desc": {"es": "Validador post-creación del CV.", "en": "Post-build CV validator."},
    "err_no_docx": {"es": "error: no existe el DOCX: {path}", "en": "error: DOCX not found: {path}"},
    "err_no_bank": {"es": "error: no encuentro CARRERA-EVIDENCIAS.md ni CAREER-EVIDENCE.md. Pásalo con --bank.",
                    "en": "error: cannot find CAREER-EVIDENCE.md or CARRERA-EVIDENCIAS.md. Pass it with --bank."},
    "err_ambiguous_bank": {"es": "error: hay dos bancos (CARRERA-EVIDENCIAS.md y CAREER-EVIDENCE.md). Indica cuál con --bank.",
                           "en": "error: there are two banks (CAREER-EVIDENCE.md and CARRERA-EVIDENCIAS.md). Choose one with --bank."},

    # --- Bloqueantes y avisos ---------------------------------------------------
    "dash": {"es": "{name} encontrado: \"{ctx}\"  (regla 7)",
             "en": "{name} found: \"{ctx}\"  (rule 7)"},
    "manual_bullet": {"es": "Carácter '•' escrito a mano. Deben ser bullets de lista (regla ATS).",
                      "en": "Hand-typed '•' character. Use real list bullets (ATS rule)."},
    "signal": {"es": "Posible señal de disponibilidad/urgencia: \"{hit}\"  (regla 6)",
               "en": "Possible availability/urgency signal: \"{hit}\"  (rule 6)"},
    "watch_gap": {"es": "Aparece \"{hit}\": hueco duro. {reason} (sección 10 del banco)",
                  "en": "\"{hit}\" appears: hard gap. {reason} (bank section 10)"},
    "watch_no_evidence": {"es": "Aparece \"{hit}\": no hay evidencia en el banco. {reason} (regla 1)",
                          "en": "\"{hit}\" appears: no evidence in the bank. {reason} (rule 1)"},
    "watch_confirm": {"es": "Aparece \"{hit}\": evidencia sin confirmar. {reason} (regla 4)",
                      "en": "\"{hit}\" appears: unconfirmed evidence. {reason} (rule 4)"},
    "watch_missing": {"es": "El banco no tiene sección 10 (lista de vigilancia): no se comprueban huecos duros ni términos sin evidencia. Ver CARRERA-EVIDENCIAS.example.md.",
                      "en": "The bank has no section 10 (watchlist): hard gaps and terms without evidence are not checked. See CAREER-EVIDENCE.example.md."},
    "watch_bad_row": {"es": "Fila no válida en la sección 10 del banco, se ignora: {row}. Niveles: hueco, sin evidencia, confirmar.",
                      "en": "Invalid row in bank section 10, ignored: {row}. Levels: gap, no evidence, confirm."},
    "missing_heading": {"es": "Falta la sección obligatoria: {h}", "en": "Missing mandatory section: {h}"},
    "heading_order": {"es": "Las secciones no están en el orden ATS esperado.",
                      "en": "Sections are not in the expected ATS order."},
    "sig_missing": {"es": "Falta la firma de cierre obligatoria.", "en": "The mandatory closing signature is missing."},
    "sig_inexact": {"es": "La firma existe pero el texto no es exacto: \"{text}\"",
                    "en": "The signature is there but the text is not exact: \"{text}\""},
    "sig_not_last": {"es": "La firma no es el último elemento del documento.",
                     "en": "The signature is not the last element of the document."},
    "no_email": {"es": "No se ve el email en las primeras líneas. El contacto va en el cuerpo, no en cabecera.",
                 "en": "No email in the first lines. Contact details go in the body, not in a header."},
    "no_linkedin": {"es": "No se ve el LinkedIn en las primeras líneas.",
                    "en": "No LinkedIn in the first lines."},
    "tables": {"es": "El DOCX contiene tablas. Prohibidas: rompen el orden de lectura del ATS.",
               "en": "The DOCX contains tables. Forbidden: they break the ATS reading order."},
    "figure_missing": {"es": "Cifra '{run}' no localizada en el banco (revisar formato o posible invención): \"{snippet}\"",
                       "en": "Figure '{run}' not found in the bank (check format or possible invention): \"{snippet}\""},
    "range": {"es": "Rango '{hit}': verificar que no funde métricas de roles distintos (ej. 45% de un rol y 50% de otro).",
              "en": "Range '{hit}': check it does not merge metrics from different roles (e.g. 45% from one role and 50% from another)."},
    "unknown_company": {"es": "Empresa no reconocida en el banco (regla 9): \"{company}\"",
                        "en": "Company not found in the bank (rule 9): \"{company}\""},
    "es_variant_block": {"es": "\"{hit}\": variante latinoamericana. En español de España: {equiv}. (regla 8)",
                         "en": "\"{hit}\": Latin American Spanish. Spain Spanish: {equiv}. (rule 8)"},
    "es_variant_warn": {"es": "\"{hit}\": posible variante latinoamericana. En español de España suele ser: {equiv}. Revisar. (regla 8)",
                        "en": "\"{hit}\": possibly Latin American Spanish. In Spain it is usually: {equiv}. Check. (rule 8)"},
    "en_variant_mix": {"es": "Mezcla inglés UK y US: \"{us}\" (US) y \"{uk}\" (UK). Usa una sola variante por documento. (regla 8)",
                       "en": "Mixes UK and US English: \"{us}\" (US) and \"{uk}\" (UK). Use one variant per document. (rule 8)"},

    # --- Datos a revisar ----------------------------------------------------------
    "d_reading": {"es": "Orden de lectura (primeras 14 líneas, tal como lo ve un ATS)",
                  "en": "Reading order (first 14 lines, as an ATS sees it)"},
    "d_jobs": {"es": "Bloques de experiencia (empresa | ciudad | fechas)",
               "en": "Experience blocks (company | city | dates)"},
    "d_job_unknown": {"es": "REVISAR: empresa no reconocida en sección 2",
                      "en": "CHECK: company not found in section 2"},
    "d_skills": {"es": "Términos en CORE SKILLS ({n}): cada uno necesita una evidencia (regla 5)",
                 "en": "CORE SKILLS terms ({n}): each one needs evidence (rule 5)"},
    "d_figures": {"es": "Cifras detectadas en la prosa del CV ({n})", "en": "Figures found in the CV prose ({n})"},
    "d_in_bank": {"es": "en banco", "en": "in bank"},
    "d_not_found": {"es": "NO LOCALIZADA", "en": "NOT FOUND"},
    "d_volume": {"es": "Volumen del documento (indicio de longitud)", "en": "Document volume (length hint)"},
    "d_vol_paras": {"es": "Párrafos con texto: {n}", "en": "Paragraphs with text: {n}"},
    "d_vol_chars": {"es": "Caracteres totales: {n}", "en": "Total characters: {n}"},
    "d_vol_ref": {"es": "Referencia: un CV de 2 páginas de este sistema ronda los 6500-7800 caracteres.",
                  "en": "Reference: a 2-page CV from this system is around 6500-7800 characters."},
    "d_vol_hint": {"es": "Es un indicio de longitud por conteo de caracteres, no un veredicto.",
                   "en": "It is a length hint from a character count, not a verdict."},
    "d_vol_high": {"es": "AVISO: volumen alto. Riesgo de desbordar a una tercera página.",
                   "en": "WARNING: high volume. Risk of spilling onto a third page."},
    "d_widows": {"es": "Líneas viudas (ahorro de espacio potencial, INDICIO)",
                 "en": "Widow lines (potential space saving, HINT)"},
    "d_widows_intro": {"es": ["Estimación por ancho medio de carácter (Arial 9.5pt), no un veredicto:",
                              "el render visual manda. Cada palabra colgando ocupa una línea entera;",
                              "recortar ~esa longitud de la misma línea la sube y ahorra una línea."],
                       "en": ["Estimate from average character width (Arial 9.5pt), not a verdict:",
                              "the visual render rules. Each dangling word takes a whole line;",
                              "trimming ~that length from the same paragraph pulls it up and saves a line."]},
    "d_widow": {"es": "- cuelga \"{last}\" (~{n} car. a recortar, {lines} líneas): \"{head}\"",
                "en": "- \"{last}\" dangles (~{n} chars to trim, {lines} lines): \"{head}\""},
    "d_no_messages": {"es": ["No encontrado junto al DOCX ({path}).",
                             "Cuando exista, este validador le aplica guiones, señales, lista de vigilancia,",
                             "cifras y variante de idioma (regla 8)."],
                      "en": ["Not found next to the DOCX ({path}).",
                             "Once it exists, this validator checks it for dashes, signals, the watchlist,",
                             "figures and language variant (rule 8)."]},
}

# Los códigos de cada hallazgo, traducidos para el informe.
CODES = {
    "GUION-LARGO": "LONG-DASH",
    "BULLET-MANUAL": "MANUAL-BULLET",
    "SENAL-PROHIBIDA": "FORBIDDEN-SIGNAL",
    "HUECO-DURO": "HARD-GAP",
    "SIN-EVIDENCIA": "NO-EVIDENCE",
    "EVIDENCIA-C": "UNCONFIRMED-EVIDENCE",
    "VIGILANCIA": "WATCHLIST",
    "ESTRUCTURA": "STRUCTURE",
    "FIRMA": "SIGNATURE",
    "CONTACTO": "CONTACT",
    "TABLA": "TABLE",
    "CIFRA-NO-LOCALIZADA": "FIGURE-NOT-FOUND",
    "RANGO-METRICA": "METRIC-RANGE",
    "EMPRESA": "COMPANY",
    "ESPANOL-LATAM": "SPANISH-VARIANT",
    "VARIANTE-INGLES": "ENGLISH-VARIANT",
}


def translator(lang):
    """Devuelve t(clave, **params) para el idioma dado."""
    def t(key, **kw):
        msg = MESSAGES[key][lang]
        if isinstance(msg, list):
            return [m.format(**kw) for m in msg]
        return msg.format(**kw) if kw else msg
    return t


def code(c, lang):
    return c if lang == "es" else CODES.get(c, c)
