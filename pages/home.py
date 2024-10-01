import streamlit as st
from api.flow_api import run_flow
from components.news_components import news_input_form, news_output, submit_button

# Página principal


def home_page():
    st.title("Gerador de Notícias com IA")

    context = news_input_form()

    if submit_button("Gerar Notícia"):
        with st.spinner("Gerando notícia..."):
            if context:
                # Executa a requisição para gerar a notícia
                response = run_flow(message=context)

                # Substitui o conteúdo com a notícia gerada
                display_news(response)
            else:
                st.error("Por favor, forneça um contexto válido.")

# Função para exibir o formulário de input


def news_input_form():
    return st.text_area("Forneça um contexto para a geração da notícia:")

# Função para exibir a notícia gerada


def display_news(result: dict):
    st.subheader("Notícia Gerada")

    if result.get("outputs"):
        output_item = result["outputs"][0].get("outputs")

        if output_item and len(output_item) > 0:
            results = output_item[0].get("results")

            if results:
                message = results.get("message")

                if message:
                    text_data = message.get("text")

                    if text_data:
                        import json
                        try:
                            # Parse JSON
                            text_content = json.loads(text_data)

                            title = text_content.get(
                                "title", "Título não encontrado")
                            description = text_content.get(
                                "description", "Descrição não encontrada")
                            sinopse = text_content.get(
                                "sinopse", "Sinopse não encontrada")
                            keywords = text_content.get(
                                "key-words", "Palavras chaves não geradas")
                            image = text_content.get("image-url", None)

                            # Layout customizado - Imagem no topo
                            if image:
                                # Define a imagem no topo, como header
                                st.image(image, use_column_width=True)

                            # Exibe o conteúdo da notícia
                            # Exibe o título grande logo após a imagem
                            st.title(title)
                            st.write(f"**Descrição:** {description}")
                            st.write(f"**Sinopse:** {sinopse}")

                            if len(keywords) >= 5:
                                st.write(
                                    f"**Palavras-chaves:** {', '.join(keywords)}")
                            else:
                                st.write(
                                    f"**Palavras-chaves:** {', '.join(keywords)}")
                        except json.JSONDecodeError:
                            st.write(
                                "Erro ao decodificar o JSON contido no campo 'text'.")
                    else:
                        st.write("Campo 'text' não encontrado.")
    else:
        st.write("Houve uma falha no servidor. Tente novamente")

# Função para exibir o botão de submissão


def submit_button(label: str):
    return st.button(label)
