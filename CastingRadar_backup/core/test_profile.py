from profile_analyzer import ProfileAnalyzer

analyzer = ProfileAnalyzer()

pruebas = [

    "Buscamos actor de 50 a 65 años para spot publicitario en Madrid. Remunerado.",

    "Se necesita hombre entre 60 y 75 años para serie.",

    "Actriz mayor de 55 años para largometraje.",

    "Hombre 70-85 años para documental.",

    "Actor para videoclip no remunerado.",

    "Buscamos hombres y mujeres de 50 a 70 años.",

    "Actor 55+ para publicidad.",

    "Mayores de 60 años para campaña.",

    "A partir de 65 años.",

    "Hasta 45 años.",

    "Menores de 30 años.",
"Buscamos protagonista masculino de 60 años.",
"Actor secundario para serie.",
"Actor de reparto.",
"Pequeña parte para publicidad.",
"Featured Extra para anuncio internacional.",
"Figuración especial para campaña.",
"Figurantes para serie.","Featured background para spot remunerado con derechos de imagen.",
"Special extra hombre 65-75 años.",
"Campaña nacional remunerada.",
"Rodaje en Alcobendas.",
"Rodaje en San Sebastián de los Reyes.",
"Rodaje en Barcelona.",
"Hombre mayor de 70 años para comercial.",
"Mujer de 25 a 35 años para serie.",
"Actor de 60+ para documental con buyout.",
"Figuración especial para anuncio TV commercial.",
]

for texto in pruebas:

    print("=" * 60)
    print(texto)
    print(analyzer.analyze(texto))