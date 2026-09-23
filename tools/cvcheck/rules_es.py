"""Reglas de texto para lo que se escribe en ESPAÑOL.

Se aplican siempre, sea cual sea el idioma del sistema: lo que cuenta es el idioma
del texto (una candidata que usa el sistema en inglés puede escribir una carta en
español). Son palabras españolas, así que no disparan sobre un texto en inglés.
"""

# --- Regla 6: nada de disponibilidad ni urgencia --------------------------------
# Disponibilidad del CANDIDATO, no la "disponibilidad de la plataforma" (uptime),
# que es una métrica técnica legítima.
SIGNAL_PATTERNS = [
    r"\bdisponibilidad\W+(inmediata|total|para incorporar|de incorporaci)",
    r"\bmi disponibilidad\b",
    r"\bdisponible (para|a partir|desde|de inmediato|inmediatamente|ya|en)\b",
    r"\bincorporaci[oó]n inmediata\b",
    r"\bcuanto antes\b",
    r"\burgent(e|emente)\b",          # solo formas en español; 'urgent' en inglés da falsos positivos
]

# --- Regla 8: español de España. Nada de variante latinoamericana ---------------
# Marcadores de alta confianza: en un CV o una carta son inequívocamente LatAm
# y tienen un equivalente claro en español de España.
# (patrón -> equivalente en español de España)
VARIANT_BLOCK = {
    r"\bcomputadora(s)?\b": "ordenador",
    r"\bcelular(es)?\b": "móvil",
    r"\bac[aá]\b": "aquí",
    r"\bpostul\w+\b": "presentar candidatura / optar a",
    r"\bmonitore\w+\b": "monitorizar / supervisar",
    r"\bcapacitaci[oó]n\w*\b": "formación",
    r"\blocaci[oó]n\w*\b": "ubicación / localización",
    r"\bcheque(ar|o|ando|é|ados?|amos)\b": "comprobar / revisar",
}
# Marcadores de confianza media: probablemente LatAm, pero con algún uso legítimo
# en España. Se avisan para que el candidato los mire, no bloquean.
VARIANT_WARN = {
    r"\breporte(s)?\b": "informe(s)",
    r"\brequerimiento(s)?\b": "requisito(s)",
    r"\bde acuerdo a\b": "de acuerdo con",
    r"\baplic\w+ (a|para) (el |la |una? )?(puesto|posici[oó]n|vacante|rol)\b": "presentarse a / optar a",
    r"\bla posici[oó]n de\b": "el puesto de",
    r"\bmanej\w+ (un |el |los |las |a )?(equipo|proyecto|persona)": "gestionar / dirigir",
}
