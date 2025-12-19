import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Print Mais - Intel", layout="wide", page_icon="🖨️")

# --- 1. SISTEMA DE LOGIN (BUSCA SENHA NOS SEGREDOS) ---
def check_password():
    """Retorna True se o usuário tiver a senha correta."""
    def password_entered():
        # Verifica se a senha digitada bate com a senha configurada no Streamlit Cloud
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove a senha da memória por segurança
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primeira vez abrindo o site: mostra o campo de senha
        st.text_input(
            "🔒 Digite a senha de acesso:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Senha errada
        st.text_input(
            "🔒 Digite a senha de acesso:", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Senha incorreta.")
        return False
    else:
        # Senha correta
        return True

if check_password():
    
    # --- CSS PARA ESTILO VISUAL ---
    st.markdown("""
    <style>
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 5px solid #20B2AA;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .metric-card h3 {font-size: 14px; color: #555; margin: 0;}
        .metric-card h2 {font-size: 24px; color: #333; margin: 0;}
        .stTabs [data-baseweb="tab-list"] {gap: 10px;}
        .stTabs [data-baseweb="tab"] {
            height: 50px; white-space: pre-wrap; background-color: #ffffff;
            border-radius: 5px; border: 1px solid #ddd; padding: 10px;
        }
        .stTabs [aria-selected="true"] {background-color: #20B2AA; color: white; border: none;}
    </style>
    """, unsafe_allow_html=True)

    # --- 2. CARREGAMENTO DE DADOS (SEGURO - VIA SECRETS) ---
    @st.cache_data
    def load_data_from_secrets():
        # As coordenadas não são dados sensíveis, podem ficar no código para facilitar
        coords = {
            'AFOGADOS DA INGAZEIRA': {'lat': -7.7495, 'lon': -37.6385},
            'BELO JARDIM': {'lat': -8.3323, 'lon': -36.4255},
            'BREJINHO': {'lat': -7.3486, 'lon': -37.2974},
            'CARUARU': {'lat': -8.2849, 'lon': -35.9696},
            'GARANHUNS': {'lat': -8.8829, 'lon': -36.4957},
            'GOIANA': {'lat': -7.5593, 'lon': -35.0003},
            'ITAMBE': {'lat': -7.4087, 'lon': -35.1099},
            'JABOATAO': {'lat': -8.1105, 'lon': -35.0177},
            'LAJEDO': {'lat': -8.6625, 'lon': -36.3197},
            'LIMOEIRO': {'lat': -7.8732, 'lon': -35.4507},
            'MACAPARANA': {'lat': -7.5539, 'lon': -35.4533},
            'OLINDA': {'lat': -8.0089, 'lon': -34.8553},
            'OROBO': {'lat': -7.7342, 'lon': -35.6033},
            'PETROLANDIA': {'lat': -8.9790, 'lon': -38.2195},
            'PETROLINA': {'lat': -9.3831, 'lon': -40.5069},
            'POMBOS': {'lat': -8.1388, 'lon': -35.3976},
            'RECIFE': {'lat': -8.0476, 'lon': -34.8770},
            'SANTA CRUZ CAPIBARIBE': {'lat': -7.9472, 'lon': -36.2045},
            'SAO JOSE DO EGITO': {'lat': -7.4764, 'lon': -37.2694},
            'SAO LOURENCO DA MATA': {'lat': -8.0016, 'lon': -35.0176},
            'SAO VICENTE FERRER': {'lat': -7.5910, 'lon': -35.4899},
            'SERRA TALHADA': {'lat': -7.9931, 'lon': -38.2983},
            'TABIRA': {'lat': -7.5901, 'lon': -37.5348},
            'TIMBAUBA': {'lat': -7.5028, 'lon': -35.3202},
            'VITORIA DE SANTO ANTAO': {'lat': -8.1190, 'lon': -35.2952}
        }

        try:
            # AQUI ACONTECE A MÁGICA: O código lê o texto oculto nos Secrets e transforma em dados
            dados_thales = json.loads(st.secrets["dados_thales_json"])
            dados_nov = json.loads(st.secrets["dados_nov_json"])
            
            return pd.DataFrame(dados_thales), pd.DataFrame(dados_nov), coords
        except Exception as e:
            # Se não configurar os secrets, mostra o erro amigável
            return pd.DataFrame(), pd.DataFrame(), {}

    df_thales, df_nov, coords_dict = load_data_from_secrets()

    # --- 3. PROCESSAMENTO DOS DADOS (INTELIGÊNCIA) ---
    if not df_thales.empty and not df_nov.empty:
        # Agrupamento Thales
        df_thales_ag = df_thales.groupby(['id', 'cidade', 'cliente'])[['ago', 'set', 'out']].sum().reset_index()
        df_thales_ag['Total_Trimestre'] = df_thales_ag['ago'] + df_thales_ag['set'] + df_thales_ag['out']
        df_thales_ag['Media_Thales'] = df_thales_ag['Total_Trimestre'] / 3

        # Agrupamento Novembro
        df_nov_ag = df_nov.groupby(['id', 'cidade', 'cliente', 'vendedor'])['nov'].sum().reset_index()

        # Unificação (Antes x Depois)
        df_full = pd.merge(df_thales_ag, df_nov_ag, on='id', how='outer', suffixes=('_ant', '_nov'))

        # Limpeza de Nomes
        df_full['Cliente'] = df_full['cliente_nov'].combine_first(df_full['cliente_ant'])
        df_full['Cidade'] = df_full['cidade_nov'].combine_first(df_full['cidade_ant'])
        df_full.fillna(0, inplace=True)
        df_full['vendedor'] = df_full['vendedor'].replace(0, 'Sem Venda')

        # Regra de Negócio: Definição de Status
        def definir_status(row):
            thales_ativo = row['Media_Thales'] > 0
            nov_ativo = row['nov'] > 0
            
            if thales_ativo and not nov_ativo:
                return '🔴 Churn (Perdido)'
            elif thales_ativo and nov_ativo:
                if row['nov'] > row['Media_Thales']:
                     return '🟢 Retido (Cresceu)'
                else:
                     return '🔵 Retido (Caiu)'
            elif not thales_ativo and nov_ativo:
                return '🟡 Novo/Recuperado'
            else:
                return '⚪ Inativo'

        df_full['Status'] = df_full.apply(definir_status, axis=1)

        # Adiciona Latitude e Longitude
        def get_lat(cidade): return coords_dict.get(cidade, {}).get('lat', None)
        def get_lon(cidade): return coords_dict.get(cidade, {}).get('lon', None)
        df_full['lat'] = df_full['Cidade'].apply(get_lat)
        df_full['lon'] = df_full['Cidade'].apply(get_lon)

        # --- 4. BARRA LATERAL (FILTROS) ---
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
        st.sidebar.title("Comando")
        
        # Botão de Sair
        if st.sidebar.button("Sair / Logout"):
            del st.session_state["password_correct"]
            st.rerun()

        # Filtros
        cidades = ['TODAS'] + sorted(df_full['Cidade'].unique().tolist())
        cidade_filtro = st.sidebar.selectbox("🗺️ Filtrar Cidade", cidades)
        
        status_opcoes = df_full['Status'].unique()
        status_filtro = st.sidebar.multiselect("🏷️ Filtrar Status", status_opcoes, default=status_opcoes)

        # Aplicação dos Filtros
        df_view = df_full.copy()
        if cidade_filtro != 'TODAS':
            df_view = df_view[df_view['Cidade'] == cidade_filtro]
        if status_filtro:
            df_view = df_view[df_view['Status'].isin(status_filtro)]

        # --- 5. O DASHBOARD (VISUALIZAÇÃO) ---
        st.title("🚀 Painel de Inteligência: Transição de Carteira")
        st.markdown("---")

        # Cartões de Métricas (KPIs)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fat_total = df_view['nov'].sum()
            st.markdown(f'<div class="metric-card"><h3>💰 Faturamento Nov</h3><h2>R$ {fat_total:,.2f}</h2></div>', unsafe_allow_html=True)
        
        with col2:
            novos = df_view[df_view['Status'] == '🟡 Novo/Recuperado']['nov'].sum()
            st.markdown(f'<div class="metric-card"><h3>✨ Novos Negócios</h3><h2>R$ {novos:,.2f}</h2></div>', unsafe_allow_html=True)
        
        with col3:
            churn_val = df_view[df_view['Status'] == '🔴 Churn (Perdido)']['Media_Thales'].sum()
            st.markdown(f'<div class="metric-card"><h3>⚠️ Potencial Perdido</h3><h2 style="color:#FF4B4B">R$ {churn_val:,.2f}</h2></div>', unsafe_allow_html=True)
        
        with col4:
            clientes_ativos = df_view[df_view['nov'] > 0].shape[0]
            st.markdown(f'<div class="metric-card"><h3>👥 Clientes Ativos</h3><h2>{clientes_ativos}</h2></div>', unsafe_allow_html=True)

        st.write("") # Espaço em branco

        # Abas de Navegação
        tab_map, tab_pareto, tab_equipe, tab_retencao, tab_sim, tab_detalhe = st.tabs([
            "🗺️ Mapa", 
            "📉 Perdas (Pareto)", 
            "🏆 Equipe", 
            "⚖️ Comparativo", 
            "🎮 Simulador", 
            "📋 Tabela Detalhada"
        ])

        # --- ABA MAPA ---
        with tab_map:
            st.subheader("📍 Geografia das Vendas")
            
            # Prepara dados geográficos
            df_map = df_view.groupby(['Cidade', 'lat', 'lon'])[['nov', 'Media_Thales']].sum().reset_index()
            
            # Formatação para o mouseover
            df_map['Faturamento Nov'] = df_map['nov'].apply(lambda x: f"R$ {x:,.2f}")
            df_map['Média Histórica'] = df_map['Media_Thales'].apply(lambda x: f"R$ {x:,.2f}")
            df_map['Status_Cidade'] = df_map.apply(lambda x: 'Crescimento' if x['nov'] > x['Media_Thales'] else 'Queda', axis=1)
            
            # Tamanho da bolha (ajuste matemático suave)
            df_map['Tamanho_Bolha'] = (df_map['nov'] + df_map['Media_Thales']).apply(lambda x: x**0.5) 

            fig_map = px.scatter_mapbox(
                df_map, lat="lat", lon="lon", hover_name="Cidade",
                hover_data={"lat": False, "lon": False, "Tamanho_Bolha": False, "Status_Cidade": False, "Faturamento Nov": True, "Média Histórica": True},
                size="Tamanho_Bolha", color="Status_Cidade",
                color_discrete_map={'Crescimento': '#00CC96', 'Queda': '#FF4B4B'},
                zoom=6.5, height=600, size_max=40
            )
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        # --- ABA PARETO (CHURN) ---
        with tab_pareto:
            st.subheader("🕵️ Maiores Clientes Perdidos")
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                df_lost = df_view[df_view['Status'] == '🔴 Churn (Perdido)'].sort_values(by='Media_Thales', ascending=False).head(10)
                if not df_lost.empty:
                    fig_bar = px.bar(df_lost, x='Media_Thales', y='Cliente', orientation='h', text_auto='.2s', 
                                     title="Top 10 Clientes Perdidos (Valor Médio)", 
                                     color_discrete_sequence=['#FF4B4B'])
                    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.success("Parabéns! Nenhum cliente perdido nesta seleção.")
            
            with col_b:
                st.info("💡 **Dica:** Estes clientes representam o maior volume financeiro que deixou de entrar. A recuperação deve começar por aqui.")

        # --- ABA EQUIPE ---
        with tab_equipe:
            st.subheader("🏆 Ranking de Vendedores (Novembro)")
            df_vendedores = df_view[df_view['nov'] > 0].groupby('vendedor')['nov'].sum().reset_index().sort_values(by='nov', ascending=False)
            
            col_e1, col_e2 = st.columns([2, 1])
            with col_e1:
                fig_vend = px.bar(df_vendedores, x='vendedor', y='nov', text_auto='.2s', 
                                  title="Faturamento por Vendedor", color='nov', color_continuous_scale='Teal')
                st.plotly_chart(fig_vend, use_container_width=True)
            with col_e2:
                st.plotly_chart(px.pie(df_vendedores, names='vendedor', values='nov', title="Share de Vendas"), use_container_width=True)

        # --- ABA COMPARATIVO ---
        with tab_retencao:
            st.subheader("⚖️ Thales vs. Atual (Mesmo Cliente)")
            # Filtra Top 20 clientes ativos
            df_comp = df_view[(df_view['Media_Thales'] > 0) | (df_view['nov'] > 0)].copy()
            df_comp['Total_Volume'] = df_comp['Media_Thales'] + df_comp['nov']
            df_top20 = df_comp.sort_values(by='Total_Volume', ascending=False).head(20)
            
            df_long = df_top20.melt(id_vars='Cliente', value_vars=['Media_Thales', 'nov'], var_name='Periodo', value_name='Valor')
            
            fig_group = px.bar(df_long, x='Cliente', y='Valor', color='Periodo', barmode='group',
                               title="Top 20 Clientes: Antes vs Depois", 
                               color_discrete_map={'Media_Thales': '#FFA07A', 'nov': '#20B2AA'}, text_auto='.2s')
            st.plotly_chart(fig_group, use_container_width=True)

        # --- ABA SIMULADOR ---
        with tab_sim:
            st.subheader("🎲 Simulador de Metas")
            col_sim1, col_sim2 = st.columns([1, 2])
            
            with col_sim1:
                meta = st.slider("Meta de Recuperação (%)", 0, 100, 20)
                st.markdown(f"Se recuperarmos **{meta}%** do churn...")
            
            with col_sim2:
                recup = churn_val * (meta / 100)
                total_proj = df_view['nov'].sum() + recup
                
                st.metric("Potencial Extra de Receita", f"+ R$ {recup:,.2f}")
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number", value=total_proj, 
                    title={'text': "Projeção de Faturamento Total"}, 
                    gauge={'bar': {'color': "#20B2AA"}}
                ))
                st.plotly_chart(fig_gauge, use_container_width=True, height=250)

        # --- ABA TABELA ---
        with tab_detalhe:
            st.subheader("📋 Lista Detalhada")
            
            def highlight_rows(val):
                if 'Churn' in str(val): return 'background-color: #ffe6e6' # Vermelho claro
                if 'Cresceu' in str(val): return 'background-color: #e6fffa' # Verde claro
                if 'Novo' in str(val): return 'background-color: #fff8e1' # Amarelo claro
                return ''
            
            cols = ['id', 'Cidade', 'Cliente', 'vendedor', 'Media_Thales', 'nov', 'Status']
            st.dataframe(
                df_view[cols].sort_values(by='Status')
                .style.applymap(highlight_rows, subset=['Status'])
                .format({'Media_Thales': 'R$ {:.2f}', 'nov': 'R$ {:.2f}'}),
                use_container_width=True, height=600
            )
            
            # Botão de Download
            csv = df_view.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Baixar Dados (CSV)", data=csv, file_name="relatorio_printmais.csv", mime="text/csv")

    else:
        # TELA DE ERRO AMIGÁVEL SE NÃO TIVER DADOS NO SECRETS
        st.warning("⚠️ Os dados do sistema não foram encontrados.")
        st.info("Por favor, configure o JSON de dados nas configurações 'Secrets' do Streamlit Cloud.")
