import streamlit as st
from supabase import create_client, Client
import uuid

# Configuração inicial da página
st.set_page_config(
    page_title="Ateliê Mimos e Artes - Catálogo",
    page_icon="🧶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Conexão segura com o Supabase usando os Secrets do Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Erro ao conectar ao banco de dados Supabase. Verifique a chave nos Secrets do Streamlit.")

# Inicializar a lista de produtos padrão na sessão se ainda não existir
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {
            "id": 1,
            "nome": "Bolsa Devoção Nossa Senhora Aparecida",
            "categoria": "Bolsas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Pronta Entrega",
            "descricao": "Bolsa artesanal bordada com imagem de Nossa Senhora Aparecida, acabamento refinado com detalhes em pérolas e alça reforçada.",
            "imagens": []
        },
        {
            "id": 2,
            "nome": "Bolsa Devoção São Francisco de Assis",
            "categoria": "Bolsas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Sob Encomenda",
            "descricao": "Bolsa delicada em tons amadeirados com bordado de São Francisco de Assis.",
            "imagens": []
        },
        {
            "id": 3,
            "nome": "Naninha Oração Santo Anjo do Senhor",
            "categoria": "Naninhas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Pronta Entrega",
            "descricao": "Naninha macia em tecido antialérgico, estampada com a oração do Santo Anjo, ideal para berço e momentos de devoção do bebê.",
            "imagens": []
        },
        {
            "id": 4,
            "nome": "Naninha Homem-Aranha Baby",
            "categoria": "Naninhas",
            "tema": "Tendências e Super-Heróis",
            "status": "Sob Encomenda",
            "descricao": "Naninha aconchegante do Homem-Aranha em versão fofa baby para crianças.",
            "imagens": []
        },
        {
            "id": 5,
            "nome": "Boneca de Pano Princesa Clássica",
            "categoria": "Bonecas de Pano",
            "tema": "Princesas",
            "status": "Pronta Entrega",
            "descricao": "Boneca artesanal com vestido rodado, cabelos de lã e rostinho pintado à mão.",
            "imagens": []
        },
        {
            "id": 6,
            "nome": "Amigurumi Leãozinho Safari",
            "categoria": "Amigurumi",
            "tema": "Safari",
            "status": "Sob Encomenda",
            "descricao": "Bichinho de crochê feito com fio 100% algodão e olhos com trava de segurança.",
            "imagens": []
        }
    ]

# Função para fazer upload da foto para o Supabase Storage
def upload_foto_supabase(file_obj):
    try:
        file_ext = file_obj.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_bytes = file_obj.read()
        
        supabase.storage.from_("fotos-produtos").upload(
            file_name, 
            file_bytes, 
            {"content-type": file_obj.type}
        )
        
        public_url = supabase.storage.from_("fotos-produtos").get_public_url(file_name)
        return public_url
    except Exception as e:
        st.error(f"Erro ao enviar foto para a nuvem: {e}")
        return None

# NAVEGAÇÃO LATERAL
st.sidebar.title("📌 Navegação")
modo = st.sidebar.radio("Ir para:", ["🛍️ Catálogo de Produtos", "⚙️ Painel de Gestão (Restrito)"])

# ==========================================
# MODO 1: CATÁLOGO PÚBLICO
# ==========================================
if modo == "🛍️ Catálogo de Produtos":
    st.title("🧶 Ateliê Mimos e Artes")
    st.caption("Catálogo virtual de peças artesanais exclusivas da Sil")
    st.divider()

    # Filtros e Pesquisa
    col_busca, col_cat, col_tema = st.columns([2, 1, 1])
    with col_busca:
        busca = st.text_input("🔍 Pesquisar peça por nome:", placeholder="Ex: Nossa Senhora, Naninha, Leão...")
    with col_cat:
        cat_filtro = st.selectbox("Filtrar por Categoria:", ["Todas", "Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"])
    with col_tema:
        tema_filtro = st.selectbox("Filtrar por Tema:", ["Todos", "Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"])

    # Aplicação dos filtros
    produtos_filtrados = st.session_state.produtos
    if busca:
        produtos_filtrados = [p for p in produtos_filtrados if busca.lower() in p["nome"].lower() or busca.lower() in p["descricao"].lower()]
    if cat_filtro != "Todas":
        produtos_filtrados = [p for p in produtos_filtrados if p["categoria"] == cat_filtro]
    if tema_filtro != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p["tema"] == tema_filtro]

    st.write(f"Exibindo **{len(produtos_filtrados)}** produto(s):")
    st.divider()

    # Exibição dos Produtos
    if not produtos_filtrados:
        st.warning("Nenhum produto encontrado com os filtros selecionados.")
    else:
        for prod in produtos_filtrados:
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                if prod["imagens"]:
                    st.image(prod["imagens"][0], use_container_width=True)
                else:
                    st.info("🖼️ Sem foto disponível")
                    
            with col_info:
                st.subheader(prod["nome"])
                st.write(f"**Categoria:** {prod['categoria']} | **Tema:** {prod['tema']}")
                
                # Tag visual de Status
                if prod["status"] == "Pronta Entrega":
                    st.success(f"Status: {prod['status']}")
                else:
                    st.info(f"Status: {prod['status']}")
                    
                st.write(prod["descricao"])
                
                # Galeria extra
                if len(prod["imagens"]) > 1:
                    with st.expander("📷 Ver mais fotos do produto"):
                        sub_cols = st.columns(min(len(prod["imagens"]) - 1, 4))
                        for idx, img_url in enumerate(prod["imagens"][1:]):
                            sub_cols[idx % 4].image(img_url, use_container_width=True)
                            
                # Botão WhatsApp
                msg_wa = f"Olá Sil! Gostei muito da peça '{prod['nome']}' e gostaria de solicitar um orçamento!"
                link_wa = f"https://wa.me/5518991234567?text={msg_wa.replace(' ', '%20')}"
                st.markdown(f"[💬 Encomendar pelo WhatsApp]({link_wa})")
            st.divider()

