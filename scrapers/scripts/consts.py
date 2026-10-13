"""
Supermarket data project - cleaning dictionaries

This script covers dictionaries that map naming conventions to clean the supermarket
data. Included conventions are store names and product classifications.

"""
import re
#%%% Dicionaries
store_dict = {
    "store1":"store 1",
    "store2":"store 2",
    "store3":"store 3",
    "store4":"store 4",
    }

classification_dict = {


    "habichuelas":"beans",
    "habichuela":"beans", # work on accepting plural and singular variants in pattern
    "habas":"beans",
    "maiz":"beans",
    "garbanzos":"beans",
    "habas":"beans",
    "chicharos":"beans",

    "cerveza":"beer",
    "hard seltzer":"beer",
    "smirnoff":"beer",
    "four loko":"beer",
    "roskoff":"beer",




    "pan":"bread",
    "bagel":"bread",
    "tostadas":"bread",
    "croissants":"bread",

    "cafe":"coffee",


    "salsa":"condiments",
    "caldo":"condiments",
    "sazon":"condiments",
    "azucar":"condiments",
    "miel":"condiments",
    "paprika":"condiments",
    "crema inglesa":"condiments",
    "crema agria":"condiments",
    "mostaza":"condiments",
    "sazonador":"condiments",
    "splenda":"condiments",
    "sirop":"condiments",
    "stevia":"condiments",
    "pimientos":"condiments",
    "edulcorante":"condiments",
    "endulzante":"condiments",


    "sal":"salt",

    "aceite":"cooking oil",

    "vaso":"cookware",
    "tapa":"cookware",
    "servilleta":"cookware",
    "sarten":"cookware",
    "molde":"cookware",
    "contenedor":"cookware",
    "plato":"cookware",
    "platos":"cookware",
    "cuberteria":"cookware",
    "botella":"cookware",
    "cortador de galletas":"cookware",
    "cafetera":"cookware",
    "capacillos":"cookware",


    "huevos":"eggs",

    "mango":"fruits",
    "melocoton":"fruits",
    "compota":"fruits",
    "manzana":"fruits",
    "pina":"fruits",
    "auyama":"fruits",
    "lychees":"fruits",
    "frutas":"fruits",
    "moras":"fruits",
    "datiles":"fruits",
    "chinola":"fruits",
    "peras":"fruits",
    "clementinas":"fruits",
    "mapuey":"fruits",
    "naranja":"fruits",
    "guineo":"fruits",
    "platano":"fruits",
    "melon":"fruits",
    "uva":"fruits",
    "guineitos":"fruits",

    "bombillo":"house care",
    "limpiador":"house care",
    "suavizante":"house care",
    "detergente":"house care",
    "papel":"house care",
    "removedor":"house care",
    "ambientador":"house care",
    "pila":"house care",
    "velon":"house care",
    "lejia":"house care",
    "desengrasante":"house care",
    "cera":"house care",
    "esponja":"house care",
    "escoba":"house care",
    "moho":"house care",
    "cloro":"house care",
    "encendedor":"house care",
    "endendedores":"house care",
    "betun":"house care",
    "ratones":"house care",
    "inodoro":"house care",
    "scapuntas":"house care",
    "insecticida":"house care",
    "vela":"house care",
    "quitamanchas":"house care",
    "desinfectante":"house care",
    "lavaplatos":"house care",
    "guantes":"house care",
    "difusor":"house care",
    "deshumidificador":"house care",
    "ambiental":"house care",
    "suaper":"house care",
    "almidon":"house care",
    "funda":"house care",
    "fundas":"house care",
    "madera":"house care",
    "bicarbonato":"house care",
    "fregador":"house care",
    "esponjillas":"house care",
    "pano":"house care",
    "panito":"house care",
    "muebles":"house care",
    "carbosota":"house care",
    "baking soda":"house care",



    "jugo":"juice",
    "zumo":"juice",

    "bebida hidratante":"energy drink",
    "bebida electrolito":"energy drink",
    "gatorade":"energy drink",
    "bebida para hidratacion":"energy drink",


    "leche de almendra":"milk substitute",
    "leche de soya":"milk substitute",
    "leche de avena":"milk substitute",
    "leche de pistacho":"milk substitute",

    "mantequilla de avena":"milk substitute",
    "mantequilla de almendra":"milk substitute",
    "mantequilla de cajuil":"milk substitute",
    "margarina":"milk substitute",



    "leche":"milk",
    "carnation":"milk",
    "cocoa":"milk",
    "formula":"milk",
    "bebida nutricional":"milk",
    "suplemento":"milk",


    "mantequilla":"butter",

    "yogurt":"yoghurt",


    "tortellini":"pasta",
    "tortelloni":"pasta",
    "lasagna":"pasta",
    "linguine":"pasta",
    "gnocchi":"pasta",
    "antipasto":"pasta",
    "ravioli":"pasta",
    "lasagna":"pasta",
    "macarrones":"pasta",
    "spaghetti":"pasta",
    "spaghettoni":"pasta",
    "raviolini":"pasta",
    "pasta rellena":"pasta",

    "plantilla":"personal care",
    "higienico":"personal care",
    "toallas":"personal care",
    "toallitas":"personal care",
    "tampones":"personal care",
    "jabon":"personal care",
    "exfoliante":"personal care",
    "wipes":"personal care",
    "enjuague":"personal care",
    "manitas":"personal care",
    "desodorante":"personal care",
    "tinte":"personal care",
    "cepillo":"personal care",
    "rizador":"personal care",
    "humectante":"personal care",
    "mascarilla":"personal care",
    "shampoo":"personal care",
    "acondicionador":"personal care",
    "dental":"personal care",
    "protectores":"personal care",
    "rasuradora":"personal care",
    "panales":"personal care",
    "facial":"personal care",
    "capilo":"personal care",
    "teals":"personal care",
    "spf":"personal care",
    "serum":"personal care",
    "dental":"personal care",
    "repelente":"personal care",
    "pastillas":"personal care",
    "absorbente":"personal care",
    "desmanchador":"personal care",


    "gato":"pet care",
    "perro":"pet care",
    "pez":"pet care",
    "mascota":"pet care",
    "mascotas":"pet care",

    "harina":"processed grain",
    "tortitas":"processed grain",
    "tortillas":"processed grain",
    "pancakes":"processed grain",
    "avena":"processed grain",
    "cereal":"processed grain",
    "tortilla":"processed grain",
    "casabe":"processed grain",
    "waffles":"processed grain",
    "papilla":"processed grain",
    "masa":"processed grain",
    "granola":"processed grain",
    "barra":"processed grain",



    "hummus":"prepared foods",
    "pizza":"prepared foods",
    "empanada":"prepared foods",
    "empanadas":"prepared foods",
    "empanaditas":"prepared foods",
    "pastel en hoja":"prepared foods",
    "catibias":"prepared foods",


    "barra de chocolate":"chocolate",






    "salami":"processed meat",
    "salchicha":"processed meat",
    "jamon":"processed meat",
    "prosciutto":"processed meat",
    "mortadella":"processed meat",
    "nuggets":"processed meat",
    "tapas":"processed meat",
    "charcuteria":"processed meat",

    "arroz":"grain",
    "trigo":"grain",
    "farro":"grain",
    "quinoa":"grain",

    "gelatina":"snacks",
    "snack":"snacks",
    "galletas":"snacks",
    "galletitas":"snacks",
    "dulce de":"snacks",
    "chips":"snacks",
    "pipas":"snacks",
    "platanitos":"snacks",
    "yuquitas":"snacks",
    "palitos":"snacks",
    "galleta":"snacks",
    "tiras":"snacks",
    "palito":"snacks",
    "caramelos":"snacks",
    "chicharron":"snacks",
    "chispas":"snacks",
    "donas":"snacks",
    "aros de cebolla":"snacks",
    "marshmallow":"snacks",
    "pudding":"snacks",
    "fritas":"snacks",
    "palomitas":"snacks",
    "fun size":"snacks",
    "bombon":"snacks",
    "bombones":"snacks",
    "hershey":"snacks",
    "haribo":"snacks",
    "m&m's":"snacks",
    "choco trio":"snacks",
    "paletas":"snacks",
    "pretzel":"snacks",
    "dip":"snacks",

    "pastel":"cake",
    "bizcocho":"cake",
    "boquilla":"cake",
    "extracto":"cake",
    "coco rallado":"cake",
    "budin":"cake",
    "relleno para pie":"cake",
    "levadura":"cake",
    "pudin":"cake",
    "hornear":"cake",
    "vainilla":"cake",


    "cordero":"fresh meat",
    "carne":"fresh meat",
    "pechuga":"fresh meat",
    "churrasco":"fresh meat",
    "palomilla":"fresh meat",
    "secreto":"fresh meat",
    "steak":"fresh meat",
    "costilla":"fresh meat",
    "hamburguesa":"fresh meat",
    "pavo entero":"fresh meat",
    "pavo congelado":"fresh meat",
    "muslo":"fresh meat",
    "pico y pala":"fresh meat",
    "pollo entero":"fresh meat",
    "gallina congelada":"fresh meat",
    "tocineta":"fresh meat",
    "alas":"fresh meat",

    "queso":"cheese",
    "auricchio":"cheese",
    "creme fraiche":"cheese",

    "refresco":"soft drinks",
    "agua tonica":"soft drinks",
    "agua gasificada":"soft drinks",
    "agua mineral":"soft drinks",
    "malta":"soft drinks",
    "agua tonica":"soft drinks",
    "tonica":"soft drinks",
    "club soda":"soft drinks",
    "agua tonica":"soft drinks",

    "agua":"water",

    "te":"tea",

    "batata":"vegetables",
    "yautia":"vegetables",
    "zanahoria":"vegetables",

    "papa":"vegetables",
    "aji":"vegetables",
    "tofu":"vegetables",
    "berenjena":"vegetables",
    "tomates":"vegetables",
    "remolacha":"vegetables",
    "trufas":"vegetables",
    "vegetales mixtos":"vegetables",
    "alcachofa":"vegetables",
    "ajo":"vegetables",
    "rucula":"vegetables",
    "apio":"vegetables",
    "name":"vegetables",
    "cebolla":"vegetables",
    "pepino":"vegetables",
    "tofu":"vegetables",

    "vino":"wine",
    "vinos":"wine",
    "oporto":"wine",
    "sidra":"wine",
    "champin":"wine",
    "cava":"wine",
    "prosecco":"wine",
    "espumante":"wine",
    "jerez":"wine",



    "aguardiente":"spirits",
    "cognac":"spirits",
    "brandy":"spirits",
    "ron":"spirits",
    "aperitivo":"spirits",
    "cachaca":"spirits",
    "grappa":"spirits",
    "ginebra":"spirits",
    "licor":"spirits",
    "sangria":"spirits",
    "coctel":"spirits",
    "tequila":"spirits",
    "mezcla":"spirits",
    "vodka":"spirits",
    "mamajuana":"spirits",
    "whisky":"spirits",
    "bitter":"spirits",
    "mezcal":"spirits",
    "mojito":"spirits",
    "daiquiri":"spirits",
    "ponche":"spirits",


    }

store_brand = ['lider','zerca','bravo']

#For product classification, Build regex pattern with word boundaries (\b)
pattern = r'\b(' + '|'.join(map(re.escape, classification_dict)) + r')\b'
pattern2 = r'\b(' + '|'.join(map(re.escape, store_brand)) + r')\b'
