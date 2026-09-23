#!/usr/bin/env python3
"""Validador post-creacion del CV.

Lee el DOCX final y el banco de evidencias (CARRERA-EVIDENCIAS.md o CAREER-EVIDENCE.md),
y produce el dossier de revisión que hay que mirar ANTES de enviar el CV al recruiter.
El informe sale en el idioma del banco (`lang: es|en` en su cabecera).

Principios:
  - No inventa ni corrige nada. Solo comprueba y reporta. La decisión es del candidato.
  - El banco de evidencias manda. Toda comprobación sale de sus reglas (sección 7),
    su cronología (sección 2), su lista de vigilancia (sección 10) y de la estructura
    ATS que fija la skill (cv-a-medida / cv-tailoring). Nada de una carrera concreta
    vive en este código.
  - Sin dependencias externas: solo la librería estándar de Python 3. Un .docx es
    un zip con word/document.xml dentro, así que no hace falta pandoc para leerlo.

Uso:
    python3 tools/validate-cv.py candidaturas/AAAA-MM-empresa/CV-Nombre-Apellidos.docx
    python3 tools/validate-cv.py <docx> --bank CARRERA-EVIDENCIAS.md --out <ruta.md> --lang es

Salida:
  - Informe legible por stdout, agrupado en BLOQUEANTES, AVISOS y DATOS A REVISAR.
  - Un fichero VALIDACION.md (o VALIDATION.md en inglés) junto al DOCX, o donde diga --out.
  - Código de salida != 0 si hay algún BLOQUEANTE.
"""

import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

from cvcheck import bank, rules_en, rules_es
from cvcheck.messages import code, translator

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# --- Estructura ATS obligatoria (skill cv-a-medida, fase 3.3) ---
REQUIRED_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "CORE SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "EDUCATION AND LANGUAGES",
]
OPTIONAL_HEADINGS = ["SELECTED PROJECT"]  # solo arquetipos A y B

SIGNATURE = (
    "No fancy design here, and that's on purpose: this CV is ATS-optimized "
    "so a machine reads it as well as you do."
)

# --- Regla 7: guiones largos prohibidos (em-dash, en-dash, figure/horizontal bar) ---
FORBIDDEN_DASHES = {"—": "em-dash", "–": "en-dash",
                    "―": "horizontal bar", "‒": "figure dash"}

# --- Regla 6: nada de disponibilidad ni urgencia ---
# Los patrones viven en rules_es.py y rules_en.py. Se aplican los dos siempre: cuenta
# el idioma del texto, no el del sistema.
SIGNAL_PATTERNS = rules_en.SIGNAL_PATTERNS + rules_es.SIGNAL_PATTERNS

# Huecos duros, términos sin evidencia y evidencias sin confirmar dependen de cada
# carrera: no están aquí, se leen de la sección 10 del banco (ver cvcheck/bank.py).

# --- Estimación de líneas viudas (una sola palabra colgando al final de un párrafo) ---
# Una palabra sola en la última línea ocupa una línea entera de papel. En un CV de
# dos páginas ajustadas eso es caro: recortar esa palabra sube el texto y ahorra una
# línea. Aqui se ESTIMA el ajuste de línea por el ancho medio de glifo, porque Arial
# es proporcional y no hay render. Es un INDICIO calibrado con los CV de este sistema:
# el cuerpo (9.5pt) envuelve alrededor de 112 caracteres por línea a ancho completo.
# El render visual siempre manda; esto solo señala dónde mirar.
AVG_GLYPH_DXA = 89          # ~4.45pt por carácter a 9.5pt Arial (1 pt = 20 DXA).
                            # Calibrado con ground-truth: a ancho completo el cuerpo
                            # envuelve a ~114 car./línea (10146 / 89).
BULLET_CAP_PENALTY = 6      # un bullet sangrado cabe ~6 car. menos por línea
WIDOW_MAX_CHARS = 18        # última línea de <= 18 car. = cola corta que desperdicia línea
DEFAULT_USABLE_DXA = 10146  # A4 con márgenes laterales de 880: 11906 - 880 - 880


