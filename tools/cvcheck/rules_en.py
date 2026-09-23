"""Reglas de texto para lo que se escribe en INGLÉS.

Se aplican siempre, sea cual sea el idioma del sistema: lo que cuenta es el idioma
del texto (el CV va en inglés aunque el sistema se use en español).
"""

# --- Regla 6: nada de disponibilidad ni urgencia --------------------------------
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
]

# --- Regla 8: una sola variante de inglés por documento -------------------------
# No se impone UK ni US: se avisa cuando un mismo texto mezcla las dos. Solo pares
# sin ambigüedad (no 'analyse', que choca con 'analyses', ni 'license/licence').
# (raíz US, raíz UK, sufijos admitidos)
_IZE = r"(e|es|ed|ing|ation|ations|er|ers)"
SPELLING_PAIRS = [
    ("organiz", "organis", _IZE),
    ("optimiz", "optimis", _IZE),
    ("prioritiz", "prioritis", _IZE),
    ("standardiz", "standardis", _IZE),
    ("recogniz", "recognis", _IZE),
    ("utiliz", "utilis", _IZE),
    ("moderniz", "modernis", _IZE),
    ("productiz", "productis", _IZE),
    ("behavior", "behaviour", r"(s|al)?"),
    ("color", "colour", r"(s|ed|ful)?"),
    ("favor", "favour", r"(s|ed|able|ite|ites)?"),
    ("labor", "labour", r"(s)?"),
    ("center", "centre", r"(s|d)?"),
    ("defense", "defence", r"(s)?"),
    ("modeling", "modelling", r""),
    ("modeled", "modelled", r""),
    ("traveled", "travelled", r""),
    ("labeled", "labelled", r""),
    ("canceled", "cancelled", r""),
]
