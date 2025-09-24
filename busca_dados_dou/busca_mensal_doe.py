import requests
import PyPDF2
from io import BytesIO
from calendar import monthrange

def search_name_in_monthly_pdfs(year, month, name_to_find):
    """
    Gera URLs para todos os dias de um mês/ano específico, tratando a
    sensibilidade a maiúsculas/minúsculas dos nomes de arquivo, e busca por um nome.
    """
    found_in_pdfs = []
    
    # URL base para o mês e ano
    base_url = f"https://diof.ro.gov.br/data/uploads/{year}/{month:02}/"
    print(f"Preparando para buscar PDFs para o mês {month:02}/{year}...\n")
    print(f"URL base de pesquisa: {base_url}")

    num_days = monthrange(year, month)[1]

    for day in range(1, num_days + 1):
        day_str = f"{day:02}"
        month_str = f"{month:02}"
        
        # Nomes de arquivo a serem testados
        filenames_to_try = [
            f"DOE-{day_str}.{month_str}.{year}.pdf",
            f"DOE-{day_str}-{month_str}-{year}.pdf",
            f"Doe-{day_str}-{month_str}-{year}.pdf",
            f"Doe.{day_str}.{month_str}.{year}.pdf",
            f"SUPLEMENTAR-{day_str}-{month_str}-{year}.pdf",
            f"DOE-SUPLEMENTAR-02-{day_str}-{month_str}-{year}.pdf",
            f"DOE-SUPLEMENTAR-{day_str}-{month_str}-{year}.pdf",
            f"Doe-Suplementar-{day_str}-{month_str}-{year}.pdf"
        ]

        found_for_day = False
        
        for filename in filenames_to_try:
            pdf_url = base_url + filename
            print(f"  -> Tentando {pdf_url}...")
            
            try:
                response = requests.get(pdf_url, stream=True)
                
                if response.status_code == 200:
                    found_for_day = True # Marca que uma publicação foi encontrada para o dia
                    
                    pdf_file_obj = BytesIO(response.content)
                    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                    
                    name_found_in_pdf = False
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text and name_to_find.lower() in text.lower():
                            found_in_pdfs.append(pdf_url)
                            print(f"  [SUCESSO] Nome encontrado no PDF: {pdf_url}")
                            name_found_in_pdf = True
                            break
                    
                    if not name_found_in_pdf:
                        print("  [INFO] Nome não encontrado neste PDF.")
                        
                    break  # Sai do loop de filenames, pois uma URL válida foi encontrada
                
                elif response.status_code == 404:
                    continue  # Continua para a próxima opção de nome de arquivo
                
                else:
                    print(f"  [ERRO] Ocorreu um erro inesperado: {response.status_code}")
                    found_for_day = True # Impede a mensagem de "não houve publicação"
                    break

            except Exception as e:
                print(f"  [ERRO] Não foi possível processar o PDF em {pdf_url}: {e}")
                found_for_day = True
                break
        
        if not found_for_day:
            print(f"  [INFO] Não houve publicação no diário para o dia {day_str}/{month_str}/{year}.")

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
name_to_find = "joabe zeferino dos santos"

# Executar a função
search_name_in_monthly_pdfs(year_to_search, month_to_search, name_to_find)