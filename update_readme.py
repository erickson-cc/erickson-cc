import urllib.request
import re
import sys

USER_ID = "100892536"
# Acedemos ao endereço público visível no browser em vez do RSS desativado
URL = f"https://www.goodreads.com/review/list/{USER_ID}?shelf=currently-reading"

def update_readme():
    try:
        # User-Agent modificado para simular um browser comum e evitar bloqueios básicos
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        response = urllib.request.urlopen(req)
        html_data = response.read().decode('utf-8')

        # Expressões regulares para localizar a célula do título e do autor na tabela HTML
        title_match = re.search(r'<td class="field title".*?<a title="([^"]+)"', html_data, re.IGNORECASE | re.DOTALL)
        author_match = re.search(r'<td class="field author".*?<a.*?>(.*?)</a>', html_data, re.IGNORECASE | re.DOTALL)

        if not title_match or not author_match:
            print("Nenhum livro encontrado ou falha ao ler a estrutura da página.")
            sys.exit(0)

        title = title_match.group(1).strip()
        # Limpa quebras de linha e formatações extra que possam vir no HTML do autor
        author = author_match.group(1).strip().replace('\n', '').replace(' *', '')
        
        reading_text = f"**Currently Reading:** {title}, {author}"

        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        start_marker = "<!-- currently-reading-start -->"
        end_marker = "<!-- currently-reading-end -->"
        pattern = re.compile(rf"({start_marker}).*?({end_marker})", re.DOTALL)
        
        new_content = pattern.sub(rf"\1\n{reading_text}\n\2", content)

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("README atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar o README: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_readme()