# ----------------------------------------------------------------------------
# Lectura del DOCX
# ----------------------------------------------------------------------------
def read_docx_paragraphs(path):
    """Devuelve la lista de párrafos en orden de documento (orden de lectura ATS)."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter(W + "p"):
        parts = []
        for node in p.iter():
            if node.tag == W + "t" and node.text:
                parts.append(node.text)
            elif node.tag == W + "tab":
                parts.append("\t")
        paras.append("".join(parts))
    return paras


def has_docx_tables(path):
    """Regla ATS: cero tablas. Detecta w:tbl en el documento."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    return "<w:tbl>" in xml or "<w:tbl " in xml


def read_docx_layout(path):
    """Como read_docx_paragraphs pero conserva si cada párrafo es un bullet.
    Necesario para estimar el ajuste de línea: un bullet tiene sangría y envuelve
    a menos caracteres por línea que un párrafo a ancho completo."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    items = []
    for p in root.iter(W + "p"):
        parts = []
        for node in p.iter():
            if node.tag == W + "t" and node.text:
                parts.append(node.text)
            elif node.tag == W + "tab":
                parts.append("\t")
        is_bullet = p.find(".//" + W + "numPr") is not None
        items.append({"text": "".join(parts), "bullet": is_bullet})
    return items


def usable_width_dxa(path):
    """Ancho útil de la caja de texto: ancho de página menos márgenes laterales.
    Se lee del sectPr para que la estimación se adapte si cambian los márgenes."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml")
        sect = next(ET.fromstring(xml).iter(W + "sectPr"), None)
        if sect is None:
            return DEFAULT_USABLE_DXA
        pgsz = sect.find(W + "pgSz")
        pgmar = sect.find(W + "pgMar")
        width = int(pgsz.get(W + "w"))
        left = int(pgmar.get(W + "left"))
        right = int(pgmar.get(W + "right"))
        return max(1, width - left - right)
    except Exception:
        return DEFAULT_USABLE_DXA


def _wrap_words(text, cap):
    """Ajuste de línea codicioso por conteo de caracteres, sin partir palabras.
    Devuelve la lista de líneas resultante. cap = caracteres por línea estimados."""
    lines, cur = [], ""
    for w in text.split():
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= cap:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def widow_candidates(docx_path):
    """Párrafos de prosa cuya última línea sería una sola palabra colgando.
    Devuelve (texto, ultima_palabra, num_lineas). Estimación, no veredicto."""
    usable = usable_width_dxa(docx_path)
    cap_full = max(20, usable // AVG_GLYPH_DXA)
    cap_bullet = max(20, cap_full - BULLET_CAP_PENALTY)
    heads = set(REQUIRED_HEADINGS + OPTIONAL_HEADINGS)
    out = []
    for it in read_docx_layout(docx_path):
        text = it["text"].strip()
        if not text or is_meta_line(text) or text.upper() in heads:
            continue
        cap = cap_bullet if it["bullet"] else cap_full
        lines = _wrap_words(text, cap)
        # Cola corta al final de un párrafo de varias líneas: desperdicia una línea.
        if len(lines) >= 2 and len(lines[-1]) <= WIDOW_MAX_CHARS:
            out.append((text, lines[-1], len(lines)))
    return out


# ----------------------------------------------------------------------------
# Utilidades numéricas: comparar cifras entre CV y banco ignorando el formato
# ("99.95%" del CV == "99,95%" del banco; "$1M" == "1M$"; "400,000" == "400.000")
# ----------------------------------------------------------------------------
def digit_runs(text):
    """Conjunto de cifras normalizadas, de forma que el mismo valor coincida
    aunque el formato difiera entre el CV (inglés) y el banco (español):
        '99.95%'  -> '9995'      '99,95%' -> '9995'
        '400K'    -> '400000'    '400.000' -> '400000'
        '$1M'     -> '1000000'   '1M$'     -> '1000000'
        '1.5M'    -> '1500000'   '1,5M'    -> '1500000'
    El sufijo K/M solo cuenta si está pegado al número (no '400 Kubernetes')."""
    runs = set()
    for m in re.finditer(r"(\d[\d.,]*)([KkMm])?(?![A-Za-z])", text):
        num = m.group(1).rstrip(".,")
        suffix = m.group(2)
        digits = re.sub(r"[.,\s]", "", num)
        if not digits:
            continue
        if suffix:
            mult = 1000 if suffix in "Kk" else 1000000
            try:
                runs.add(str(int(digits) * mult))
            except ValueError:
                runs.add(digits)
        else:
            runs.add(digits)
    return runs


def is_year(run):
    return len(run) == 4 and (run.startswith("19") or run.startswith("20"))


def bank_numbers(bank_text):
    """Cifras del banco para comparar, quitando ruido que NO son métricas:
    identificadores EV-nn y R-nn, y el teléfono. Si no se limpian, un dato
    inventado como '73%' colaria por coincidir con el id EV-73."""
    t = re.sub(r"\bEV-\d+", " ", bank_text)
    t = re.sub(r"\bR-\d+", " ", t)
    t = re.sub(r"\+?\d[\d ]{6,}\d", " ", t)   # números de teléfono
    return digit_runs(t)


# ----------------------------------------------------------------------------
# Comprobaciones
# ----------------------------------------------------------------------------
class Report:
    def __init__(self, lang):
        self.lang = lang
        self.t = translator(lang)
        self.blockers = []   # (código, mensaje)
        self.warnings = []   # (código, mensaje)
        self.data = []       # (título, [líneas])

    def block(self, code, msg):
        if (code, msg) not in self.blockers:
            self.blockers.append((code, msg))

    def warn(self, code, msg):
        if (code, msg) not in self.warnings:
            self.warnings.append((code, msg))

    def datum(self, title, lines):
        self.data.append((title, lines))


def find_all(patterns, text, flags=re.IGNORECASE):
    """Devuelve la lista de (patrón, coincidencia) encontradas."""
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags):
            hits.append((pat, m.group(0)))
    return hits


