import urllib.request
import xml.etree.ElementTree as ET
import re
import sys

# Substitua pelo seu ID numérico do Goodreads
USER_ID = "100892536"
RSS_URL = f"https://www.goodreads.com/review/list_rss/{USER_ID}?shelf=currently-reading"

def update_readme():
    try:
        # Faz a requisição ao RSS do Goodreads
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        # Busca o primeiro item do feed (livro mais recente adicionado à prateleira)
        item = root.find('./channel/item')
        if item is None:
            print("Nenhum livro na prateleira 'Currently Reading'.")
            sys.exit(0)

        title = item.find('title').text
        author = item.find('author_name').text

        # Formata a string exatamente como você pediu
        reading_text = f"**Currently Reading:** {title}, {author}"

        # Lê o README atual
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex para substituir o texto entre as tags
        start_marker = "<!-- currently-reading-start -->"
        end_marker = "<!-- currently-reading-end -->"
        pattern = re.compile(rf"({start_marker}).*?({end_marker})", re.DOTALL)
        
        # Insere o novo texto formatado
        new_content = pattern.sub(rf"\1\n{reading_text}\n\2", content)

        # Salva o arquivo modificado
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("README atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar o README: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_readme()
