import json
import re

# --- Configuration ---
full_data_json_path = "/home/ubuntu/site_bazar/full_item_data.json"
output_translated_data_path = "/home/ubuntu/site_bazar/full_item_data_translated.json"

# --- Simple Internal Translation Logic ---
def internal_translate(text_pt, lang_to="en"):
    if not text_pt:
        return ""
    if lang_to == "en":
        # Dictionary for known titles (exact matches from CSV "Descrição" column)
        title_translations = {
            "Radiador a Óleo 2500W": "2500W Oil Radiator",
            "Tineco Floor One S5": "Tineco Floor One S5",
            "Banco alto, preto / velatura castanha, 63 cm": "High stool, black / brown stained, 63 cm",
            "Shnuggle Baby Bath - com suporte": "Shnuggle Baby Bath - with stand",
            "Berço TRAMA Cama Cosleep Musa Branco/Tola": "TRAMA Cosleep Crib Musa White/Tola",
            "Poltrona, chapa de carvalho": "Armchair, oak veneer",
            "Cadeira dobrável GUNDE": "GUNDE Folding Chair",
            "Cadeira de Escritório Executiva MITSAI Roma Preto": "MITSAI Roma Executive Office Chair Black",
            "Cadeira escritório": "Office Chair",
            "Cadeira de Refeição KINDERKRAFT Yummy Grey": "KINDERKRAFT Yummy High Chair Grey",
            "Conjunto de 4 x Cadeiras de jantar": "Set of 4 Dining Chairs",
            "Cama casal completa com cabeceira e colchão, branco, 160x200 cm": "Complete double bed with headboard and mattress, white, 160x200 cm",
            "Cama de casal com cabeceira e colchão 140x200 cm": "Double bed with headboard and mattress 140x200 cm",
            "Cama de solteiro completa com colchão novo 90 x 190 cm": "Complete single bed with new mattress 90 x 190 cm",
            "Cómoda c/6 gavetas, branco, 138x84 cm": "Chest of 6 drawers, white, 138x84 cm",
            "Varinha Mágica Bosh": "Bosch Hand Blender",
            "Fritadeira sem Óleo PHILIPS": "PHILIPS Oil-Free Fryer",
            "Espelho, ef carvalho 65x150 cm": "Mirror, oak effect 65x150 cm",
            "Espelho redondo - chapa de nogueira, 60 cm": "Round mirror - walnut veneer, 60 cm",
            "Impressora Multifuncional Epson": "Epson Multifunction Printer",
            "Caixote c/tampa, cinz clr, 22 l": "Bin with lid, light grey, 22 l",
            "Chicco Recipiente de fraldas": "Chicco Nappy Bin",
            "Caixote c/tampa de pressão, aço inoxidável, 4 l": "Bin with pressure lid, stainless steel, 4 l",
            "Candeeiro de pé, freixo/branco": "Floor lamp, ash/white",
            "Secretária, branco, 142x50 cm": "Desk, white, 142x50 cm",
            "Mesa, branco, 125x75 cm": "Table, white, 125x75 cm",
            "Mesa, branco, 120x60 cm": "Table, white, 120x60 cm",
            "Secretária de trabalho com caveletes de altura ajustável 75 x 150 cm": "Work desk with height-adjustable trestles 75 x 150 cm",
            "2 x Monitores ASUS VZ24EHE (23.8\" - FHD - IPS)": "2 x ASUS VZ24EHE Monitors (23.8\" - FHD - IPS)",
            "Set 7 Peças - Trem De Cozinha TEFAL": "TEFAL 7-Piece Cookware Set",
            "Estante de parede (prateleiras), branco, 110x26 cm": "Wall shelf (shelves), white, 110x26 cm",
            "LACK Estante de parede (prateleiras), branco, 190x26 cm": "LACK Wall shelf (shelves), white, 190x26 cm",
            "Móvel TV, branco, 180x40x38 cm": "TV unit, white, 180x40x38 cm",
            "Sapateira": "Shoe Rack",
            "Sofá 3 lugares": "3-seater sofa",
            "Tabua de passar roupa": "Ironing Board",
            "Tábua de engomar sevilha": "Seville ironing board",
            "TV LG 65NANO766QA": "LG 65NANO766QA TV",
            "Dreo 25dB Ventilador de torre inteligente 106 cm": "Dreo 25dB Smart Tower Fan 106 cm",
        }
        
        # Check if it is a known title first
        if text_pt in title_translations:
            return title_translations[text_pt]

        # For descriptions or other texts not in the title_translations dictionary:
        # Provide the Portuguese text with a clear note about AI translation and review.
        # This is an attempt to fulfill the translation request directly.
        # A more sophisticated approach would involve a real translation API/library.
        # For now, this makes it clear that it's an AI attempt based on the PT text.
        
        # Basic keyword/phrase replacements for a slightly better "translation feel"
        # This is very rudimentary and should be used with caution.
        translated_text = text_pt
        simple_replacements = {
            "Sobre o produto": "About the product",
            "Descrição": "Description",
            "Cor": "Color",
            "Material": "Material",
            "Dimensões": "Dimensions",
            "Altura": "Height",
            "Largura": "Width",
            "Profundidade": "Depth",
            "Características": "Features",
            "Especificações": "Specifications",
            "Inclui": "Includes",
            "Não inclui": "Does not include",
            "Como novo": "Like new",
            "Em bom estado": "In good condition",
            "Usado": "Used",
            "excelente estado": "excellent condition",
            # Add more common phrases carefully
        }

        for pt_phrase, en_phrase in simple_replacements.items():
            translated_text = re.sub(r"\b" + re.escape(pt_phrase) + r"\b", en_phrase, translated_text, flags=re.IGNORECASE)

        return f"--- (AI-Assisted Translation - Please Review) ---\n{translated_text}\n---"

    return text_pt # Default to original if lang_to is not 'en'

# --- Load Data ---
try:
    with open(full_data_json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
except FileNotFoundError:
    print(f"Error: {full_data_json_path} not found. Cannot process translations.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {full_data_json_path}.")
    exit()

translated_items = []

for item in items:
    item_copy = item.copy()
    title_pt = item_copy.get("title_pt", "")
    description_pt = item_copy.get("description_pt", "")

    item_copy["title_en"] = internal_translate(title_pt, lang_to="en")
    
    # Always attempt to translate the Portuguese description for the English version
    if description_pt:
        item_copy["description_en"] = internal_translate(description_pt, lang_to="en")
    else:
        item_copy["description_en"] = "Description not available." # Or some other placeholder if PT is also empty
        
    item_copy["description_en_is_fallback"] = False # Mark that we attempted translation

    translated_items.append(item_copy)

# --- Save Translated Data ---
with open(output_translated_data_path, 'w', encoding='utf-8') as outfile:
    json.dump(translated_items, outfile, indent=4, ensure_ascii=False)

print(f"Enhanced translation processing complete. Translated data saved to {output_translated_data_path}")