def is_meta_line(p):
    """Contacto y línea de empresa/fechas usan '  |  '. No se analizan como prosa."""
    return "  |  " in p or " | " in p


def check_language_variant(text, rep, prefix):
    """Regla 8, según el idioma del texto (no el del sistema):
    - español: español de España, nada de variante latinoamericana;
    - inglés: una sola variante (UK o US) en el mismo texto.
    Cada bloque de marcadores es de su idioma, así que no dispara sobre el otro."""
    t = rep.t
    for pat, equiv in rules_es.VARIANT_BLOCK.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            rep.block("ESPANOL-LATAM", prefix + t("es_variant_block", hit=m.group(0), equiv=equiv))
    for pat, equiv in rules_es.VARIANT_WARN.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            rep.warn("ESPANOL-LATAM", prefix + t("es_variant_warn", hit=m.group(0).strip(), equiv=equiv))
    # Inglés: basta una forma US y una UK en el mismo texto, aunque sean palabras distintas.
    first_us = first_uk = None
    for us, uk, suffix in rules_en.SPELLING_PAIRS:
        first_us = first_us or re.search(r"\b%s%s\b" % (us, suffix), text, re.IGNORECASE)
        first_uk = first_uk or re.search(r"\b%s%s\b" % (uk, suffix), text, re.IGNORECASE)
    if first_us and first_uk:
        rep.warn("VARIANTE-INGLES", prefix + t("en_variant_mix", us=first_us.group(0), uk=first_uk.group(0)))


def check_watchlist(text, watch, rep, prefix):
    """Sección 10 del banco: huecos duros y términos sin evidencia bloquean,
    evidencias sin confirmar avisan."""
    t = rep.t
    for level, pats, _term, reason in watch or []:
        for rx in pats:
            m = rx.search(text)
            if not m:
                continue
            if level == "gap":
                rep.block("HUECO-DURO", prefix + t("watch_gap", hit=m.group(0), reason=reason))
            elif level == "no-evidence":
                rep.block("SIN-EVIDENCIA", prefix + t("watch_no_evidence", hit=m.group(0), reason=reason))
            else:
                rep.warn("EVIDENCIA-C", prefix + t("watch_confirm", hit=m.group(0), reason=reason))


def check_prose(text, watch, rep, prefix=""):
    """Reglas de texto comunes al CV y a los mensajes: señales de disponibilidad
    (regla 6), lista de vigilancia (sección 10) y variante de idioma (regla 8)."""
    for pat, hit in find_all(SIGNAL_PATTERNS, text):
        rep.block("SENAL-PROHIBIDA", prefix + rep.t("signal", hit=hit))
    check_watchlist(text, watch, rep, prefix)
    check_language_variant(text, rep, prefix)


