import os
import re
import unicodedata

def normalize_name(name):
    """
    Retira acentos, converte para minúsculas, substitui espaços por sublinhado
    e remove caracteres que não sejam letras, números, sublinhado, hífen ou ponto.
    """
    # Separa nome e extensão (se houver)
    base, ext = os.path.splitext(name)
    # Normaliza: remove acentos e converte para ASCII
    base = (
        unicodedata.normalize('NFKD', base)
        .encode('ASCII', 'ignore')
        .decode('ASCII')
    )
    # Converte para minúsculas
    base = base.lower()
    # Substitui espaços por "_"
    base = base.replace(" ", "_")
    # Remove caracteres indesejados (permitindo letras, números, _ e -)
    base = re.sub(r'[^a-z0-9_\-]', '', base)
    return base + ext.lower()

def collect_renaming_mapping(root_dir):
    """
    Percorre recursivamente o diretório a partir de root_dir.
    Retorna um dicionário mapeando caminhos relativos antigos para novos caminhos relativos.
    """
    renaming_map = {}
    # Usar topdown=False para renomear primeiro arquivos e depois diretórios
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        # Renomear arquivos
        for filename in files:
            new_filename = normalize_name(filename)
            if new_filename != filename:
                old_path = os.path.join(current_root, filename)
                new_path = os.path.join(current_root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    rel_old = os.path.relpath(old_path, root_dir).replace(os.sep, '/')
                    rel_new = os.path.relpath(new_path, root_dir).replace(os.sep, '/')
                    renaming_map[rel_old] = rel_new
                    print(f"Arquivo renomeado: {rel_old} -> {rel_new}")
                except Exception as e:
                    print(f"Erro ao renomear o arquivo {old_path}: {e}")
        # Renomear diretórios
        for dirname in dirs:
            new_dirname = normalize_name(dirname)
            if new_dirname != dirname:
                old_dir = os.path.join(current_root, dirname)
                new_dir = os.path.join(current_root, new_dirname)
                try:
                    os.rename(old_dir, new_dir)
                    rel_old = os.path.relpath(old_dir, root_dir).replace(os.sep, '/')
                    rel_new = os.path.relpath(new_dir, root_dir).replace(os.sep, '/')
                    renaming_map[rel_old] = rel_new
                    print(f"Pasta renomeada: {rel_old} -> {rel_new}")
                except Exception as e:
                    print(f"Erro ao renomear a pasta {old_dir}: {e}")
    return renaming_map

def update_html_files(root_dir, renaming_map):
    """
    Para cada arquivo HTML encontrado sob root_dir, atualiza links e referências
    substituindo os caminhos antigos pelos novos conforme renaming_map.
    """
    # Ordenar as chaves por tamanho decrescente para evitar substituições parciais
    sorted_keys = sorted(renaming_map.keys(), key=len, reverse=True)
    for current_root, _, files in os.walk(root_dir):
        for filename in files:
            if filename.lower().endswith('.html'):
                file_path = os.path.join(current_root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    updated = content
                    for old, new in renaming_map.items():
                        # Substitui ocorrências dos caminhos antigos (no formato unix com "/")
                        updated = updated.replace(old, new)
                    if updated != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated)
                        rel_file = os.path.relpath(file_path, root_dir).replace(os.sep, '/')
                        print(f"Arquivo HTML atualizado: {rel_file}")
                except Exception as e:
                    print(f"Erro ao atualizar o arquivo {file_path}: {e}")

if __name__ == "__main__":
    # Defina o diretório raiz do seu projeto
    root_directory = os.getcwd()  # ou especifique o caminho absoluto

    print("Iniciando a normalização de nomes...")
    mapping = collect_renaming_mapping(root_directory)
    
    if mapping:
        print("\nAtualizando arquivos HTML...")
        update_html_files(root_directory, mapping)
        print("\nProcesso concluído!")
    else:
        print("Nenhuma renomeação necessária.")