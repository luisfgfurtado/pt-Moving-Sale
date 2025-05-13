import csv
import re
import unicodedata

def normalize_text(text):
    """Remove acentos, converte para minúsculas e normaliza espaços"""
    # Remove acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Converte para minúsculas
    text = text.lower()
    # Remove caracteres especiais e normaliza espaços
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Normaliza espaços em branco
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Caminho para o arquivo CSV
csv_file = '/Users/luisfurtado/Downloads/Itens_e_Pre_os.csv'
index_file = '/Users/luisfurtado/Downloads/bazzar/site_bazar/index-pt.html'

# Carregar os preços do CSV com texto normalizado
prices = {}
normalized_prices = {}
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Pular o cabeçalho
    for row in reader:
        item_name = row[0].strip()
        price = row[1].strip()
        normalized_name = normalize_text(item_name)
        prices[normalized_name] = price
        normalized_prices[normalized_name] = item_name

# Atualizar os preços no index-pt.html
with open(index_file, 'r', encoding='utf-8') as file:
    content = file.read()

found_items = set()
# Encontrar todos os títulos de itens no HTML
pattern = r'<h3>\s*<a[^>]*>(.*?)</a>\s*</h3>\s*<div\s+class="price-section">\s*<p\s+class="price">€\s*[\d.,]+</p>'
matches = re.finditer(pattern, content, re.DOTALL)

for match in matches:
    html_item_name = match.group(1)
    normalized_html_name = normalize_text(html_item_name)
    
    if normalized_html_name in prices:
        found_items.add(normalized_html_name)
        new_price = prices[normalized_html_name]
        
        # Criar o padrão de substituição específico para este item
        replacement_pattern = rf'(<h3>\s*<a[^>]*>{re.escape(html_item_name)}</a>\s*</h3>\s*<div\s+class="price-section">\s*<p\s+class="price">)€\s*[\d.,]+(</p>)'
        content = re.sub(replacement_pattern, rf'\1{new_price}\2', content, flags=re.DOTALL)
        print(f'Atualizado: {normalized_prices[normalized_html_name]} -> {new_price}')

# Salvar o arquivo atualizado
with open(index_file, 'w', encoding='utf-8') as file:
    file.write(content)

# Listar itens sem correspondência
unmatched_items = set(normalized_prices.keys()) - found_items
if unmatched_items:
    print("\nItens sem correspondência:")
    for item in unmatched_items:
        print(f"- {normalized_prices[item]}")
else:
    print("\nTodos os itens tiveram correspondência.")

print("\nAtualização concluída!")