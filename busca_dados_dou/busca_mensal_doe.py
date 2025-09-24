import requests
import PyPDF2
from io import BytesIO
from datetime import date
from calendar import monthrange

def search_name_in_monthly_pdfs(year, month, name_to_find):
    """
    Gera URLs para todos os dias de um mês/ano específico e busca por um nome
    em arquivos DOE e DOE Suplementar.

    Args:
        year (int): O ano dos arquivos.
        month (int): O mês dos arquivos (1-12).
        name_to_find (str): O nome a ser pesquisado.
    """
    found_in_pdfs = []
    
    # URL base para o mês e ano
    base_url = f"https://diof.ro.gov.br/data/uploads/{year}/{month:02}/"
    print(f"Preparando para buscar PDFs para o mês {month:02}/{year}...\n")
    print(f"URL base de pesquisa: {base_url}")

    # Obter o número de dias no mês
    num_days = monthrange(year, month)[1]

    # Iterar por cada dia do mês
    for day in range(1, num_days + 1):
        day_str = f"{day:02}"
        month_str = f"{month:02}"
        
        # Gerar os dois tipos de nomes de arquivo
        filenames = [
            f"DOE-{day_str}-{month_str}-{year}.pdf",
            f"DOE-SUPLEMENTAR-{day_str}-{month_str}-{year}.pdf"
        ]

        # Iterar sobre os dois tipos de arquivo por dia
        for filename in filenames:
            pdf_url = base_url + filename
            print(f"  -> Verificando {pdf_url}...")
            
            try:
                # Baixar o conteúdo do PDF
                pdf_response = requests.get(pdf_url, stream=True)
                
                # Acessar a URL apenas se o arquivo existir (status 200)
                if pdf_response.status_code == 200:
                    # Ler o PDF a partir da memória
                    pdf_file_obj = BytesIO(pdf_response.content)
                    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                    
                    # Extrair e pesquisar o texto
                    found = False
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        
                        if name_to_find.lower() in text.lower():
                            found_in_pdfs.append(pdf_url)
                            print(f"  [SUCESSO] Nome encontrado no PDF: {pdf_url}")
                            found = True
                            break # Sai do loop de páginas
                    if not found:
                        print("  [INFO] Nome não encontrado neste PDF.")

                elif pdf_response.status_code == 404:
                    # Imprimir que o arquivo não existe, o que é comum para DOEs suplementares
                    # que não são publicados todos os dias.
                    print("  [INFO] Arquivo não encontrado (Erro 404). Ignorando.")
                else:
                    print(f"  [ERRO] Ocorreu um erro ao baixar o arquivo: {pdf_response.status_code}")
            
            except Exception as e:
                print(f"  [ERRO] Não foi possível processar o PDF em {pdf_url}: {e}")

    # Relatório final
    print("\n" + "="*50)
    print(f"RESUMO DA BUSCA - {month:02}/{year}")
    print("="*50)
    if found_in_pdfs:
        print(f"A expressão '{name_to_find}' foi encontrada nos seguintes arquivos PDF:")
        for pdf in found_in_pdfs:
            print(f"- {pdf}")
    else:
        print(f"A expressão '{name_to_find}' NÃO foi encontrada em nenhum dos arquivos analisados.")

# --- Configuração da busca ---
year_to_search = 2025
month_to_search = 9
name_to_find = "afonso roberto plantes neto"

# Executar a função
search_name_in_monthly_pdfs(year_to_search, month_to_search, name_to_find)