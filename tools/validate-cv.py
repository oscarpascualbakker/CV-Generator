#!/usr/bin/env python3
"""Validador post-creacion del CV.

Lee el DOCX final y CARRERA-EVIDENCIAS.md, y produce el dossier de revisión
que hay que mirar ANTES de enviar el CV al recruiter.

Principios:
  - No inventa ni corrige nada. Solo comprueba y reporta. La decisión es del candidato.
  - El banco de evidencias manda. Toda comprobación sale de sus reglas (sección 7),
    sus huecos (sección 6) y de la estructura ATS que fija la skill cv-a-medida.
  - Sin dependencias externas: solo la librería estándar de Python 3. Un .docx es
    un zip con word/document.xml dentro, así que no hace falta pandoc para leerlo.

Uso:
    python3 tools/validate-cv.py candidaturas/AAAA-MM-empresa/CV-Nombre-Apellidos.docx
    python3 tools/validate-cv.py <docx> --bank CARRERA-EVIDENCIAS.md --out <ruta.md>

Salida:
  - Informe legible por stdout, agrupado en BLOQUEANTES, AVISOS y DATOS A REVISAR.
  - Un fichero VALIDACION.md junto al DOCX (o donde diga --out).
  - Código de salida != 0 si hay algún BLOQUEANTE.
"""

import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

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

# --- Regla 6: nada de disponibilidad, urgencia ni ERE ---
# Se buscan señales sobre la disponibilidad del CANDIDATO, no la palabra
# "availability" a secas (que es una métrica técnica legítima: uptime de plataforma).
SIGNAL_PATTERNS = [
    r"\bavailable (immediately|now|to start|for hire|for work|from|on|to join)\b",
    r"\bimmediate availability\b",
    r"\bmy availability\b",
    r"\bimmediate start\b",
    r"\bnotice period\b",
    r"\bopen to work\b",
    r"\bactively (looking|seeking)\b",
    r"\b(seeking|looking for) (a )?new (role|position|opportunity|challenge)\b",
    # Disponibilidad del CANDIDATO, no la "disponibilidad de la plataforma"
    # (uptime), que es una métrica técnica legítima igual que 'availability' en inglés.
    r"\bdisponibilidad\W+(inmediata|total|para incorporar|de incorporaci)",
    r"\bmi disponibilidad\b",
    r"\bdisponible (para|a partir|desde|de inmediato|inmediatamente|ya|en)\b",
    r"\bincorporaci[oó]n inmediata\b",
    r"\bcuanto antes\b",
    r"\burgent(e|emente)\b",          # solo formas en español; 'urgent' en inglés da falsos positivos
]
# ERE se comprueba aparte, sensible a mayúsculas, para no chocar con 'were'/'here'.
ERE_PATTERN = r"\bERE\b"

# NOTA: los tres diccionarios que siguen (HARD_GAP_PATTERNS, C_EVIDENCE_PATTERNS,
# NO_EVIDENCE_PATTERNS) codifican huecos y evidencias sin cerrar concretos de la
# sección 6 del banco. No son datos personales, pero SÍ dependen de cada carrera:
# al adaptar tu banco, revisa estos patrones y sustitúyelos por los tuyos.

# --- Sección 6 del banco: huecos duros que NUNCA pueden aparecer en el CV ---
# "Qué NO se puede decir". Si aparecen, es un bloqueante directo.
HARD_GAP_PATTERNS = {
    r"\bGxP\b": "GxP (hueco duro, regla sección 6)",
    r"\b21\s?CFR\b": "21 CFR Part 11 (hueco duro)",
    r"\bPart\s?11\b": "21 CFR Part 11 (hueco duro)",
    r"\bcomputerized system validation\b": "CSV / validación de sistemas (hueco duro)",
    r"\bOkta\b": "Okta (IdP enterprise no evidenciado, sección 6)",
    r"\bEntra ID\b": "Entra ID (IdP enterprise no evidenciado, sección 6)",
    r"\bOIDC\b": "OIDC (identidad enterprise no evidenciada, sección 6)",
}