def run_message_checks(msg_text, label, bank_text, watch, rep):
    """Aplica a la carta y al mensaje de LinkedIn las mismas reglas de texto que al CV:
    guiones largos, señales de disponibilidad, lista de vigilancia, variante de idioma
    y cifras contra el banco. Suele ser el fichero donde vive el texto en español."""
    t = rep.t
    prefix = f"({label}) "

    # Guiones largos (regla 7)
    for ch, name in FORBIDDEN_DASHES.items():
        if ch in msg_text:
            idx = msg_text.find(ch)
            ctx = msg_text[max(0, idx - 40): idx + 40].replace("\n", " ").strip()
            rep.block("GUION-LARGO", prefix + t("dash", name=name, ctx="..." + ctx + "..."))

    check_prose(msg_text, watch, rep, prefix)

    # Cifras que no aparecen en el banco (reglas 1 y 2). Se saltan los encabezados
    # markdown, donde un '(200-300 palabras)' es una instrucción, no un dato.
    bank_runs = bank_numbers(bank_text)
    for line in msg_text.splitlines():
        if line.strip().startswith("#"):
            continue
        for run in digit_runs(line):
            if is_year(run) or len(run) <= 1:
                continue
            if run not in bank_runs:
                snippet = line.strip()
                snippet = (snippet[:90] + "...") if len(snippet) > 90 else snippet
                rep.warn("CIFRA-NO-LOCALIZADA", prefix + t("figure_missing", run=run, snippet=snippet))


