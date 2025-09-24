import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO

def search_name_in_pdfs(base_url, name_to_find):
    """
    Navega em uma URL, encontra links para PDFs, baixa-os e busca por um nome.

    Args:
        base_url (str): A URL base para começar a busca.
        name_to_find (str): O nome a ser pesquisado dentro dos PDFs.
    """
    found_in_pdfs = []
    
    print(f"Buscando PDFs em: {base_url}\n")
    try:
        # 1. Obter o conteúdo da página web
        response = requests.get(base_url)
        response.raise_for_status()  # Lança um erro para requisições HTTP ruins
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Encontrar todos os links na página que terminam com .pdf
        pdf_links = [link.get('href') for link in soup.find_all('a') if link.get('href', '').endswith('.pdf')]
        
        if not pdf_links:
            print("Nenhum link para PDF foi encontrado na página principal.")
            return

        print(f"Encontrados {len(pdf_links)} links para PDFs. Iniciando a busca...")

        # 3. Iterar sobre cada link de PDF
        for link in pdf_links:
            # Construir a URL completa do PDF
            pdf_url = link if link.startswith('http') else base_url.rstrip('/') + '/' + link.lstrip('/')
            
            print(f"  -> Verificando {pdf_url}...")
            
            try:
                # 4. Baixar o conteúdo do PDF
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status()

                # 5. Ler o PDF a partir da memória (sem salvar no disco)
                pdf_file_obj = BytesIO(pdf_response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                
                # 6. Extrair e pesquisar o texto
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if name_to_find.lower() in text.lower():
                        found_in_pdfs.append(pdf_url)
                        print(f"  [SUCESSO] Nome encontrado no PDF: {pdf_url}")
                        break  # Sai do loop de páginas e vai para o próximo PDF

            except Exception as e:
                print(f"  [ERRO] Não foi possível processar o PDF em {pdf_url}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a URL: {e}")

    # 7. Relatório final
    print("\n" + "="*50)
    print("RESUMO DA BUSCA")
    print("="*50)
    if found_in_pdfs:
        print(f"A expressão '{name_to_find}' foi encontrada nos seguintes arquivos PDF:")
        for pdf in found_in_pdfs:
            print(f"- {pdf}")
    else:
        print(f"A expressão '{name_to_find}' NÃO foi encontrada em nenhum PDF analisado.")

# --- Configuração da busca ---
base_url = "https://diof.ro.gov.br/"
name_to_find = "afonso roberto plantes neto"

# Executar a função
search_name_in_pdfs(base_url, name_to_find)