# --- Evidencia marcada C o inexistente: mirar antes de enviar ---
# EV-21 (MCP) y EV-24 (RAG) son C: reales pero sin cerrar. A2A no existe en el banco.
C_EVIDENCE_PATTERNS = {
    r"\bMCP\b": "MCP: evidencia EV-21 marcada C. Confirmar el 'qué has construido' antes de enviar.",
    r"\bModel Context Protocol\b": "MCP: evidencia EV-21 marcada C. Confirmar profundidad real.",
    r"\bRAG\b": "RAG: evidencia EV-24 marcada C. Solo va si hay algo concreto detrás.",
}
NO_EVIDENCE_PATTERNS = {
    r"\bA2A\b": "A2A: NO existe evidencia en el banco. Regla 1: si no tiene EV, no se escribe.",
}

# --- Regla 8: español de España. Nada de variante latinoamericana ---------
# Marcadores de alta confianza: en un CV o una carta son inequívocamente LatAm
# y tienen un equivalente claro en español de España. Son palabras españolas que
# no aparecen en un texto en inglés, así que no dan falsos positivos sobre el CV
# en inglés. (patrón -> (marca, equivalente en español de España)).
SPANISH_LATAM_BLOCK = {
    r"\bcomputadora(s)?\b": ("computadora", "ordenador"),
    r"\bcelular(es)?\b": ("celular", "móvil"),
    r"\bac[aá]\b": ("acá", "aquí"),
    r"\bpostul\w+\b": ("postular/postulación", "presentar candidatura / optar a"),
    r"\bmonitore\w+\b": ("monitorear/monitoreo", "monitorizar / supervisar"),
    r"\bcapacitaci[oó]n\w*\b": ("capacitación", "formación"),
    r"\blocaci[oó]n\w*\b": ("locación", "ubicación / localización"),
    r"\bcheque(ar|o|ando|é|ados?|amos)\b": ("chequear/chequeo", "comprobar / revisar"),
}
# Marcadores de confianza media: probablemente LatAm, pero con algún uso legitimo
# en España. Se avisan para que el candidato los mire, no bloquean.
SPANISH_LATAM_WARN = {
    r"\breporte(s)?\b": ("reporte(s)", "informe(s)"),
    r"\brequerimiento(s)?\b": ("requerimiento(s)", "requisito(s)"),
    r"\bde acuerdo a\b": ("de acuerdo a", "de acuerdo con"),
    r"\baplic\w+ (a|para) (el |la |una? )?(puesto|posici[oó]n|vacante|rol)\b":
        ("aplicar a (un puesto)", "presentarse a / optar a"),
    r"\bla posici[oó]n de\b": ("la posición de (empleo)", "el puesto de"),
    r"\bmanej\w+ (un |el |los |las |a )?(equipo|proyecto|persona)":
        ("manejar (un equipo)", "gestionar / dirigir"),
}

# --- Empresas válidas: se leen de la sección 2 del banco. Cualquier otra en un
# job block = invención. No se incrustan nombres aquí: el banco es la fuente de verdad.
def known_companies(bank_text):
    """Extrae los nombres de empresa de la tabla de la sección 2 (Cronología de roles).

    Cada fila tiene la forma `| R-nn | Rol | Empresa, Ciudad | ...`. Se toma la
    tercera celda y se descarta la ciudad (lo que va tras la primera coma)."""
    companies = []
    for line in bank_text.splitlines():
        m = re.match(r"\s*\|\s*R-\d+\s*\|[^|]*\|\s*([^|]+?)\s*\|", line)
        if m:
            company = m.group(1).split(",")[0].strip()
            if company:
                companies.append(company)
    return companies

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
    def __init__(self):
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


def check_spanish_variant(text, rep, source):
    """Regla 8: español de España. Marca variante latinoamericana.
    'source' indica de qué fichero sale (CV o Mensajes.md) para el informe.
    Los marcadores son palabras españolas: no disparan sobre texto en inglés."""
    for pat, (marca, equiv) in SPANISH_LATAM_BLOCK.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            rep.block("ESPANOL-LATAM",
                      f"({source}) \"{m.group(0)}\": variante latinoamericana. "
                      f"En español de España: {equiv}. (regla 8)")
    for pat, (marca, equiv) in SPANISH_LATAM_WARN.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            rep.warn("ESPANOL-LATAM",
                     f"({source}) \"{m.group(0).strip()}\": posible variante latinoamericana. "
                     f"En español de España suele ser: {equiv}. Revisar. (regla 8)")