def run_checks(paras, bank_text, docx_path, watch, rep):
    t = rep.t
    non_empty = [p for p in paras if p.strip()]
    full_text = "\n".join(paras)
    bank_runs = bank_numbers(bank_text)
    companies = bank.known_companies(bank_text)

    # 1. Guiones largos (regla 7) --------------------------------------------
    for p in paras:
        for ch, name in FORBIDDEN_DASHES.items():
            if ch in p:
                rep.block("GUION-LARGO", t("dash", name=name, ctx=p.strip()[:80]))

    # Bullet manual con carácter '•' en vez de lista real
    if any("•" in p for p in paras):
        rep.warn("BULLET-MANUAL", t("manual_bullet"))

    # 2 y 3. Señales (regla 6), lista de vigilancia (sección 10), variante (regla 8)
    check_prose(full_text, watch, rep)

    # 4. Estructura ATS obligatoria ------------------------------------------
    upper_paras = [p.strip().upper() for p in paras]
    positions = {}
    for h in REQUIRED_HEADINGS + OPTIONAL_HEADINGS:
        positions[h] = next((i for i, up in enumerate(upper_paras) if up == h), None)

    for h in REQUIRED_HEADINGS:
        if positions[h] is None:
            rep.block("ESTRUCTURA", t("missing_heading", h=h))

    present_required = [h for h in REQUIRED_HEADINGS if positions[h] is not None]
    order_ok = all(
        positions[present_required[i]] < positions[present_required[i + 1]]
        for i in range(len(present_required) - 1)
    )
    if len(present_required) == len(REQUIRED_HEADINGS) and not order_ok:
        rep.block("ESTRUCTURA", t("heading_order"))

    # 5. Firma de cierre exacta y en última posición útil ---------------------
    sig_idx = next((i for i, p in enumerate(paras) if p.strip() == SIGNATURE), None)
    if sig_idx is None:
        soft = next((i for i, p in enumerate(paras) if "ATS-optimized" in p), None)
        if soft is None:
            rep.block("FIRMA", t("sig_missing"))
        else:
            rep.warn("FIRMA", t("sig_inexact", text=paras[soft].strip()))
    else:
        last_text_idx = max(i for i, p in enumerate(paras) if p.strip())
        if sig_idx != last_text_idx:
            rep.warn("FIRMA", t("sig_not_last"))

    # 6. Contacto en el cuerpo, en las primeras líneas ------------------------
    head = " ".join(non_empty[:6])
    if "@" not in head:
        rep.warn("CONTACTO", t("no_email"))
    if "linkedin" not in head.lower():
        rep.warn("CONTACTO", t("no_linkedin"))

    # 7. Tablas (rompen el parseo lineal) ------------------------------------
    if has_docx_tables(docx_path):
        rep.block("TABLA", t("tables"))

    # 8. Cifras del CV que no aparecen en el banco (reglas 1 y 2) -------------
    #    Se analiza solo la prosa (resumen, skills, bullets), no el contacto ni
    #    las líneas de empresa/fechas. Se ignoran los años.
    seen = set()
    for p in paras:
        if is_meta_line(p) or not p.strip():
            continue
        for run in digit_runs(p):
            if is_year(run) or len(run) <= 1:
                continue  # un solo dígito es demasiado ambiguo para afirmar nada
            if run not in bank_runs:
                ctx = p.strip()
                snippet = (ctx[:90] + "...") if len(ctx) > 90 else ctx
                if (run, snippet) not in seen:
                    seen.add((run, snippet))
                    rep.warn("CIFRA-NO-LOCALIZADA", t("figure_missing", run=run, snippet=snippet))

    # 9. Rangos de métrica que podrían mezclar dos roles (reglas 2 y 3) -------
    for p in paras:
        if is_meta_line(p):
            continue
        for m in re.finditer(r"\d+\s*[-–]\s*\d+\s*%", p):
            rep.warn("RANGO-METRICA", t("range", hit=m.group(0).strip()))

    # ---- DATOS A REVISAR (dossier para el humano) --------------------------

    # a) Orden de lectura tal como lo ve el ATS
    reading = [f"{i+1:>2}. {p.strip()}" for i, p in enumerate(non_empty[:14])]
    rep.datum(t("d_reading"), reading)

    # b) Bloques de experiencia: empresa, fechas y verificación contra sección 2
    job_lines = []
    for p in paras:
        if "  |  " in p and re.search(r"\b(19|20)\d\d\b|Present", p):
            company = p.split("  |  ")[0].strip()
            if any(k.lower() in p.lower() for k in ["linkedin", "@", "github"]):
                continue  # es la línea de contacto, no un job
            known = any(c.lower() in company.lower() or company.lower() in c.lower()
                        for c in companies)
            mark = "OK" if known else t("d_job_unknown")
            job_lines.append(f"[{mark}] {p.strip()}")
            if not known:
                rep.block("EMPRESA", t("unknown_company", company=company))
    if job_lines:
        rep.datum(t("d_jobs"), job_lines)

    # c) Términos de CORE SKILLS: cada uno necesita evidencia (regla 5)
    if positions["CORE SKILLS"] is not None and positions["PROFESSIONAL EXPERIENCE"] is not None:
        start, end = positions["CORE SKILLS"], positions["PROFESSIONAL EXPERIENCE"]
        terms = []
        for p in paras[start + 1:end]:
            rhs = p.split(":", 1)[1] if ":" in p else p
            terms.extend(x.strip() for x in rhs.split(",") if x.strip())
        if terms:
            rep.datum(t("d_skills", n=len(terms)), ["- " + x for x in terms])

    # d) Todas las cifras del CV localizadas en el banco (traza de métricas)
    located = []
    for p in paras:
        if is_meta_line(p) or not p.strip():
            continue
        for run in sorted(digit_runs(p)):
            if is_year(run) or len(run) <= 1:
                continue
            status = t("d_in_bank") if run in bank_runs else t("d_not_found")
            located.append(f"{run:>8}  [{status}]")
    if located:
        uniq = sorted(set(located))
        rep.datum(t("d_figures", n=len(uniq)), uniq)

    # e) Longitud aproximada del documento por conteo de caracteres
    total_chars = sum(len(p) for p in paras)
    vol = [t("d_vol_paras", n=len(non_empty)), t("d_vol_chars", n=total_chars),
           t("d_vol_ref"), t("d_vol_hint")]
    if total_chars > 8500:
        vol.append(t("d_vol_high"))
    rep.datum(t("d_volume"), vol)

    # f) Líneas viudas: una sola palabra colgando al final de un párrafo -------
    #    Cada una desperdicia una línea entera. Recortarla es el ahorro de
    #    espacio más barato para no desbordar de dos páginas.
    widows = widow_candidates(docx_path)
    if widows:
        wl = t("d_widows_intro") + [""]
        for text, last, n in widows:
            head = (text[:66] + "...") if len(text) > 66 else text
            wl.append(t("d_widow", last=last, n=len(last) + 1, lines=n, head=head))
        rep.datum(t("d_widows"), wl)

    return rep


