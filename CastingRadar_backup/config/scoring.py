# =====================================================
# PUNTUACIÓN POR PAPEL
# =====================================================

ROLE_SCORE = {

    "protagonista": 40,

    "secundario": 30,

    "reparto": 20,

    "pequena_parte": 15,

    # Muy interesante, especialmente en publicidad
    "featured_extra": 20,

    # Interesante
    "figuracion_especial": 10,

    # Baja prioridad
    "figuracion": -40,
}

# =====================================================
# PRODUCCIÓN
# =====================================================

PRODUCTION_SCORE = {

    "publicidad": 30,

    "spot": 30,

    "campaña": 30,

    "serie": 20,

    "largometraje": 18,

    "documental": 15,

    "cortometraje": 10,

    "videoclip": 8,
}

# =====================================================
# REMUNERACIÓN
# =====================================================

REMUNERATION_SCORE = {

    True: 20,

    False: -30,

    None: 0,
}

# =====================================================
# DERECHOS DE IMAGEN
# =====================================================

RIGHTS_SCORE = {

    True: 20,

    False: 0,
}

# =====================================================
# UBICACIÓN
# =====================================================

LOCATION_SCORE = {

    "madrid_norte": 35,

    "madrid": 25,

    "nacional": 15,

    "otras": 0,
}

# =====================================================
# SEXO
# =====================================================

SEX_SCORE = {

    "hombre": 15,

    "ambos": 10,

    "mujer": -100,

    None: 0,
}

# =====================================================
# EDAD
# =====================================================

AGE_MATCH_SCORE = 20

AGE_UNKNOWN_SCORE = 0