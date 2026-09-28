import streamlit as st
from supabase import create_client, Client
import uuid

# Configuração da página
st.set_page_config(page_title="Ateliê Mimos e Artes", page_icon="🧶", layout="wide")

# Conexão segura com o Supabase usando os Secrets do Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Erro ao conectar ao banco de dados Supabase. Verifique os Secrets no Streamlit.")

# Inicializar lista de produtos padrão na sessão se ainda não existir
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {
            "id": 1,
            "nome": "Bolsa Devoção Nossa Senhora",
            "categoria": "Bolsas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Pronta Entrega",
            "descricao": "Bolsa bordada com detalhes em pérolas e alça reforçada.",
            "imagens": []
        },
        {
            "id": 2,
            "nome": "Naninha Oração Santo Anjo",
            "categoria": "Naninhas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Sob Encomenda",
            "descricao": "Naninha macia em tecido antialérgico com a oração do Santo Anjo.",
            "imagens": []
        }
    ]

# Função para fazer upload da foto para o Supabase Storage
def upload_foto_supabase(file_obj):
    try:
        # Gera um nome único para o arquivo evitar sobreposição
        file_ext = file_obj.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_bytes = file_obj.read()
        
        # Envia para o bucket 'fotos-produtos'
        res = supabase.storage.from_("fotos-produtos").upload(
            file_name, 
            file_bytes, 
            {"content-type": file_obj.type}
        )
        
        # Obtém a URL pública e permanente da imagem
        public_url = supabase.storage.from_("fotos-produtos").get_public_url(file_name)
        return public_url
    except Exception as e:
        st.error(f"Erro ao enviar foto: {e}")
        return None

# NAVEGAÇÃO LATERAL
st.sidebar.title("📌 Navegação")
modo = st.sidebar.radio("Ir para:", ["🛍️ Catálogo de Produtos", "⚙️ Painel de Gestão (Restrito)"])

# ==========================================
# MODO 1: CATÁLOGO PÚBLICO
# ==========================================
if modo == "🛍️ Catálogo de Produtos":
    st.title("🧶 Ateliê Mimos e Artes")
    st.caption("Catálogo virtual de peças artesanais exclusivas")
    st.divider()

    # Exibição dos produtos
    for prod in st.session_state.produtos:
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            if prod["imagens"]:
                st.image(prod["imagens"][0], use_container_width=True)
            else:
                st.info("🖼️ Sem foto disponível")
                
        with col_info:
            st.subheader(prod["nome"])
            st.write(f"**Categoria:** {prod['categoria']} | **Tema:** {prod['tema']}")
            st.write(f"**Status:** {prod['status']}")
            st.write(prod["descricao"])
            
            # Galeria extra se houver mais fotos
            if len(prod["imagens"]) > 1:
                with st.expander("Ver mais fotos"):
                    sub_cols = st.columns(len(prod["imagens"]) - 1)
                    for idx, img_url in enumerate(prod["imagens"][1:]):
                        sub_cols[idx].image(img_url, use_container_width=True)
                        
            msg_wa = f"Olá Sil! Gostei muito da peça '{prod['nome']}' e gostaria de saber mais informações!"
            link_wa = f"https://wa.me/5518991234567?text={msg_wa.replace(' ', '%20')}"
            st.markdown(f"[💬 Encomendar pelo WhatsApp]({link_wa})")
        st.divider()

# ==========================================
# MODO 2: PAINEL DE GESTÃO (ÁREA RESTRITA)
# ==========================================
else:
    st.title("⚙️ Painel de Gestão do Ateliê")
    senha = st.text_input("🔐 Digite a senha para acessar:", type="password")
    
    if senha == "sil123":
        st.success("Acesso autorizado!")
        st.divider()
        
        opcoes_produtos = {p["nome"]: p for p in st.session_state.produtos}
        
        def ao_mudar_produto():
            st.session_state.uploader_key = st.session_state.get("uploader_key", 0) + 1

        prod_selecionado_nome = st.selectbox(
            "Escolha qual produto deseja alterar:", 
            list(opcoes_produtos.keys()),
            on_change=ao_mudar_produto
        )
        prod_obj = opcoes_produtos[prod_selecionado_nome]

        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0

        # GERENCIAR FOTOS ATUAIS
        st.markdown("### 🖼️ Fotos Atuais do Produto")
        fotos_atuais = prod_obj.get("imagens", [])

        if not fotos_atuais:
            st.info("Nenhuma foto cadastrada para este produto.")
        else:
            cols_fotos = st.columns(min(len(fotos_atuais), 4))
            for f_idx, foto_url in enumerate(fotos_atuais):
                with cols_fotos[f_idx % 4]:
                    st.image(foto_url, use_container_width=True)
                    if st.button(f"🗑️ Excluir", key=f"del_{prod_obj['id']}_{f_idx}"):
                        prod_obj["imagens"].pop(f_idx)
                        st.toast("Foto removida!", icon="✅")
                        st.rerun()

        st.divider()

        # FORMULÁRIO DE EDIÇÃO E UPLOAD
        with st.form("form_edicao"):
            st.markdown("### ✏️ Alterar Informações")
            novo_nome = st.text_input("Nome:", value=prod_obj["nome"])
            nova_categoria = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"], index=["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"].index(prod_obj["categoria"]))
            novo_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"], index=["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"].index(prod_obj["tema"]))
            novo_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"], index=["Pronta Entrega", "Sob Encomenda"].index(prod_obj["status"]))
            nova_descricao = st.text_area("Descrição:", value=prod_obj["descricao"])
            
            st.markdown("➕ **Adicionar Novas Fotos (Permanentes na Nuvem):**")
            novas_fotos_upload = st.file_uploader(
                "Selecione as fotos do celular ou computador", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True,
                key=f"uploader_{st.session_state.uploader_key}"
            )
            
            btn_salvar = st.form_submit_button("💾 Salvar Alterações")
            
            if btn_salvar:
                prod_obj["nome"] = novo_nome
                prod_obj["categoria"] = nova_categoria
                prod_obj["tema"] = novo_tema
                prod_obj["status"] = novo_status
                prod_obj["descricao"] = nova_descricao
                
                # Upload direto para o Supabase
                if novas_fotos_upload:
                    with st.spinner("Enviando fotos para a nuvem..."):
                        for arq in novas_fotos_upload:
                            url_publica = upload_foto_supabase(arq)
                            if url_publica:
                                prod_obj["imagens"].append(url_publica)
                
                st.session_state.uploader_key += 1
                st.success("✅ Produto atualizado e fotos salvas com sucesso na nuvem!")
                st.rerun()

    elif senha != "":
        st.error("Senha incorreta!")

    elif senha != "":
        st.error("Senha incorreta! Tente novamente.")
