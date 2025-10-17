import requests
import time
import os

MANIFEST_URL = "http://127.0.0.1:5000/manifest.mpd"

def baixar_manifesto():
    """
    Função 1: Fazer uma requisição GET ao manifesto
    - Obter o JSON com as representações de vídeo
    - Retornar o dicionário com as informações do manifesto
    """
    url = "http://127.0.0.1:5000/manifest.mpd"
    response = requests.get(url)

    if response.status_code == 200:
        manifesto = response.json()
        return manifesto
    else:
        print(f"Erro ao baixar manifesto: {response.status_code}")
        return None

def medir_largura_de_banda(url_arquivo_externo):
    """
    Função 2: Medir a largura de banda
    - Baixar um arquivo de url externo como base
    - Medir o tempo da transferência
    - Calcular a largura de banda em Mbps: (tamanho_bytes * 8) / (tempo * 1_000_000)
    - Retornar a largura de banda medida
    """
    nome_arquivo = "teste_externo.tmp"

    inicio = time.time()
    response = requests.get(url_arquivo_externo, stream=True)

    with open(nome_arquivo, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    fim = time.time()

    tamanho_bytes = os.path.getsize(nome_arquivo)
    tempo = fim - inicio

    largura_banda_mbps = (tamanho_bytes * 8) / (tempo * 1000000)
    print(f"Tamanho do arquivo: {tamanho_bytes} bytes")
    print(f"Tempo de download: {tempo:.2f} segundos")
    print(f"Largura de banda estimada: {largura_banda_mbps:.2f} Mbps")

    os.remove(nome_arquivo)
    return largura_banda_mbps

def selecionar_qualidade(manifesto, largura_banda_mbps):
    """
    Função 3: Escolher a melhor representação
    - Percorrer as representações disponíveis no manifesto
    - Comparar a largura de banda exigida por cada uma com a medida
    - Retornar a melhor representação suportada
    """
    representacoes = manifesto["video"]["representations"]

    # Ordena do menor para o maior bandwidth (kbps)
    representacoes_ordenadas = sorted(representacoes, key=lambda r: r["bandwidth"])

    qualidade = representacoes_ordenadas[0]

    for rep in representacoes_ordenadas:
        # Converte largura_banda_mbps para kbps para comparação
        if rep["bandwidth"] <= largura_banda_mbps * 1000:
            qualidade = rep

    print(f"Qualidade escolhida: {qualidade['id']} ({qualidade['bandwidth']} kbps)")
    return qualidade

def baixar_video(representacao):
    """
    Função 4: Baixar o segmento de vídeo escolhido
    - Fazer uma requisição GET para a URL da representação escolhida
    - Salvar o conteúdo em um arquivo local (ex: video_720p.mp4)
    """
    url = representacao["url"]
    qualidade = representacao["id"]
    nome_arquivo = f"video_{qualidade}.mp4"

    print(f"Baixando segmento em {qualidade} de {url}")

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(nome_arquivo, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Segmento salvo como {nome_arquivo}")
        return nome_arquivo
    else:
        print(f"Erro ao baixar segmento: {response.status_code}")
        return None

def main():
    """
     Função principal:
    - Chamar as funções na ordem correta
    - Exibir os dados na tela
    - Salvar o vídeo com a qualidade selecionada
    """
    # Baixando o manifesto
    manifesto = baixar_manifesto()
    if manifesto is None:
        return

    # Medindo a largura de banda usando arquivo externo de 100MB
    url_teste = "https://www.estado.rs.gov.br"
    largura_banda = medir_largura_de_banda(url_teste)

    # Selecionando a melhor qualidade com base na largura de banda
    representacao_escolhida = selecionar_qualidade(manifesto, largura_banda)

    # Baixando o vídeo da qualidade escolhida
    baixar_video(representacao_escolhida)

if __name__ == '__main__':
    main()
