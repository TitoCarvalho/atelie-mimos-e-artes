import streamlit as st
import base64
import uuid
from supabase import create_client, Client

# 1. Configuração da Página
st.set_page_config(
    page_title="Ateliê Mimos & Artes da Sil",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Conexão com o Supabase para Armazenamento de Fotos na Nuvem
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase()

def salvar_foto_nuvem(file_obj):
    """Envia a foto para o Supabase Storage e retorna a URL pública."""
    if supabase:
        try:
            file_ext = file_obj.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_ext}"
            file_bytes = file_obj.read()
            
            # Upload para o bucket fotos-produtos
            supabase.storage.from_("fotos-produtos").upload(
                file_name, 
                file_bytes, 
                {"content-type": file_obj.type}
            )
            # Retorna a URL pública gerada
            return supabase.storage.from_("fotos-produtos").get_public_url(file_name)
        except Exception as e:
            pass
            
    # Fallback seguro caso a conexão falhe
    file_bytes = file_obj.read()
    base64_image = base64.b64encode(file_bytes).decode('utf-8')
    return f"data:{file_obj.type};base64,{base64_image}"

# 3. Injeção de Estilo CSS Personalizado
st.markdown("""
    <style>
    /* Fundo principal e tipografia */
    .stApp {
        background: linear-gradient(180deg, #FFF9FA 0%, #F7EBEF 100%);
        font-family: 'Quicksand', 'Segoe UI', sans-serif;
    }
    
    /* Cabeçalho Principal */
    .header-container {
        background: linear-gradient(135deg, #8A2B59 0%, #C85A8A 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0px 10px 25px rgba(138, 43, 89, 0.2);
        margin-bottom: 25px;
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .header-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.95;
        margin-top: 8px;
    }

    /* Cartões de Métricas */
    [data-testid="stMetricValue"] {
        color: #8A2B59 !important;
        font-weight: 800 !important;
    }
    
    /* Estilização dos Containers dos Produtos */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 18px !important;
        border: 1px solid #F0C2D4 !important;
        box-shadow: 0px 6px 15px rgba(200, 90, 138, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        padding: 15px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 20px rgba(138, 43, 89, 0.15);
        border-color: #C85A8A !important;
    }

    /* Títulos dos Produtos */
    .product-title {
        color: #5A1838;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 10px;
    }

    /* Botão de Destaque WhatsApp */
    .stLinkButton > a {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stLinkButton > a:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 18px rgba(37, 211, 102, 0.45) !important;
    }

    /* Caixa de Contato / Rodapé */
    .footer-box {
        background: linear-gradient(135deg, #FFF3F7 0%, #F5E1EA 100%);
        border: 2px dashed #C85A8A;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-top: 30px;
    }
    .footer-title {
        color: #8A2B59;
        font-weight: 800;
        font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Dados Fixos do Ateliê
NOME_ATELIE = "Ateliê Mimos & Artes da Sil"
WHATSAPP_NUM = "5515981269458"
ENDERECO = "Rua Romeu de Campos, 1029 - Bairro Vila Nova - Três Lagoas - MS, CEP: 79604-100"
LINK_FB = "https://www.facebook.com/1731249910444261?ref=NONE_xav_ig_profile_page_web"
LINK_IG = "https://www.instagram.com/mimoseartesdasil?utm_source=ig_web_button_share_sheet&stkn=ZDNlZDc0MzIxNw=="

# 5. Inicialização dos Produtos na Sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {
            "id": 1,
            "nome": "Bolsa Infantil Super-Heróis",
            "categoria": "Bolsas",
            "tema": "Tendências e Super-Heróis",
            "status": "Sob Encomenda",
            "descricao": "Bolsa artesanal resistente em tecido estampado com tema de super-heróis. Perfeita para passeios e rotina escolar.",
            "imagens": [
                "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500",
                "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"
            ]
        },
        {
            "id": 2,
            "nome": "Bolsa de Devoção Nossa Senhora",
            "categoria": "Bolsas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Pronta Entrega",
            "descricao": "Bolsa com detalhes delicados e estampa de santinhos de devoção. Acabamento reforçado e estampa exclusiva.",
            "imagens": [
                "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=500"
            ]
        },
        {
            "id": 3,
            "nome": "Naninha de Aconchego Safari",
            "categoria": "Naninhas",
            "tema": "Safari",
            "status": "Pronta Entrega",
            "descricao": "Naninha ultra macia em tecido antialérgico com bichinhos do safari. Proporciona conforto e segurança ao bebê.",
            "imagens": [
                "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=500"
            ]
        },
        {
            "id": 4,
            "nome": "Naninha Anjinho da Guarda",
            "categoria": "Naninhas",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Sob Encomenda",
            "descricao": "Naninha em formato de anjinho, em tecido 100% algodão. Toque suave ideal para o sono abençoado do bebê.",
            "imagens": [
                "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=500"
            ]
        },
        {
            "id": 5,
            "nome": "Boneca de Pano Princesa Real",
            "categoria": "Bonecas de Pano",
            "tema": "Princesas",
            "status": "Sob Encomenda",
            "descricao": "Boneca artesanal com vestido rico em rendas, cabelo em fios de lã e rostinho pintado à mão com carinho.",
            "imagens": [
                "https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?w=500"
            ]
        },
        {
            "id": 6,
            "nome": "Boneca Camponesa Clássica",
            "categoria": "Bonecas de Pano",
            "tema": "Diversos",
            "status": "Pronta Entrega",
            "descricao": "Boneca de pano tradicional com roupinha florida e chapéu de tecido. Uma peça afetiva para decoração ou brincadeiras.",
            "imagens": [
                "https://images.unsplash.com/photo-1535572290543-960a8046f5af?w=500"
            ]
        },
        {
            "id": 7,
            "nome": "Amigurumi São Francisco de Assis",
            "categoria": "Amigurumi",
            "tema": "Religioso (Santos de Devoção)",
            "status": "Sob Encomenda",
            "descricao": "Santinho em crochê feito à mão (Amigurumi) com linha 100% algodão, mini passarinhos e cordão tradicional.",
            "imagens": [
                "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=500"
            ]
        },
        {
            "id": 8,
            "nome": "Amigurumi Leãozinho do Safari",
            "categoria": "Amigurumi",
            "tema": "Safari",
            "status": "Pronta Entrega",
            "descricao": "Fofo leãozinho em técnica de amigurumi com olhos de segurança. Ideal para nichos de maternidade.",
            "imagens": [
                "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=500"
            ]
        }
    ]

# 6. Navegação no Menu Lateral
st.sidebar.markdown("## 📍 Navegação")
modo_visao = st.sidebar.radio("Selecione o modo:", ["🛍️ Catálogo (Visão do Cliente)", "⚙️ Gerenciar Produtos (Painel da Sil)"])

# ==========================================
# MODO 1: CATÁLOGO PÚBLICO DO CLIENTE
# ==========================================
if modo_visao == "🛍️ Catálogo (Visão do Cliente)":
    
    # Banner de Boas-Vindas
    st.markdown(f"""
        <div class="header-container">
            <div class="header-title">🧵 {NOME_ATELIE}</div>
            <div class="header-subtitle">💖 Peças feitas à mão que aquecem o coração: Arte em tecido, bonecas de pano e amigurumis.</div>
        </div>
    """, unsafe_allow_html=True)

    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("✨ Acervo Artesanal", f"{len(st.session_state.produtos)} Peças")
    m2.metric("📍 Produção Local", "Três Lagoas / MS")
    m3.metric("💝 Carinho em Cada Ponto", "100% Personalizado")

    st.divider()

    # Filtros
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 💖 Encontre seu Mimo")
    busca_termo = st.sidebar.text_input("🔍 O que você procura?", placeholder="Ex: Anjinho, Leão, Bolsa...")

    categoria_sel = st.sidebar.selectbox("📂 Categoria", ["Todas", "Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"])
    tema_sel = st.sidebar.selectbox("🎭 Tema Escolhido", ["Todos", "Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"])
    status_sel = st.sidebar.selectbox("⏱️ Disponibilidade", ["Todos", "Pronta Entrega", "Sob Encomenda"])

    # Filtragem
    produtos_filtrados = st.session_state.produtos

    if busca_termo:
        produtos_filtrados = [p for p in produtos_filtrados if busca_termo.lower() in p["nome"].lower() or busca_termo.lower() in p["descricao"].lower()]

    if categoria_sel != "Todas":
        produtos_filtrados = [p for p in produtos_filtrados if p["categoria"] == categoria_sel]

    if tema_sel != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p["tema"] == tema_sel]

    if status_sel != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p["status"] == status_sel]

    # Exibição
    st.markdown(f"### 🌸 Exibindo Peças Especiais ({len(produtos_filtrados)})")

    if not produtos_filtrados:
        st.warning("Nenhum mimo encontrado com esses filtros. Que tal tentar outra combinação?")
    else:
        cols = st.columns(2)
        for idx, prod in enumerate(produtos_filtrados):
            with cols[idx % 2]:
                with st.container(border=True):
                    
                    # Exibição das Fotos Reais (Galeria/Carrossel com abas)
                    fotos = prod.get("imagens", [])
                    if fotos:
                        if len(fotos) == 1:
                            st.image(fotos[0], use_container_width=True)
                        else:
                            st.caption(f"📸 **Galeria do Produto ({len(fotos)} fotos reais):**")
                            tabs = st.tabs([f"Foto {i+1}" for i in range(len(fotos))])
                            for t_idx, tab in enumerate(tabs):
                                with tab:
                                    st.image(fotos[t_idx], use_container_width=True)
                    else:
                        st.info("Nenhuma foto disponível para esta peça.")

                    st.markdown(f'<div class="product-title">{prod["nome"]}</div>', unsafe_allow_html=True)
                    
                    if prod["status"] == "Pronta Entrega":
                        st.success(f"✨ {prod['status']}")
                    else:
                        st.info(f"🎨 {prod['status']}")
                    
                    st.caption(f"🏷️ **{prod['categoria']}** | 🎭 **{prod['tema']}**")
                    st.write(prod["descricao"])
                    
                    msg_wa = f"Olá, Sil! Me apaixonei pelo produto '{prod['nome']}' ({prod['categoria']}) do seu catálogo! Como posso encomendar?"
                    link_wa = f"https://wa.me/{WHATSAPP_NUM}?text={msg_wa.replace(' ', '%20')}"
                    
                    st.link_button("💬 Encomendar Amor em Ponto", link_wa, use_container_width=True)

    # FAQ
    st.divider()
    st.markdown("### ❓ Como Funciona nosso Ateliê?")

    with st.expander("💖 Como escolho as cores e detalhes do meu pedido?"):
        st.write("Cada pecinha é feita de forma afetiva! Ao clicar no botão de encomenda, você fala direto com a Sil pelo WhatsApp e combinamos as cores, tecidos e estampas perfeitas para você.")

    with st.expander("📦 Envia para todo o Brasil?"):
        st.write("Sim! Enviamos para todo o Brasil via Correios ou transportadora. Para moradores de Três Lagoas/MS, oferecemos opção de retirada local.")

    with st.expander("💳 Quais são as opções de pagamento?"):
        st.write("Aceitamos PIX, cartões de crédito e débito com total segurança e facilidade.")

    # Rodapé
    st.markdown(f"""
        <div class="footer-box">
            <div class="footer-title">📍 Venha Conhecer Nosso Cantinho</div>
            <p style="color: #6A2145; font-weight: 600; margin-top: 10px;">
                {ENDERECO}<br>
                <strong>WhatsApp:</strong> (15) 98126-9458
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_social1, col_social2 = st.columns(2)
    with col_social1:
        st.link_button("📸 Acompanhe no Instagram", LINK_IG, use_container_width=True)
    with col_social2:
        st.link_button("📘 Siga Nossa Página no Facebook", LINK_FB, use_container_width=True)

# ==========================================
# MODO 2: PAINEL DE GESTÃO (ÁREA RESTRITA)
# ==========================================
else:
    st.title("⚙️ Painel de Gestão do Ateliê")
    st.caption("Área restrita para atualizar informações, adicionar ou remover fotos reais dos produtos.")
    
    # Proteção por senha
    senha = st.text_input("🔐 Digite a senha para acessar a edição:", type="password")
    
    if senha == "sil123":
        st.success("Acesso autorizado!")
        
        st.divider()
        st.subheader("📝 Editar Produto Existente")
        
        opcoes_produtos = {p["nome"]: p for p in st.session_state.produtos}
        prod_selecionado_nome = st.selectbox("Escolha qual produto deseja alterar:", list(opcoes_produtos.keys()))
        prod_obj = opcoes_produtos[prod_selecionado_nome]

        # -------------------------------------------------------------
        # GERENCIADOR E REMOÇÃO DE FOTOS INDIVIDUAIS
        # -------------------------------------------------------------
        st.markdown("### 🖼️ Gerenciar Fotos Atuais")
        fotos_atuais = prod_obj.get("imagens", [])

        if not fotos_atuais:
            st.info("Este produto ainda não possui fotos cadastradas.")
        else:
            st.write(f"O produto possui **{len(fotos_atuais)} foto(s)**. Clique em 'Excluir' para remover uma foto específica:")
            
            cols_fotos = st.columns(min(len(fotos_atuais), 4))
            for f_idx, foto_url in enumerate(fotos_atuais):
                with cols_fotos[f_idx % 4]:
                    st.image(foto_url, use_container_width=True)
                    if st.button(f"🗑️ Excluir Foto {f_idx + 1}", key=f"del_{prod_obj['id']}_{f_idx}"):
                        prod_obj["imagens"].pop(f_idx)
                        st.toast(f"Foto {f_idx + 1} removida com sucesso!", icon="✅")
                        st.rerun()

        st.divider()

        # -------------------------------------------------------------
        # FORMULÁRIO DE EDIÇÃO DE TEXTO E UPLOAD PARA NUVEM
        # -------------------------------------------------------------
        with st.form("form_edicao"):
            st.markdown("### ✏️ Alterar Informações do Produto")
            novo_nome = st.text_input("Nome do Produto:", value=prod_obj["nome"])
            nova_categoria = st.selectbox("Categoria:", ["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"], index=["Bolsas", "Naninhas", "Bonecas de Pano", "Amigurumi"].index(prod_obj["categoria"]))
            novo_tema = st.selectbox("Tema:", ["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"], index=["Religioso (Santos de Devoção)", "Tendências e Super-Heróis", "Safari", "Princesas", "Diversos"].index(prod_obj["tema"]))
            novo_status = st.selectbox("Status:", ["Pronta Entrega", "Sob Encomenda"], index=["Pronta Entrega", "Sob Encomenda"].index(prod_obj["status"]))
            nova_descricao = st.text_area("Descrição do Produto:", value=prod_obj["descricao"])
            
            st.markdown("---")
            st.markdown("➕ **Adicionar Mais Fotos Reais (Salvas na Nuvem):**")
            novas_fotos_upload = st.file_uploader("Selecione novas fotos do seu dispositivo", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
            
            btn_salvar = st.form_submit_button("💾 Salvar Alterações")
            
            if btn_salvar:
                prod_obj["nome"] = novo_nome
                prod_obj["categoria"] = nova_categoria
                prod_obj["tema"] = novo_tema
                prod_obj["status"] = novo_status
                prod_obj["descricao"] = nova_descricao
                
                # Salva as novas fotos no Supabase Storage
                if novas_fotos_upload:
                    with st.spinner("Enviando fotos para a nuvem..."):
                        for arq in novas_fotos_upload:
                            url_foto = salvar_foto_nuvem(arq)
                            prod_obj["imagens"].append(url_foto)
                
                st.success(f"✅ O produto '{novo_nome}' foi atualizado com sucesso!")
                st.rerun()

    elif senha != "":
        st.error("Senha incorreta! Tente novamente.")