# ==========================================
# MODO 2: PAINEL DE GESTÃO (ÁREA RESTRITA)
# ==========================================
else:
    st.title("⚙️ Painel de Gestão do Ateliê")
    st.caption("Área restrita para atualização de produtos, estoque e envio de fotos para a nuvem.")
    
    senha = st.text_input("🔐 Digite a senha para acessar a edição:", type="password")
    
    if senha == "sil123":
        st.success("Acesso autorizado!")
        st.divider()
        
        aba_editar, aba_novo = st.tabs(["✏️ Editar / Adicionar Fotos", "➕ Cadastrar Novo Produto"])
        
        # -------------------------------------------------------------
        # ABA 1: EDITAR PRODUTO EXISTENTE
        # -------------------------------------------------------------
        with aba_editar:
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

            # Gerenciamento de fotos existentes
            st.markdown("### 🖼️ Fotos Atuais do Produto")
            fotos_atuais = prod_obj.get("imagens", [])

            if not fotos_atuais:
                st.info("Este produto ainda não possui fotos cadastradas.")
            else:
                st.write(f"O produto possui **{len(fotos_atuais)} foto(s)**. Clique em 'Excluir' para remover:")
                cols_fotos = st.columns(min(len(fotos_atuais), 4))
                for f_idx, foto_url in enumerate(fotos_atuais):
                    with cols_fotos[f_idx % 4]:
                        st.image(foto_url, use_container_width=True)
                        if st.button(f"🗑️ Excluir Foto {f_idx + 1}", key=f"del_{prod_obj['id']}_{f_idx}"):
                            prod_obj["imagens"].pop(f_idx)
                            st.toast("Foto removida!", icon="✅")
                            st.rerun()

            st.divider()

            # Form de Edição
            with st.form("form_edicao"):
                st.markdown("### ✏️ Alterar Informações do Produto")
                novo_nome = st.text_input("Nome do Produto:", value=prod_obj["nome"])
                nova_categoria = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"], index=["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"].index(prod_obj["categoria"]))
                novo_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"], index=["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"].index(prod_obj["tema"]))
                novo_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"], index=["Pronta Entrega", "Sob Encomenda"].index(prod_obj["status"]))
                nova_descricao = st.text_area("Descrição do Produto:", value=prod_obj["descricao"])
                
                st.markdown("---")
                st.markdown("➕ **Adicionar Fotos Reais ao Produto (Salvas na Nuvem):**")
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
                    
                    if novas_fotos_upload:
                        with st.spinner("Enviando fotos para a nuvem..."):
                            for arq in novas_fotos_upload:
                                url_publica = upload_foto_supabase(arq)
                                if url_publica:
                                    prod_obj["imagens"].append(url_publica)
                    
                    st.session_state.uploader_key += 1
                    st.success(f"✅ O produto '{novo_nome}' foi atualizado com sucesso!")
                    st.rerun()

        # -------------------------------------------------------------
        # ABA 2: CADASTRAR NOVO PRODUTO
        # -------------------------------------------------------------
        with aba_novo:
            st.markdown("### ➕ Adicionar um Novo Produto ao Catálogo")
            with st.form("form_novo_produto"):
                cad_nome = st.text_input("Nome do Novo Produto:")
                cad_categoria = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"])
                cad_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"])
                cad_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"])
                cad_descricao = st.text_area("Descrição do Produto:")
                cad_fotos = st.file_uploader("Fotos do Novo Produto:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="new_prod_uploader")
                
                btn_cadastrar = st.form_submit_button("✨ Cadastrar Produto")
                
                if btn_cadastrar:
                    if not cad_nome:
                        st.error("Por favor, digite o nome do produto.")
                    else:
                        novas_urls = []
                        if cad_fotos:
                            with st.spinner("Enviando fotos..."):
                                for f in cad_fotos:
                                    u = upload_foto_supabase(f)
                                    if u:
                                        novas_urls.append(u)
                        
                        novo_id = max([p["id"] for p in st.session_state.produtos], default=0) + 1
                        st.session_state.produtos.append({
                            "id": novo_id,
                            "nome": cad_nome,
                            "categoria": cad_categoria,
                            "tema": cad_tema,
                            "status": cad_status,
                            "descricao": cad_descricao,
                            "imagens": novas_urls
                        })
                        st.success(f"✅ Produto '{cad_nome}' cadastrado com sucesso!")
                        st.rerun()

    elif senha != "":
        st.error("Senha incorreta! Tente novamente.")
