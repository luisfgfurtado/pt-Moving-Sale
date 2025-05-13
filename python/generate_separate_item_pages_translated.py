import json
import os
import re # For sanitizing filenames

# --- Configuration ---
full_data_json_path = "/home/ubuntu/site_bazar/full_item_data_translated.json"
output_site_dir = "/home/ubuntu/site_bazar"
whatsapp_number = "+351915722650"
footer_text_additional = "Faro | Algarve | Portugal"

# --- Load Data ---
try:
    with open(full_data_json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
except FileNotFoundError:
    print(f"Error: {full_data_json_path} not found. Cannot generate site.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {full_data_json_path}.")
    exit()

# --- Helper to sanitize for HTML filenames ---
def sanitize_filename(name):
    name = str(name) # Ensure it's a string
    name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name) # Allow dots for extensions
    name = re.sub(r'_+', '_', name) # Replace multiple underscores with one
    return name.lower()

# --- Comprehensive CSS Content ---
css_content = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f9f9f9;
    color: #333;
    line-height: 1.6;
}
header {
    background-color: #ffffff;
    padding: 20px 40px;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
header h1 a {
    margin: 0;
    font-size: 1.8em;
    font-weight: 600;
    text-decoration: none;
    color: inherit;
}
.lang-switcher-home a, .lang-switcher-item a {
    margin-left: 10px;
    text-decoration: none;
    color: #007aff;
    font-weight: 500;
}
.container {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
}

/* Homepage Card Styles */
.item-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    margin-top: 20px;
}
.item-card {
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    text-align: left;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
}
.item-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 15px;
}
.item-card h3 {
    font-size: 1.25em;
    font-weight: 600;
    margin: 0 0 8px 0;
    line-height: 1.3;
}
.item-card h3 a {
    text-decoration: none;
    color: #333;
}
.item-card h3 a:hover {
    color: #007aff;
}
.item-card .price {
    font-size: 1.15em;
    font-weight: 600;
    color: #007aff;
    margin-bottom: 0;
}

/* Item Detail Page Styles */
.item-detail-container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.item-detail-container h2 {
    margin-top: 0;
    font-size: 2em;
    font-weight: 600;
}
.item-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
    margin: 20px 0;
}
.item-gallery img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    object-fit: cover;
    cursor: pointer; /* For lightbox */
}
.item-description {
    margin: 20px 0;
}
.item-description h3 {
    margin-top: 0;
    margin-bottom: 10px;
}
.item-price-detail {
    font-size: 1.5em;
    font-weight: 600;
    color: #007aff;
    margin: 20px 0;
}
.reserve-button {
    display: inline-block;
    background-color: #007aff;
    color: white;
    padding: 12px 25px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    font-size: 1.1em;
    transition: background-color 0.2s ease;
}
.reserve-button:hover {
    background-color: #005ecb;
}

