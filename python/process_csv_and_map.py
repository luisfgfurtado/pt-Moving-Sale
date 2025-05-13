import csv
import os
import json

# --- Configuration ---
csv_file_path = "/home/ubuntu/upload/Inventário.csv"
zip_extracted_base_dir = "/home/ubuntu/inventory_check"
output_processed_data_path = "/home/ubuntu/site_bazar/processed_inventory_data.json"
output_mapping_report_path = "/home/ubuntu/site_bazar/mapping_report.txt"

items_to_exclude_csv_pasta_name = ["Estante branco 77x77", "Candeeiro de pé"]
item_to_mark_reserved_title_pt = "Tineco Floor One S5" # Title from CSV 'Descrição' column

# --- Helper Functions ---
def sanitize_folder_name(name):
    return name.strip()

# --- 1. Read CSV Data ---
csv_items = []
csv_header = []
problematic_csv_rows = []

try:
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile, delimiter=';')
        csv_header = [h.strip() for h in next(reader)]
        if not csv_header or len(csv_header) < 4:
            raise ValueError("CSV header is missing or has too few columns (expected at least Item, Descrição, Qtd, Pasta, Preço).")

        pasta_col_index = -1
        item_col_index = -1
        desc_col_index = -1
        qtd_col_index = -1
        preco_col_index = -1

        for i, col_name in enumerate(csv_header):
            col_lower = col_name.lower()
            if 'pasta' in col_lower:
                pasta_col_index = i
            elif 'item' == col_lower:
                item_col_index = i
            elif 'descrição' in col_lower:
                desc_col_index = i
            elif 'qtd' in col_lower:
                qtd_col_index = i
            elif 'preço' in col_lower or 'preco' in col_lower:
                preco_col_index = i
        
        if desc_col_index == -1:
            raise ValueError("Column for 'Descrição' (used as title) not found in CSV header.")
        if item_col_index == -1:
            item_col_index = desc_col_index # Default to Descrição if Item column is missing
        if pasta_col_index == -1:
            raise ValueError("Column for 'Pasta' not found in CSV header.")
        if qtd_col_index == -1:
            raise ValueError("Column for 'Qtd' not found in CSV header.")
        if preco_col_index == -1:
            raise ValueError("Column for 'Preço' not found in CSV header.")

        for i, row in enumerate(reader):
            if len(row) == len(csv_header):
                item_name_raw = row[item_col_index].strip()
                description_as_title = row[desc_col_index].strip()
                quantity = row[qtd_col_index].strip()
                price_raw = row[preco_col_index].strip()
                price = price_raw.replace('€', '').replace(',', '.').strip()
                folder_name_csv = sanitize_folder_name(row[pasta_col_index])
                
                try:
                    float(price)
                except ValueError:
                    problematic_csv_rows.append(f"Row {i+2}: Invalid price format for item '{description_as_title}': '{price_raw}'. Using 0.00.")
                    price = "0.00"

                if folder_name_csv and folder_name_csv not in items_to_exclude_csv_pasta_name:
                    status = "available" # Default status
                    if description_as_title == item_to_mark_reserved_title_pt:
                        status = "reserved"
                    
                    csv_items.append({
                        "csv_item_name": item_name_raw,
                        "csv_description_as_title": description_as_title,
                        "csv_quantity": quantity,
                        "csv_price": price,
                        "csv_folder_name": folder_name_csv,
                        "status": status,  # Added status field
                        "original_csv_row": i + 2
                    })
            else:
                problematic_csv_rows.append(f"Row {i+2}: Mismatched number of columns. Expected {len(csv_header)}, got {len(row)}. Data: {row}")

except FileNotFoundError:
    with open(output_mapping_report_path, 'w', encoding='utf-8') as r_file:
        r_file.write(f"Erro Crítico: Arquivo CSV não encontrado em {csv_file_path}\n")
    print(f"CRITICAL ERROR: CSV file not found. Report: {output_mapping_report_path}")
    exit()
except ValueError as ve:
    with open(output_mapping_report_path, 'w', encoding='utf-8') as r_file:
        r_file.write(f"Erro Crítico ao processar CSV: {str(ve)}\n")
        if csv_header:
             r_file.write(f"Cabeçalho encontrado: {csv_header}\n")
    print(f"CRITICAL ERROR processing CSV: {str(ve)}. Report: {output_mapping_report_path}")
    exit()
except Exception as e:
    with open(output_mapping_report_path, 'w', encoding='utf-8') as r_file:
        r_file.write(f"Erro Crítico inesperado ao ler CSV: {str(e)}\n")
    print(f"CRITICAL UNEXPECTED ERROR reading CSV: {str(e)}. Report: {output_mapping_report_path}")
    exit()

