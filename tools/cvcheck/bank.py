"""Lectura del banco de evidencias, en cualquiera de sus dos idiomas.

Lo comparten validate-cv.py y el hook de pre-commit. Todo se localiza por el NÚMERO
de sección (`## 1.`, `## 2.`, `## 10.`), nunca por su título, para que un banco en
inglés y otro en español funcionen con el mismo código.
"""

import os
import re

# Nombre del banco en cada idioma. El idioma del sistema sale del propio banco.
BANK_NAMES = {"es": "CARRERA-EVIDENCIAS.md", "en": "CAREER-EVIDENCE.md"}

# Ficheros y carpetas que produce el sistema, por idioma.
FILENAMES = {
    "es": {"log": "CANDIDATURAS.md", "apps": "candidaturas", "messages": "Mensajes.md",
           "report": "VALIDACION.md"},
    "en": {"log": "APPLICATIONS.md", "apps": "applications", "messages": "Messages.md",
           "report": "VALIDATION.md"},
}

# Todo lo que nunca se versiona, en los dos idiomas. Lo usa el hook de pre-commit.
PRIVATE_PATTERNS = [
    BANK_NAMES["es"], BANK_NAMES["en"],
    FILENAMES["es"]["log"], FILENAMES["en"]["log"],
    FILENAMES["es"]["apps"] + "/*", FILENAMES["en"]["apps"] + "/*",
    "tools/cv-content.js",
    "*.docx",
    "*.pdf",
    ".claude/settings.json",
    ".claude/settings.local.json",
]

LANG_RE = re.compile(r"^\s*(?:<!--\s*)?lang\s*:\s*(es|en)\b", re.IGNORECASE)


def find_bank(start_dir, max_up=6):
    """Sube desde start_dir buscando un banco. Devuelve (ruta, None) o (None, error).
    Si en la misma carpeta hay uno de cada idioma, es ambiguo: se pide --bank."""
    d = os.path.abspath(start_dir)
    for _ in range(max_up):
        found = [os.path.join(d, n) for n in BANK_NAMES.values()
                 if os.path.isfile(os.path.join(d, n))]
        if len(found) == 1:
            return found[0], None
        if len(found) > 1:
            return None, "ambiguous"
        d = os.path.dirname(d)
    return None, "missing"


def bank_lang(bank_text, bank_path=None):
    """Idioma del sistema. Manda la línea `lang: es|en` de la cabecera del banco.
    Sin ella, se deduce del nombre del fichero. Por defecto, español (compatibilidad)."""
    for line in bank_text.splitlines()[:15]:
        m = LANG_RE.match(line)
        if m:
            return m.group(1).lower()
    if bank_path and os.path.basename(bank_path) == BANK_NAMES["en"]:
        return "en"
    return "es"


def section(bank_text, number):
    """Texto de la sección `## <number>.` hasta la siguiente `## `. '' si no existe."""
    out, inside = [], False
    head = re.compile(r"^##\s+%d\.(\s|$)" % number)
    for line in bank_text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = bool(head.match(line))
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


def table_rows(text):
    """Filas de las tablas markdown de un texto, como listas de celdas.
    Se saltan las filas separadoras (|---|---|). La cabecera sí se devuelve."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s[1:-1].split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


# --- Sección 1: identidad ------------------------------------------------------
IDENTITY_FIELDS = {"nombre", "name", "teléfono", "telefono", "phone", "email",
                   "linkedin", "github"}


def identity_values(bank_text):
    """Datos de contacto de la tabla de la sección 1 (nombre, teléfono, email...).
    Solo valores de 6 caracteres o más, para no bloquear por coincidencias triviales."""
    values = []
    for cells in table_rows(section(bank_text, 1)):
        if len(cells) >= 2 and cells[0].lower() in IDENTITY_FIELDS:
            values.append(cells[1])
    return [v for v in values if len(v) >= 6]


# --- Sección 2: cronología de roles --------------------------------------------
def known_companies(bank_text):
    """Empresas de la tabla de la sección 2. Cada fila es `| R-nn | Rol | Empresa, Ciudad | ...`:
    se toma la tercera celda y se descarta la ciudad (lo que va tras la primera coma).
    Si el banco no numera la sección 2, se buscan las filas R-nn en todo el fichero."""
    text = section(bank_text, 2) or bank_text
    companies = []
    for cells in table_rows(text):
        if len(cells) >= 3 and re.fullmatch(r"R-\d+", cells[0]):
            company = cells[2].split(",")[0].strip()
            if company:
                companies.append(company)
    return companies


# --- Sección 10: lista de vigilancia del validador -----------------------------
# Cada fila: | Término(s) | Nivel | Motivo |
#   - Término: `regex` entre comillas invertidas, o texto literal (varios, separados
#     por comas). Un literal todo en mayúsculas (MCP, ERE) distingue mayúsculas.
#   - Nivel: hueco/gap (bloquea), sin evidencia/no evidence (bloquea),
#     confirmar/confirm (avisa).
LEVELS = {
    "hueco": "gap", "gap": "gap",
    "sin evidencia": "no-evidence", "no evidence": "no-evidence",
    "confirmar": "confirm", "confirm": "confirm",
}


def _literal_pattern(term):
    """Literal -> regex con límites de palabra. Los espacios admiten variaciones
    ('21 CFR' casa con '21CFR')."""
    body = r"\s*".join(re.escape(part) for part in term.split())
    flags = 0 if re.fullmatch(r"[A-Z0-9]+", term) and re.search(r"[A-Z]", term) else re.IGNORECASE
    return re.compile(r"(?<!\w)" + body + r"(?!\w)", flags)


def watchlist(bank_text):
    """Devuelve (entradas, errores). Entrada: (nivel, [regex compilados], término, motivo).
    None en lugar de lista si el banco no tiene sección 10."""
    text = section(bank_text, 10)
    if not text.strip():
        return None, []
    entries, errors = [], []
    rows = table_rows(text)
    for cells in rows[1:]:  # la primera es la cabecera
        if len(cells) < 2 or not cells[0]:
            continue
        term_cell, level_cell = cells[0], cells[1].strip().lower()
        reason = cells[2] if len(cells) >= 3 else ""
        level = LEVELS.get(level_cell)
        if not level:
            errors.append(f"{term_cell}: nivel '{cells[1]}'")
            continue
        regexes = re.findall(r"`([^`]+)`", term_cell)
        try:
            if regexes:
                pats = [re.compile(r, re.IGNORECASE) for r in regexes]
            else:
                pats = [_literal_pattern(t.strip()) for t in term_cell.split(",") if t.strip()]
        except re.error as e:
            errors.append(f"{term_cell}: {e}")
            continue
        entries.append((level, pats, term_cell, reason))
    return entries, errors
