import streamlit as st
from supabase import create_client, Client
import uuid
import base64

# Configuração da página
st.set_page_config(
    page_title="Ateliê Mimos & Artes da Sil",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Global em Tons Rosê, Vinho e Estilo Elegante
st.markdown("""
<style>
    /* Fundo da Aplicação */
    .stApp {
        background-color: #FFF9F9;
    }
    
    /* Cabeçalho Principal */
    .main-header {
        background: linear-gradient(135deg, #800020 0%, #C2185B 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.15);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-family: 'Georgia', serif;
    }
    .main-header p {
        color: #F8BBD0;
        margin-top: 8px;
        font-size: 1.1rem;
    }
    
    /* Rodapé / Informações de Contato */
    .info-box {
        background-color: #FFFFFF;
        border: 1px solid #F8BBD0;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 25px;
        color: #4A4A4A;
    }
    
    /* Cartões de Produtos */
    .product-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.08);
        border-left: 6px solid #800020;
        margin-bottom: 20px;
    }
    
    /* Botão WhatsApp */
    .btn-whatsapp {
        display: inline-block;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        font-weight: bold;
        padding: 10px 22px;
        border-radius: 25px;
        text-decoration: none;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }
    .btn-whatsapp:hover {
        transform: scale(1.03);
    }
    
    /* Botões Gerais */
    .stButton>button {
        background-color: #800020;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #C2185B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Conexão com o Supabase
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase()

# Lista de Produtos na Sessão
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

# Função de Envio de Fotos
def salvar_foto(file_obj):
    if supabase:
        try:
            file_ext = file_obj.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_ext}"
            file_bytes = file_obj.read()
            
            supabase.storage.from_("fotos-produtos").upload(
                file_name, 
                file_bytes, 
                {"content-type": file_obj.type}
            )
            return supabase.storage.from_("fotos-produtos").get_public_url(file_name)
        except Exception:
            pass
            
    # Fallback seguro
    file_bytes = file_obj.read()
    base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
    return f"data:{file_obj.type};base64,{base64_encoded}"

# --- NAVEGAÇÃO LATERAL E SUPERIOR ---
st.sidebar.markdown("## 🧵 Navegação")
modo_sidebar = st.sidebar.radio("Ir para:", ["🛍️ Catálogo de Produtos", "⚙️ Painel de Gestão (Restrito)"], key="nav_sidebar")

# Informações no Menu Lateral
st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Informações do Ateliê")
st.sidebar.write("📍 **Localização:** Três Lagoas - MS")
st.sidebar.write("📸 **Instagram:** [@ateliemimoseartes](#)")
st.sidebar.write("📱 **WhatsApp:** (67) 99999-9999")

modo = modo_sidebar

# ==========================================
# MODO 1: CATÁLOGO DO CLIENTE
# ==========================================
if modo == "🛍️ Catálogo de Produtos":
    # Banner de Cabeçalho
    st.markdown("""
    <div class="main-header">
        <h1>🌸 Ateliê Mimos & Artes da Sil</h1>
        <p>Peças artesanais exclusivas feitas com amor, carinho e devoção</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bloco de Informações de Contato e Endereço
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown("<div class='info-box'>📍 <b>Endereço:</b><br>Três Lagoas - MS</div>", unsafe_allow_html=True)
    with col_info2:
        st.markdown("<div class='info-box'>📸 <b>Redes Sociais:</b><br>Instagram: @ateliemimoseartes</div>", unsafe_allow_html=True)
    with col_info3:
        st.markdown("<div class='info-box'>💬 <b>Atendimento:</b><br>Segunda a Sábado via WhatsApp</div>", unsafe_allow_html=True)

    # Área de Pesquisa e Filtros
    st.markdown("### 🔍 Encontre o produto ideal")
    col_b, col_c, col_t = st.columns([2, 1, 1])
    with col_b:
        busca = st.text_input("Buscar por nome do produto:", placeholder="Ex: Bolsa, Naninha, Santos...")
    with col_c:
        cat_f = st.selectbox("Categoria:", ["Todas", "Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"])
    with col_t:
        tema_f = st.selectbox("Tema:", ["Todos", "Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"])

    # Filtragem dos produtos
    prods = st.session_state.produtos
    if busca:
        prods = [p for p in prods if busca.lower() in p["nome"].lower() or busca.lower() in p["descricao"].lower()]
    if cat_f != "Todas":
        prods = [p for p in prods if p["categoria"] == cat_f]
    if tema_f != "Todos":
        prods = [p for p in prods if p["tema"] == tema_f]

    st.write(f"Mostrando **{len(prods)}** produto(s) encontrado(s):")
    st.divider()

    # Listagem dos Produtos
    if not prods:
        st.warning("Nenhum produto encontrado para os filtros selecionados.")
    else:
        for p in prods:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            c_img, c_txt = st.columns([1, 2])
            
            with c_img:
                if p["imagens"]:
                    st.image(p["imagens"][0], use_container_width=True)
                else:
                    st.info("🖼️ Foto em breve")
            
            with c_txt:
                st.subheader(p["nome"])
                st.write(f"🏷️ **Categoria:** {p['categoria']} | 🎨 **Tema:** {p['tema']}")
                
                if p["status"] == "Pronta Entrega":
                    st.success(f"✨ Status: {p['status']}")
                else:
                    st.info(f"⏳ Status: {p['status']}")
                    
                st.write(p["descricao"])
                
                if len(p["imagens"]) > 1:
                    with st.expander("📷 Ver mais fotos deste produto"):
                        g_cols = st.columns(min(len(p["imagens"]) - 1, 4))
                        for idx, img_u in enumerate(p["imagens"][1:]):
                            g_cols[idx % 4].image(img_u, use_container_width=True)
                
                msg_wa = f"Olá Sil! Gostei do produto '{p['nome']}' e gostaria de pedir informações!"
                link_wa = f"https://wa.me/5567999999999?text={msg_wa.replace(' ', '%20')}"
                st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-whatsapp">💬 Encomendar pelo WhatsApp</a>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MODO 2: PAINEL DA ARTESÃ
# ==========================================
else:
    st.title("⚙️ Painel de Gestão da Artesã")
    st.caption("Área restrita para edição e cadastro de peças.")
    
    senha = st.text_input("🔐 Digite a senha para acessar:", type="password")
    
    if senha == "sil123":
        st.success("Acesso liberado!")
        st.divider()
        
        tab_edit, tab_new = st.tabs(["✏️ Gerenciar Produtos & Fotos", "➕ Cadastrar Nova Peça"])
        
        with tab_edit:
            opcoes_prod = {p["nome"]: p for p in st.session_state.produtos}
            
            def reset_uploader():
                st.session_state.up_key = st.session_state.get("up_key", 0) + 1

            p_nome = st.selectbox("Selecione o produto para editar:", list(opcoes_prod.keys()), on_change=reset_uploader)
            p_obj = opcoes_prod[p_nome]

            if "up_key" not in st.session_state:
                st.session_state.up_key = 0

            st.markdown("### 🖼️ Fotos Cadastradas")
            fotos = p_obj.get("imagens", [])
            
            if not fotos:
                st.info("Este produto ainda não possui fotos salvas.")
            else:
                f_cols = st.columns(min(len(fotos), 4))
                for idx, f_url in enumerate(fotos):
                    with f_cols[idx % 4]:
                        st.image(f_url, use_container_width=True)
                        if st.button(f"🗑️ Excluir Foto {idx+1}", key=f"del_{p_obj['id']}_{idx}"):
                            p_obj["imagens"].pop(idx)
                            st.toast("Foto removida com sucesso!")
                            st.rerun()

            st.divider()

            with st.form("form_edicao"):
                st.markdown("### ✏️ Editar Dados do Produto")
                n_nome = st.text_input("Nome:", value=p_obj["nome"])
                n_cat = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"], index=["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"].index(p_obj["categoria"]))
                n_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"], index=["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"].index(p_obj["tema"]))
                n_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"], index=["Pronta Entrega", "Sob Encomenda"].index(p_obj["status"]))
                n_desc = st.text_area("Descrição:", value=p_obj["descricao"])
                
                st.markdown("➕ **Adicionar Fotos ao Produto:**")
                novas_fotos = st.file_uploader(
                    "Selecione as fotos do seu celular ou computador", 
                    type=["png", "jpg", "jpeg"], 
                    accept_multiple_files=True,
                    key=f"uploader_{st.session_state.up_key}"
                )
                
                if st.form_submit_button("💾 Salvar Alterações"):
                    p_obj["nome"] = n_nome
                    p_obj["categoria"] = n_cat
                    p_obj["tema"] = n_tema
                    p_obj["status"] = n_status
                    p_obj["descricao"] = n_desc
                    
                    if novas_fotos:
                        with st.spinner("Enviando fotos..."):
                            for arq in novas_fotos:
                                url_salva = salvar_foto(arq)
                                if url_salva:
                                    p_obj["imagens"].append(url_salva)
                    
                    st.session_state.up_key += 1
                    st.success("✅ Alterações salvas com sucesso!")
                    st.rerun()

        with tab_new:
            st.markdown("### ➕ Cadastrar Novo Produto no Catálogo")
            with st.form("form_novo"):
                c_nome = st.text_input("Nome da Peça:")
                c_cat = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"])
                c_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"])
                c_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"])
                c_desc = st.text_area("Descrição:")
                c_fotos = st.file_uploader("Fotos do Produto:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="new_up")
                
                if st.form_submit_button("✨ Cadastrar Produto"):
                    if not c_nome:
                        st.error("Por favor, informe o nome da peça.")
                    else:
                        urls = []
                        if c_fotos:
                            with st.spinner("Salvando fotos..."):
                                for f in c_fotos:
                                    u = salvar_foto(f)
                                    if u:
                                        urls.append(u)
                        
                        n_id = max([p["id"] for p in st.session_state.produtos], default=0) + 1
                        st.session_state.produtos.append({
                            "id": n_id,
                            "nome": c_nome,
                            "categoria": c_cat,
                            "tema": c_tema,
                            "status": c_status,
                            "descricao": c_desc,
                            "imagens": urls
                        })
                        st.success(f"✅ Peça '{c_nome}' cadastrada com sucesso!")
                        st.rerun()

    elif senha != "":
        st.error("Senha incorreta!")