def run_message_checks(msg_text, bank_text, rep):
    """Aplica a la carta y al mensaje de LinkedIn (Mensajes.md) las mismas reglas
    de texto que al CV: guiones largos, señales de disponibilidad, huecos duros,
    términos sin evidencia, cifras contra el banco y español de España.
    Es el fichero donde vive el texto en español, así que es donde la regla 8 pesa."""
    label = "Mensajes.md"

    # Guiones largos (regla 7)
    for ch, name in FORBIDDEN_DASHES.items():
        if ch in msg_text:
            idx = msg_text.find(ch)
            ctx = msg_text[max(0, idx - 40): idx + 40].replace("\n", " ").strip()
            rep.block("GUION-LARGO", f"({label}) {name} encontrado: \"...{ctx}...\"  (regla 7)")

    # Señales de disponibilidad / urgencia / ERE (regla 6)
    for pat, hit in find_all(SIGNAL_PATTERNS, msg_text):
        rep.block("SENAL-PROHIBIDA", f"({label}) Posible señal de disponibilidad/urgencia: \"{hit}\"  (regla 6)")
    if re.search(ERE_PATTERN, msg_text):
        rep.block("SENAL-PROHIBIDA", f"({label}) Aparece \"ERE\": nunca en carta ni mensaje (regla 6).")

    # Huecos duros (sección 6)
    for pat, desc in HARD_GAP_PATTERNS.items():
        m = re.search(pat, msg_text, re.IGNORECASE)
        if m:
            rep.block("HUECO-DURO", f"({label}) Aparece \"{m.group(0)}\": {desc}. No puede ir en el mensaje.")

    # Términos sin evidencia (regla 1)
    for pat, desc in NO_EVIDENCE_PATTERNS.items():
        m = re.search(pat, msg_text, re.IGNORECASE)
        if m:
            rep.block("SIN-EVIDENCIA", f"({label}) {desc}")

    # Evidencia C mencionada (regla 4)
    for pat, desc in C_EVIDENCE_PATTERNS.items():
        m = re.search(pat, msg_text, re.IGNORECASE)
        if m:
            rep.warn("EVIDENCIA-C", f"({label}) {desc}")

    # Español de España (regla 8)
    check_spanish_variant(msg_text, rep, label)

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
                rep.warn("CIFRA-NO-LOCALIZADA",
                         f"({label}) Cifra '{run}' no localizada en el banco "
                         f"(revisar formato o posible invención): \"{snippet}\"")