# ----------------------------------------------------------------------------
# Salida
# ----------------------------------------------------------------------------
def render_report(rep, docx_path, bank_path):
    t = rep.t
    lines = [t("title"), "", f"- DOCX: `{docx_path}`", f"- {t('bank')}: `{bank_path}`", "",
             t("intro"), ""]

    lines += [f"## {t('blockers')} ({len(rep.blockers)})", ""]
    if rep.blockers:
        lines += [t("blockers_intro"), ""]
        lines += [f"- **[{code(c, rep.lang)}]** {msg}" for c, msg in rep.blockers]
    else:
        lines.append(t("blockers_none"))
    lines.append("")

    lines += [f"## {t('warnings')} ({len(rep.warnings)})", ""]
    if rep.warnings:
        lines += [t("warnings_intro"), ""]
        lines += [f"- **[{code(c, rep.lang)}]** {msg}" for c, msg in rep.warnings]
    else:
        lines.append(t("none"))
    lines.append("")

    lines += [f"## {t('data')}", ""]
    for title, block in rep.data:
        lines += [f"### {title}", ""] + list(block) + [""]

    lines += [f"## {t('manual')}", ""] + manual_checks_block(docx_path, t) + [""]
    return "\n".join(lines)


def manual_checks_block(docx_path, t):
    """La prueba de parseo ATS de la skill, que necesita pandoc. Se informa si falta."""
    import shutil
    have_pandoc = shutil.which("pandoc")
    return [
        t("manual_intro"), "",
        t("manual_parse"), "",
        "   ```",
        f"   pandoc -t plain --wrap=none \"{docx_path}\"",
        "   ```",
        "   " + (t("pandoc_ok") if have_pandoc else t("pandoc_missing")),
    ]


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Validador post-creación del CV / Post-build CV validator.")
    ap.add_argument("docx", help="CV en DOCX / CV as DOCX.")
    ap.add_argument("--bank", help="CARRERA-EVIDENCIAS.md o/or CAREER-EVIDENCE.md.")
    ap.add_argument("--out", help="Ruta del informe / Report path. Default: VALIDACION.md | VALIDATION.md.")
    ap.add_argument("--lang", choices=["es", "en"],
                    help="Idioma del informe / Report language. Default: el del banco / the bank's.")
    args = ap.parse_args()

    # Localizar el banco: --bank, o subiendo desde el DOCX hasta encontrarlo.
    docx_dir = os.path.dirname(os.path.abspath(args.docx))
    bank_path, err = args.bank, None
    if not bank_path:
        bank_path, err = bank.find_bank(docx_dir)

    if not os.path.isfile(args.docx):
        print(translator(args.lang or "es")("err_no_docx", path=args.docx), file=sys.stderr)
        return 2
    if not bank_path or not os.path.isfile(bank_path):
        key = "err_ambiguous_bank" if err == "ambiguous" else "err_no_bank"
        print(translator(args.lang or "es")(key), file=sys.stderr)
        return 2

    with open(bank_path, encoding="utf-8") as f:
        bank_text = f.read()
    lang = args.lang or bank.bank_lang(bank_text, bank_path)
    rep = Report(lang)
    t = rep.t

    watch, watch_errors = bank.watchlist(bank_text)
    if watch is None:
        rep.warn("VIGILANCIA", t("watch_missing"))
    for row in watch_errors:
        rep.warn("VIGILANCIA", t("watch_bad_row", row=row))

    paras = read_docx_paragraphs(args.docx)
    run_checks(paras, bank_text, args.docx, watch, rep)

    # Los mensajes viven junto al DOCX (Mensajes.md o Messages.md). Reciben las
    # mismas reglas de texto. Si no están aún, se nota.
    msg_paths = [os.path.join(docx_dir, bank.FILENAMES[l]["messages"]) for l in ("es", "en")]
    found = [p for p in msg_paths if os.path.isfile(p)]
    for msg_path in found:
        with open(msg_path, encoding="utf-8") as f:
            run_message_checks(f.read(), os.path.basename(msg_path), bank_text, watch, rep)
    if not found:
        expected = os.path.join(docx_dir, bank.FILENAMES[lang]["messages"])
        rep.datum(bank.FILENAMES[lang]["messages"], t("d_no_messages", path=expected))

    report_md = render_report(rep, args.docx, bank_path)

    out_path = args.out or os.path.join(docx_dir, bank.FILENAMES[lang]["report"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(report_md)
    print("\n" + t("written", path=out_path))

    return 1 if rep.blockers else 0


if __name__ == "__main__":
    sys.exit(main())
