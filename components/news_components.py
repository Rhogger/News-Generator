import streamlit as st


def news_input_form():
    return st.text_area("Forneça um contexto para a geração da notícia:")


def news_output(result: dict):
    st.subheader("Notícia Gerada")
    # Verifique se 'outputs' existe
    if result.get("outputs"):
        # Verifique se o primeiro item da lista 'outputs' existe e contém a chave 'outputs'
        output_item = result["outputs"][0].get("outputs")

        if output_item and len(output_item) > 0:
            # Acessando os dados internos do primeiro objeto 'results'
            results = output_item[0].get("results")

            if results:
                message = results.get("message")

                if message:
                    # Aqui acessa o 'text' dentro de 'message'
                    text_data = message.get("text")

                    if text_data:
                        # Remover as barras invertidas
                        text_data_cleaned = text_data.replace('\\', '')

                        print(
                            "----------------------------------------------------------", text_data_cleaned)

                        # Como o campo 'text' parece ser um JSON stringificado, precisamos desserializar
                        import json
                        try:
                            text_content = json.loads(text_data_cleaned)
                            # Agora você pode acessar os campos dentro do objeto 'text', como title, description, etc.
                            title = text_content.get(
                                "title", "Título não encontrado")
                            description = text_content.get(
                                "description", "Descrição não encontrada")
                            sinopse = text_content.get(
                                "sinopse", "Sinopse não encontrada")
                            keywords = text_content.get(
                                "key-words", "Palavras chaves não geradas")
                            image = text_content.get(
                                "image-url", None
                            )

                            # Exibindo no Streamlit
                            st.write(f"Título: {title}")
                            st.write(f"Descrição: {description}")
                            st.write(f"Sinopse: {sinopse}")

                            if len(keywords) >= 5:
                                st.write(
                                    f"Palavras-chaves: {keywords[0]}, {keywords[1]}, {keywords[2]}, {keywords[3]}, {keywords[4]}")
                            else:
                                st.write(
                                    f"Palavras-chaves: {', '.join(keywords)}")

                            # Exibir a imagem se disponível
                            if image != "Imagem não gerada":
                                st.image(image)
                            else:
                                st.write("Imagem não disponível")
                        except json.JSONDecodeError:
                            st.write(
                                "Erro ao decodificar o JSON contido no campo 'text'.")
                    else:
                        st.write("Campo 'text' não encontrado.")
    else:
        st.write("Houve uma falha no servidor. Tente novamente")


def submit_button(label: str):
    return st.button(label)