def run_checks(paras, bank_text, docx_path):
    rep = Report()
    non_empty = [p for p in paras if p.strip()]
    full_text = "\n".join(paras)
    bank_runs = bank_numbers(bank_text)
    companies = known_companies(bank_text)

    # 1. Guiones largos (regla 7) --------------------------------------------
    dash_hits = []
    for i, p in enumerate(paras):
        for ch, name in FORBIDDEN_DASHES.items():
            if ch in p:
                dash_hits.append((name, p.strip()[:80]))
    if dash_hits:
        for name, ctx in dash_hits:
            rep.block("GUION-LARGO", f"{name} encontrado: \"{ctx}\"  (regla 7)")

    # Bullet manual con carácter '•' en vez de lista real
    if any("•" in p for p in paras):
        rep.warn("BULLET-MANUAL", "Carácter '•' escrito a mano. Deben ser bullets de lista (regla ATS).")

    # 2. Señales de disponibilidad / urgencia / ERE (regla 6) -----------------
    for pat, hit in find_all(SIGNAL_PATTERNS, full_text):
        rep.block("SENAL-PROHIBIDA", f"Posible señal de disponibilidad/urgencia: \"{hit}\"  (regla 6)")
    if re.search(ERE_PATTERN, full_text):  # sensible a mayúsculas a propósito
        rep.block("SENAL-PROHIBIDA", "Aparece \"ERE\": nunca en CV, carta ni mensaje (regla 6, sección 6).")

    # 3. Huecos duros de la sección 6 que jamás van en el CV ------------------
    for pat, desc in HARD_GAP_PATTERNS.items():
        m = re.search(pat, full_text, re.IGNORECASE)
        if m:
            rep.block("HUECO-DURO", f"Aparece \"{m.group(0)}\": {desc}. No puede ir en el CV.")

    # Términos sin ninguna evidencia en el banco (regla 1) --------------------
    for pat, desc in NO_EVIDENCE_PATTERNS.items():
        m = re.search(pat, full_text, re.IGNORECASE)
        if m:
            rep.block("SIN-EVIDENCIA", desc)

    # 4. Estructura ATS obligatoria ------------------------------------------
    upper_paras = [p.strip().upper() for p in paras]
    positions = {}
    for h in REQUIRED_HEADINGS + OPTIONAL_HEADINGS:
        positions[h] = next((i for i, up in enumerate(upper_paras) if up == h), None)

    for h in REQUIRED_HEADINGS:
        if positions[h] is None:
            rep.block("ESTRUCTURA", f"Falta la sección obligatoria: {h}")

    present_required = [h for h in REQUIRED_HEADINGS if positions[h] is not None]
    order_ok = all(
        positions[present_required[i]] < positions[present_required[i + 1]]
        for i in range(len(present_required) - 1)
    )
    if len(present_required) == len(REQUIRED_HEADINGS) and not order_ok:
        rep.block("ESTRUCTURA", "Las secciones no están en el orden ATS esperado.")

    # 5. Firma de cierre exacta y en última posición útil ---------------------
    sig_idx = next((i for i, p in enumerate(paras) if p.strip() == SIGNATURE), None)
    if sig_idx is None:
        soft = next((i for i, p in enumerate(paras) if "ATS-optimized" in p), None)
        if soft is None:
            rep.block("FIRMA", "Falta la firma de cierre obligatoria.")
        else:
            rep.warn("FIRMA", f"La firma existe pero el texto no es exacto: \"{paras[soft].strip()}\"")
    else:
        last_text_idx = max(i for i, p in enumerate(paras) if p.strip())
        if sig_idx != last_text_idx:
            rep.warn("FIRMA", "La firma no es el último elemento del documento.")

    # 6. Contacto en el cuerpo, en las primeras líneas ------------------------
    head = " ".join(non_empty[:6])
    if "@" not in head:
        rep.warn("CONTACTO", "No se ve el email en las primeras líneas. El contacto va en el cuerpo, no en cabecera.")
    if "linkedin" not in head.lower():
        rep.warn("CONTACTO", "No se ve el LinkedIn en las primeras líneas.")

    # 7. Tablas (rompen el parseo lineal) ------------------------------------
    if has_docx_tables(docx_path):
        rep.block("TABLA", "El DOCX contiene tablas. Prohibidas: rompen el orden de lectura del ATS.")

    # 8. Cifras del CV que no aparecen en el banco (reglas 1 y 2) -------------
    #    Se analiza solo la prosa (resumen, skills, bullets), no el contacto ni
    #    las líneas de empresa/fechas. Se ignoran los años.
    missing = []
    for p in paras:
        if is_meta_line(p) or not p.strip():
            continue
        for run in digit_runs(p):
            if is_year(run):
                continue
            if len(run) <= 1:
                continue  # un solo dígito es demasiado ambiguo para afirmar nada
            if run not in bank_runs:
                # localizar el token original para dar contexto
                ctx = p.strip()
                snippet = (ctx[:90] + "...") if len(ctx) > 90 else ctx
                missing.append((run, snippet))
    if missing:
        seen = set()
        for run, snippet in missing:
            key = (run, snippet)
            if key in seen:
                continue
            seen.add(key)
            rep.warn("CIFRA-NO-LOCALIZADA",
                     f"Cifra '{run}' no localizada en el banco (revisar formato o posible invención): \"{snippet}\"")

    # 9. Rangos de métrica que podrían mezclar dos roles (reglas 2 y 3) -------
    for p in paras:
        if is_meta_line(p):
            continue
        for m in re.finditer(r"\d+\s*[-–]\s*\d+\s*%", p):
            rep.warn("RANGO-METRICA",
                     f"Rango '{m.group(0).strip()}': verificar que no funde métricas de roles distintos (ej. 45% de EV-10 y 50% de EV-33).")

    # 10. Evidencia C o sin cerrar mencionada en el CV (regla 4) --------------
    for pat, desc in C_EVIDENCE_PATTERNS.items():
        m = re.search(pat, full_text, re.IGNORECASE)
        if m:
            rep.warn("EVIDENCIA-C", desc)

    # 11. Español de España en el CV (regla 8). Inofensivo si el CV va en inglés.
    check_spanish_variant(full_text, rep, "CV")

    # ---- DATOS A REVISAR (dossier para el humano) --------------------------

    # a) Orden de lectura tal como lo ve el ATS
    reading = [f"{i+1:>2}. {p.strip()}" for i, p in enumerate(non_empty[:14])]
    rep.datum("Orden de lectura (primeras 14 líneas, tal como lo ve un ATS)", reading)

    # b) Bloques de experiencia: empresa, fechas y verificación contra sección 2
    job_lines = []
    for p in paras:
        if "  |  " in p and re.search(r"\b(19|20)\d\d\b|Present", p):
            company = p.split("  |  ")[0].strip()
            if any(k.lower() in p.lower() for k in ["linkedin", "@", "github"]):
                continue  # es la línea de contacto, no un job
            known = any(c.lower() in company.lower() or company.lower() in c.lower()
                        for c in companies)
            mark = "OK" if known else "REVISAR: empresa no reconocida en sección 2"
            job_lines.append(f"[{mark}] {p.strip()}")
            if not known:
                rep.block("EMPRESA", f"Empresa no reconocida en el banco (regla 9): \"{company}\"")
    if job_lines:
        rep.datum("Bloques de experiencia (empresa | ciudad | fechas)", job_lines)

    # c) Términos de CORE SKILLS: cada uno necesita evidencia (regla 5)
    if positions["CORE SKILLS"] is not None and positions["PROFESSIONAL EXPERIENCE"] is not None:
        start, end = positions["CORE SKILLS"], positions["PROFESSIONAL EXPERIENCE"]
        terms = []
        for p in paras[start + 1:end]:
            if ":" in p:
                label, rhs = p.split(":", 1)
            else:
                label, rhs = "", p
            for t in rhs.split(","):
                t = t.strip()
                if t:
                    terms.append(t)
        if terms:
            rep.datum(f"Términos en CORE SKILLS ({len(terms)}): cada uno necesita una evidencia (regla 5)",
                      ["- " + t for t in terms])

    # d) Todas las cifras del CV localizadas en el banco (traza de métricas)
    located = []
    for p in paras:
        if is_meta_line(p) or not p.strip():
            continue
        for run in sorted(digit_runs(p)):
            if is_year(run) or len(run) <= 1:
                continue
            status = "en banco" if run in bank_runs else "NO LOCALIZADA"
            located.append(f"{run:>8}  [{status}]")
    if located:
        uniq = sorted(set(located))
        rep.datum(f"Cifras detectadas en la prosa del CV ({len(uniq)})", uniq)

    # e) Longitud aproximada del documento por conteo de caracteres
    total_chars = sum(len(p) for p in paras)
    vol = [
        f"Párrafos con texto: {len(non_empty)}",
        f"Caracteres totales: {total_chars}",
        "Referencia: un CV de 2 páginas de este sistema ronda los 6500-7800 caracteres.",
        "Es un indicio de longitud por conteo de caracteres, no un veredicto.",
    ]
    if total_chars > 8500:
        vol.append("AVISO: volumen alto. Riesgo de desbordar a una tercera página.")
    rep.datum("Volumen del documento (indicio de longitud)", vol)

    # f) Líneas viudas: una sola palabra colgando al final de un párrafo -------
    #    Cada una desperdicia una línea entera. Recortarla es el ahorro de
    #    espacio más barato para no desbordar de dos páginas.
    widows = widow_candidates(docx_path)
    if widows:
        wl = [
            "Estimación por ancho medio de carácter (Arial 9.5pt), no un veredicto:",
            "el render visual manda. Cada palabra colgando ocupa una línea entera;",
            "recortar ~esa longitud de la misma línea la sube y ahorra una línea.",
            "",
        ]
        for text, last, n in widows:
            head = (text[:66] + "...") if len(text) > 66 else text
            wl.append(f"- cuelga \"{last}\" (~{len(last) + 1} car. a recortar, {n} líneas): \"{head}\"")
        rep.datum("Líneas viudas (ahorro de espacio potencial, INDICIO)", wl)

    return rep


