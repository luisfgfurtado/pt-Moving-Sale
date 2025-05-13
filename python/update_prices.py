import csv
import os
import re

# Caminho para o arquivo CSV
csv_file = '/Users/luisfurtado/Downloads/Itens_e_Pre_os.csv'

# Caminho para a pasta com os arquivos HTML
html_folder = '/Users/luisfurtado/Downloads/bazzar/site_bazar'

counter = 0
# Carregar os preços do CSV
prices = {}
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Pular o cabeçalho
    for row in reader:
        item_name = row[0].strip()
        price = row[1].strip()
        prices[item_name] = price

# Criar um conjunto para rastrear itens encontrados
found_items = set()

# Atualizar os preços nos arquivos HTML
for root, _, files in os.walk(html_folder):
    for file_name in files:
        # Ignorar arquivos que começam com "index"
        if file_name.startswith("index") or not file_name.endswith('.html'):
            continue

        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='utf-8') as html_file:
            content = html_file.read()

        # Procurar pelo nome do item no arquivo HTML
        for item_name, price in prices.items():
            if item_name in content:
                counter += 1
                found_items.add(item_name)  # Marcar o item como encontrado
                # Atualizar o preço no arquivo atual
                updated_content = re.sub(
                    r'<p class="item-price-detail">€ [\d.,]+</p>',
                    f'<p class="item-price-detail">{price}</p>',
                    content
                )
                with open(file_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(updated_content)
                print(f'{counter} > "{item_name}" -> {file_name} -> {price}')

                # Procurar e atualizar o arquivo correspondente com sufixo "-en"
                en_file_name = file_name.replace("-pt", "-en")
                en_file_path = os.path.join(root, en_file_name)
                if os.path.exists(en_file_path):
                    with open(en_file_path, 'r', encoding='utf-8') as en_file:
                        en_content = en_file.read()
                    updated_en_content = re.sub(
                        r'<p class="item-price-detail">€ [\d.,]+</p>',
                        f'<p class="item-price-detail">{price}</p>',
                        en_content
                    )
                    with open(en_file_path, 'w', encoding='utf-8') as en_file:
                        en_file.write(updated_en_content)
                    print(f'{counter} > "{item_name}" -> {en_file_name} -> {price}')

# Identificar itens sem correspondência
unmatched_items = set(prices.keys()) - found_items

# Listar itens sem correspondência
if unmatched_items:
    print("\nItens sem correspondência:")
    for item in unmatched_items:
        print(f"- {item}")
else:
    print("\nTodos os itens tiveram correspondência.")