# --- 2. List Actual Folders in ZIP Extraction Directory ---
actual_folders_in_zip = []
if os.path.exists(zip_extracted_base_dir):
    for item_name_zip in os.listdir(zip_extracted_base_dir):
        if os.path.isdir(os.path.join(zip_extracted_base_dir, item_name_zip)) and item_name_zip != "__MACOSX" and not item_name_zip.startswith("."):
            actual_folders_in_zip.append(sanitize_folder_name(item_name_zip))
else:
    with open(output_mapping_report_path, 'w', encoding='utf-8') as r_file:
        r_file.write(f"Erro Crítico: Diretório de itens descompactados não encontrado em {zip_extracted_base_dir}\n")
    print(f"CRITICAL ERROR: ZIP extraction directory not found. Report: {output_mapping_report_path}")
    exit()

# --- 3. Map CSV Items to Actual Folders & Generate Report ---
valid_mapped_items = []
csv_items_not_in_zip = []
zip_folders_not_in_csv = list(actual_folders_in_zip)

for csv_item in csv_items:
    folder_name_from_csv = csv_item["csv_folder_name"]
    if folder_name_from_csv in actual_folders_in_zip:
        valid_mapped_items.append({
            "id": folder_name_from_csv,
            "title_pt": csv_item["csv_description_as_title"],
            "csv_item_name_original": csv_item["csv_item_name"],
            "description_pt_raw_csv": csv_item["csv_description_as_title"],
            "quantity": csv_item["csv_quantity"],
            "price": csv_item["csv_price"],
            "folder_name": folder_name_from_csv,
            "status": csv_item["status"], # Pass status along
            "original_csv_row": csv_item["original_csv_row"]
        })
        if folder_name_from_csv in zip_folders_not_in_csv:
            zip_folders_not_in_csv.remove(folder_name_from_csv)
    else:
        csv_items_not_in_zip.append(csv_item)

# --- 4. Save Processed Data and Report ---
with open(output_processed_data_path, 'w', encoding='utf-8') as outfile:
    json.dump(valid_mapped_items, outfile, indent=4, ensure_ascii=False)

with open(output_mapping_report_path, 'w', encoding='utf-8') as r_file:
    r_file.write('Relatório de Mapeamento CSV vs Pastas ZIP (Com Status de Reserva)\n')
    r_file.write('==================================================================\n\n')
    r_file.write(f"Itens a serem excluídos (conforme solicitado): {items_to_exclude_csv_pasta_name}\n")
    r_file.write(f"Item marcado como RESERVADO (título PT): {item_to_mark_reserved_title_pt}\n\n")
    total_initial_csv_items = 0
    try:
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as temp_infile:
            temp_reader = csv.reader(temp_infile, delimiter=';')
            next(temp_reader) # skip header
            total_initial_csv_items = sum(1 for row in temp_reader)
    except:
        total_initial_csv_items = len(csv_items) + len(items_to_exclude_csv_pasta_name) + len(csv_items_not_in_zip) # Fallback

    r_file.write(f"Total de itens no CSV (original): {total_initial_csv_items}\n")
    r_file.write(f"Total de itens no CSV considerados para mapeamento (após exclusões iniciais): {len(csv_items)}\n")
    r_file.write(f"Total de pastas encontradas no diretório ZIP (relevantes): {len(actual_folders_in_zip)}\n\n")
    r_file.write(f"Total de itens VALIDADOS e MAPEADOS com sucesso: {len(valid_mapped_items)}\n\n")

    if problematic_csv_rows:
        r_file.write('Linhas problemáticas no CSV (com dados padrão ou ignoradas na contagem inicial de mapeamento):\n')
        for problem in problematic_csv_rows:
            r_file.write(f"- {problem}\n")
        r_file.write('\n')

    if csv_items_not_in_zip:
        r_file.write('Itens listados no CSV (e não excluídos), mas SEM PASTA CORRESPONDENTE no ZIP:\n')
        for item in csv_items_not_in_zip:
            r_file.write(f"- Item: '{item['csv_description_as_title']}' (Pasta CSV: '{item['csv_folder_name']}', Linha CSV: {item['original_csv_row']})\n")
        r_file.write('\n')
    
    if zip_folders_not_in_csv:
        r_file.write('Pastas encontradas no ZIP, mas SEM ITEM CORRESPONDENTE no CSV (ou item foi excluído):\n')
        for folder_name in zip_folders_not_in_csv:
            r_file.write(f"- {folder_name}\n")
        r_file.write('\n')

    r_file.write('Dados processados dos itens mapeados foram salvos em: ' + output_processed_data_path + '\n')
    r_file.write('==================================================================\n')
    r_file.write('Fim do Relatório de Mapeamento.\n')

print(f"Processamento CSV e mapeamento (com status de reserva) concluídos. Dados salvos em {output_processed_data_path}. Relatório em {output_mapping_report_path}")