# ----------------------------------------------------------------------------
# Salida
# ----------------------------------------------------------------------------
def render_report(rep, docx_path, bank_path):
    tools_note = manual_checks_block(docx_path)
    lines = []
    lines.append(f"# Validación del CV")
    lines.append("")
    lines.append(f"- DOCX: `{docx_path}`")
    lines.append(f"- Banco: `{bank_path}`")
    lines.append("")
    lines.append("Este validador comprueba lo automatizable. No corrige nada. La decisión es del candidato.")
    lines.append("")

    lines.append(f"## Bloqueantes ({len(rep.blockers)})")
    lines.append("")
    if rep.blockers:
        lines.append("No enviar hasta resolverlos.")
        lines.append("")
        for code, msg in rep.blockers:
            lines.append(f"- **[{code}]** {msg}")
    else:
        lines.append("Ninguno detectado por comprobación automática.")
    lines.append("")

    lines.append(f"## Avisos ({len(rep.warnings)})")
    lines.append("")
    if rep.warnings:
        lines.append("No bloquean, pero hay que mirarlos uno a uno.")
        lines.append("")
        for code, msg in rep.warnings:
            lines.append(f"- **[{code}]** {msg}")
    else:
        lines.append("Ninguno.")
    lines.append("")

    lines.append("## Datos a revisar")
    lines.append("")
    for title, block in rep.data:
        lines.append(f"### {title}")
        lines.append("")
        for l in block:
            lines.append(l)
        lines.append("")

    lines.append("## Verificación manual pendiente")
    lines.append("")
    lines.extend(tools_note)
    lines.append("")
    return "\n".join(lines)


