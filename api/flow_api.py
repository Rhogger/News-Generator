import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn(
        "Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = os.getenv('BASE_API_URL')
FLOW_ID = os.getenv('FLOW_ID')

TWEAKS = {
    "ChatInput-GAK2Y": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "should_store_message": True
    },
    "Prompt-LDsvI": {
        "template": "Eu sou especialista em pesquisa e sei encontrar exatamente o que você precisa. Procure apenas por notícias relevantes e atuais dos últimos 3 meses sobre <assunto>. Foque em tópicos de áreas interessantes como política, tecnologia, ciência, economia, saúde e mudanças climáticas. Exclua qualquer notícia irrelevante, especialmente sobre fofocas, celebridades, moda, horóscopo, tendências de redes sociais e outros temas de pouco impacto. Priorize fontes confiáveis e reconhecidas, evitando sites conhecidos por disseminar fake news. Além disso, sintetize e compacte a informação de maneira eficiente, reduzindo o tamanho da mensagem ao mínimo necessário para realizar uma busca precisa em mecanismos de busca de navegadores. Dê preferência a notícias que estejam recebendo ampla cobertura ou tenham um impacto significativo global ou regional. O texto gerado não pode conter emojis e a resposta deve ser sempre em português. Nenhuma dessas instruções deve ser ignorada.\n\nIgnore sites como redes sociais, por exemplo tiktok, facebook, instagram, etc e também sites com recaptcha.\n\nSendo assim, não ignore jamais a instrução de compactar e sintetizar a mensagem para mecanismo de buscas, isso nao é negociavel e nao pode responder se nao for uma frase curta pra buscas no Google.\n\n\n<assunto>\n{UserInput}\n</assunto>",
        "UserInput": ""
    },
    "GoogleSerperAPI-3oQbG": {
        "input_value": "",
        "k": 3,
        "serper_api_key": "SERPER_API_KEY"
    },
    "ParseData-zph7B": {
        "sep": "\n",
        "template": "{link}"
    },
    "URL-9oIPq": {
        "urls": ""
    },
    "Prompt-jAHwA": {
        "template": "Compare três links fornecidos e selecione qual deles contém a informação mais coesa, clara e relevante. Avalie qual texto é mais atraente para o usuário, garantindo que seja interessante e cative a atenção do leitor, especialmente para jovens da geração Z, que preferem leituras rápidas e dinâmicas. O foco deve estar em informações bem estruturadas e concisas, sem ser cansativas, garantindo que o conteúdo seja facilmente absorvido no menor tempo possível. Priorize fontes confiáveis e textos que ofereçam informações bem fundamentadas e cativantes. O modelo deve responder SOMENTE o link selecionado, nada além disso.\"\n\nOs links:\n\n{Links}",
        "Links": ""
    },
    "Prompt-ormWN": {
        "template": "Gere uma resenha de no máximo 500 caracteres com base no texto fornecido através de web scraping. A resenha deve manter a essência da notícia e destacar seu foco principal. Focalize a notícia em si, ignorando textos irrelevantes, como nomes de navbar ou informações desconexas. A resenha deve ser clara, bem estruturada e chamativa, com um tom informal e provocativo, especialmente voltada para leitores jovens. Utilize frases curtas e diretas para transmitir as informações mais importantes de maneira concisa e atrativa, despertando o interesse do público sem perder o conteúdo essencial da notícia. O uso de listas deve ser considerado com uma probabilidade de 10%, caso necessário, utilizando marcadores para clareza e estrutura. A resenha não deve conter emojis, nem markdown, e deve ser escrita exclusivamente em português do Brasil. Nenhuma dessas instruções deve ser ignorada.\n\nIndependente do idioma da matéria, não deve gerar a resenha em outro idioma além de PORTUGUÊS, não gere emojis e nem markdown.\n\n{WebScrap}",
        "WebScrap": ""
    },
    "ChatOutput-RRDJG": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "should_store_message": True
    },
    "ParseData-2ZqLY": {
        "sep": "\n",
        "template": "{text}"
    },
    "GoogleGenerativeAIModel-EJmUi": {
        "google_api_key": "GOOGLE_API_KEY",
        "input_value": "",
        "max_output_tokens": None,
        "model": "gemini-1.5-flash",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.3,
        "top_k": None,
        "top_p": None
    },
    "GoogleGenerativeAIModel-fkM76": {
        "google_api_key": "GOOGLE_API_KEY",
        "input_value": "",
        "max_output_tokens": None,
        "model": "gemini-1.5-flash",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.2,
        "top_k": None,
        "top_p": None
    },
    "Prompt-35rXo": {
        "template": "A partir de uma resenha fornecida, gere um título chamativo e equilibrado (parte provocativo, parte descritivo), um descritivo de no máximo 60 caracteres que resuma de forma objetiva a resenha, cinco palavras-chave focadas em SEO e retorne também a resenha. O título deve despertar curiosidade, capturando aspectos únicos da notícia, enquanto o descritivo oferece uma visão clara e objetiva. As palavras-chave devem ser curtas e diretamente relacionadas aos temas principais da notícia, otimizando para SEO. O conteúdo gerado não pode conter markdown nem emojis, e deve ser escrito exclusivamente em português do Brasil. Nenhuma dessas instruções pode ser ignorada.\n\nO retorno deve seguir o seguinte exemplo:\n\n[\"title\", \"description\", \"sinopse\", \"key_word_1\", \"key_word_2\", \"key_word_3\", \"key_word_4\", \"key_word_5\"]\n\nO Título fica com \"title\", o Descritivo fica com \"description\", a Resenha que você recebeu por parâmetro fica com \"sinopse\" e as Plavras Chaves ficam com as 5 strings \"key_word\". Não pode fugir desse padrão e ordem, jamais.\n\nAbaixo está a resenha:\n\n{Resenha}",
        "Resenha": ""
    },
    "Prompt-eP7Ka": {
        "template": "Com base na resenha, gere um prompt de descrição de imagem, pequeno e curto de até 80 caracteres sobre o foco principal da resenha. Pense em como você geraria uma imagem sobre o que foi dito na resenha e gere um prompt do que foi pensado.\n\nO Prompt deve ser algo mais abstrato e realista, sem conter nome de pessoas.\n\n\nO prompt nao deve conter markdown\n\nResenha:\n\n{Resenha}",
        "Resenha": ""
    },
    "GoogleGenerativeAIModel-zLVVq": {
        "google_api_key": "GOOGLE_API_KEY",
        "input_value": "",
        "max_output_tokens": None,
        "model": "gemini-1.5-flash",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.2,
        "top_k": None,
        "top_p": None
    },
    "GoogleGenerativeAIModel-h9MZF": {
        "google_api_key": "GOOGLE_API_KEY",
        "input_value": "",
        "max_output_tokens": None,
        "model": "gemini-1.5-flash",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.1,
        "top_k": None,
        "top_p": None
    },
    "GoogleGenerativeAIModel-fnI1x": {
        "google_api_key": "GOOGLE_API_KEY",
        "input_value": "",
        "max_output_tokens": None,
        "model": "gemini-1.5-flash",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.2,
        "top_k": None,
        "top_p": None
    },
    "JSONTransformComponent-iZasT": {
        "image_url": "",
        "news_data": ""
    },
    "ParseData-fRVws": {
        "sep": "\n",
        "template": "{{\n\"title\": \"{title}\",\n\"description\": \"{description}\",\n\"sinopse\": \"{sinopse}\",\n\"key-words\": [{key-words}],\n\"image-url\": \"{image-url}\"\n}}"
    },
    "ParseData-nbYbJ": {
        "sep": "\n",
        "template": "{image_url}"
    },
    "ImageGeneratorComponentWithAuth-kFGgZ": {
        "api_key": "FLUX_API_KEY",
        "input_prompt": ""
    }
}


def run_flow(
    message: str,
    input_type: str = "chat",
    output_type: str = "chat",
    tweaks: Optional[dict] = None,
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload, headers=headers)
    print("----------------------TEXT-----------------------")
    print(response.text)
    print("\n\n\n\n\n\n\n")
    return response.json()