footer {
    text-align: center;
    padding: 30px;
    margin-top: 50px;
    font-size: 0.9em;
    color: #888;
    border-top: 1px solid #e0e0e0;
}
footer a {
    color: #007aff;
    text-decoration: none;
}
footer a:hover {
    text-decoration: underline;
}
"""
css_file_path = os.path.join(output_site_dir, "style.css")
with open(css_file_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print(f"Generated comprehensive CSS file at {css_file_path}")

# --- Generate individual item pages (PT and EN) ---
for item in items:
    item_id_original = item.get("id", "unknown_id")
    item_id_sanitized = sanitize_filename(item_id_original)
    
    title_pt = item.get("title_pt", "Item sem título")
    title_en = item.get("title_en", title_pt) 
    if not title_en: title_en = title_pt

    description_pt_html = item.get("description_pt", "Descrição não disponível.").replace('\n', '<br>')
    description_en_html = item.get("description_en", description_pt_html) 
    if not description_en_html and description_pt_html: description_en_html = description_pt_html
    if not description_en_html and not description_pt_html: description_en_html = "Description not available."

    price = item.get("price", "0.00")
    images = item.get("images", [])
    
    page_url_pt = f"item-{item_id_sanitized}-pt.html"
    page_url_en_for_pt_page = f"item-{item_id_sanitized}-en.html"
    whatsapp_message_pt = f"Fiquei interessado no {title_pt}"
    whatsapp_link_pt = f"https://wa.me/{whatsapp_number}?text={whatsapp_message_pt.replace(' ', '%20')}"
    footer_whatsapp_link = f"https://wa.me/{whatsapp_number.replace('+', '')}"
    
    item_html_content_pt = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_pt}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css">
</head>
<body>
    <header>
        <h1><a href="index-pt.html">Bazar de Mudança</a></h1>
        <div class="lang-switcher-item">
            <a href="{page_url_en_for_pt_page}">English</a>
        </div>
    </header>
    <div class="container">
        <div class="item-detail-container">
            <h2>{title_pt}</h2>
            <div class="item-gallery">
    """
    if images:
        for img_src in images:
            item_html_content_pt += f"                <a href=\"{img_src}\" data-lightbox=\"{item_id_sanitized}-pt\" data-title=\"{title_pt}\"><img src=\"{img_src}\" alt=\"{title_pt}\"></a>\n"
    else:
        item_html_content_pt += "                <p>Nenhuma imagem disponível.</p>\n"
    item_html_content_pt += f"""
            </div>
            <div class="item-description">
                <div class="availability">Disponível para retirada imediata</div>
                <h3>Descrição</h3>
                <p>{description_pt_html}</p>
            </div>
            <p class="item-price-detail">€ {price}</p>
            <a href="{whatsapp_link_pt}" class="reserve-button" target="_blank" rel="noopener">Reservar via WhatsApp</a>
        </div>
    </div>
    <footer>
        <p>Todos os itens à venda. Contacte para mais informações.</p>
        <p><a href="{footer_whatsapp_link}" target="_blank" rel="noopener">WhatsApp: {whatsapp_number}</a> | {footer_text_additional}</p>
    </footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox-plus-jquery.min.js"></script>
</body>
</html>
    """
    with open(os.path.join(output_site_dir, page_url_pt), 'w', encoding='utf-8') as f:
        f.write(item_html_content_pt)

    page_url_en = f"item-{item_id_sanitized}-en.html"
    page_url_pt_for_en_page = f"item-{item_id_sanitized}-pt.html"
    whatsapp_message_en = f"I am interested in the {title_en}"
    whatsapp_link_en = f"https://wa.me/{whatsapp_number}?text={whatsapp_message_en.replace(' ', '%20')}"

    item_html_content_en = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_en}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css">
</head>
<body>
    <header>
        <h1><a href="index-en.html">Moving Sale Bazaar</a></h1>
        <div class="lang-switcher-item">
            <a href="{page_url_pt_for_en_page}">Português</a>
        </div>
    </header>
    <div class="container">
        <div class="item-detail-container">
            <h2>{title_en}</h2>
            <div class="item-gallery">
    """
    if images:
        for img_src in images:
            item_html_content_en += f"                <a href=\"{img_src}\" data-lightbox=\"{item_id_sanitized}-en\" data-title=\"{title_en}\"><img src=\"{img_src}\" alt=\"{title_en}\"></a>\n"
    else:
        item_html_content_en += "                <p>No images available.</p>\n"
    item_html_content_en += f"""
            </div>
            <div class="item-description">
                <h3>Description</h3>
<div class="availability">Available for immediate pickup</div>
                <p>{description_en_html}</p>
            </div>
            <p class="item-price-detail">€ {price}</p>
            <a href="{whatsapp_link_en}" class="reserve-button" target="_blank" rel="noopener">Reserve via WhatsApp</a>
        </div>
    </div>
    <footer>
        <p>All items for sale. Contact for more information.</p>
        <p><a href="{footer_whatsapp_link}" target="_blank" rel="noopener">WhatsApp: {whatsapp_number}</a> | {footer_text_additional}</p>
    </footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox-plus-jquery.min.js"></script>
</body>
</html>
    """
    with open(os.path.join(output_site_dir, page_url_en), 'w', encoding='utf-8') as f:
        f.write(item_html_content_en)

print(f"Individual item HTML pages (PT and EN) with comprehensive CSS, updated footer, Lightbox2, and translated content generated in {output_site_dir}")