def manual_checks_block(docx_path):
    """La prueba de parseo ATS de la skill, que necesita pandoc. Se informa si falta."""
    import shutil
    lines = []
    lines.append("Esta es obligatoria en la skill y este validador NO la cubre.")
    lines.append("")
    have_pandoc = shutil.which("pandoc")

    lines.append("1. Prueba de parseo ATS (orden de lectura real):")
    lines.append("")
    lines.append("   ```")
    lines.append(f"   pandoc -t plain --wrap=none \"{docx_path}\"")
    lines.append("   ```")
    lines.append(f"   pandoc {'disponible' if have_pandoc else 'NO instalado: brew install pandoc'}.")
    return lines


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Validador post-creacion del CV.")
    ap.add_argument("docx", help="Ruta al CV en DOCX.")
    ap.add_argument("--bank", help="Ruta a CARRERA-EVIDENCIAS.md.")
    ap.add_argument("--out", help="Ruta del informe. Por defecto VALIDACION.md junto al DOCX.")
    args = ap.parse_args()

    if not os.path.isfile(args.docx):
        print(f"error: no existe el DOCX: {args.docx}", file=sys.stderr)
        return 2

    # Localizar el banco: --bank, o subiendo desde el DOCX hasta encontrarlo.
    bank_path = args.bank
    if not bank_path:
        d = os.path.dirname(os.path.abspath(args.docx))
        for _ in range(6):
            cand = os.path.join(d, "CARRERA-EVIDENCIAS.md")
            if os.path.isfile(cand):
                bank_path = cand
                break
            d = os.path.dirname(d)
    if not bank_path or not os.path.isfile(bank_path):
        print("error: no encuentro CARRERA-EVIDENCIAS.md. Pásalo con --bank.", file=sys.stderr)
        return 2

    with open(bank_path, encoding="utf-8") as f:
        bank_text = f.read()

    paras = read_docx_paragraphs(args.docx)
    rep = run_checks(paras, bank_text, args.docx)

    # Mensajes.md vive junto al DOCX. Es donde va el texto en español, así que
    # recibe las mismas reglas de texto (regla 8 incluida). Si no está aún, se nota.
    msg_path = os.path.join(os.path.dirname(os.path.abspath(args.docx)), "Mensajes.md")
    if os.path.isfile(msg_path):
        with open(msg_path, encoding="utf-8") as f:
            run_message_checks(f.read(), bank_text, rep)
    else:
        rep.datum("Mensajes.md",
                  [f"No encontrado junto al DOCX ({msg_path}).",
                   "Cuando exista, este validador le aplica guiones, señales, huecos,",
                   "términos sin evidencia, cifras y español de España (regla 8)."])

    report_md = render_report(rep, args.docx, bank_path)

    out_path = args.out or os.path.join(os.path.dirname(os.path.abspath(args.docx)), "VALIDACION.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(report_md)
    print(f"\n(informe escrito en: {out_path})")

    return 1 if rep.blockers else 0


if __name__ == "__main__":
    sys.exit(main())
