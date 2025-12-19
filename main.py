import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Print Mais - Intel", layout="wide", page_icon="🖨️")

# Estilo CSS customizado (Visual Limpo)
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #20B2AA;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-card h3 {
        font-size: 14px;
        color: #555;
        margin: 0;
    }
    .metric-card h2 {
        font-size: 24px;
        color: #333;
        margin: 0;
    }
    /* Ajuste das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #20B2AA;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. CARGA DE DADOS (HARDCODED) ---
@st.cache_data
def load_data():
    # Coordenadas das Cidades (PE)
    coords = {
        'AFOGADOS DA INGAZEIRA': {'lat': -7.7495, 'lon': -37.6385},
        'BELO JARDIM': {'lat': -8.3323, 'lon': -36.4255},
        'BREJINHO': {'lat': -7.3486, 'lon': -37.2974},
        'CARUARU': {'lat': -8.2849, 'lon': -35.9696},
        'GARANHUNS': {'lat': -8.8829, 'lon': -36.4957},
        'GOIANA': {'lat': -7.5593, 'lon': -35.0003},
        'ITAMBE': {'lat': -7.4087, 'lon': -35.1099},
        'JABOATAO': {'lat': -8.1105, 'lon': -35.0177}, # Jaboatão dos Guararapes
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

    # Dados Históricos (Thales)
    dados_thales = [
        {'id': 12441, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'GRAFICA PAJEU', 'ago': 5432.75, 'set': 9670.40, 'out': 6863.40},
        {'id': 15958, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'PEDRO AUGUSTO ALBUQUERQUE', 'ago': 2596.00, 'set': 0.00, 'out': 0.00},
        {'id': 16318, 'cidade': 'BELO JARDIM', 'cliente': 'MAYCON FRANKLYN', 'ago': 1712.85, 'set': 1736.00, 'out': 0.00},
        {'id': 16374, 'cidade': 'BELO JARDIM', 'cliente': 'BELOGRAFICA LTDA', 'ago': 0.00, 'set': 0.00, 'out': 1712.85},
        {'id': 15933, 'cidade': 'BREJINHO', 'cliente': 'EDSON GOMES CAETANO', 'ago': 1485.00, 'set': 0.00, 'out': 1725.00},
        {'id': 15891, 'cidade': 'CARUARU', 'cliente': 'JOSE CLEIDSON DA SILVA', 'ago': 2635.00, 'set': 0.00, 'out': 1960.00},
        {'id': 14647, 'cidade': 'CARUARU', 'cliente': 'CONNECT SIGN', 'ago': 1860.00, 'set': 510.00, 'out': 0.00},
        {'id': 14338, 'cidade': 'CARUARU', 'cliente': 'DECOREZ', 'ago': 0.00, 'set': 0.00, 'out': 848.00},
        {'id': 16367, 'cidade': 'CARUARU', 'cliente': 'PEVILE ESTRUTURAS', 'ago': 7465.60, 'set': 0.00, 'out': 0.00},
        {'id': 16203, 'cidade': 'CARUARU', 'cliente': 'RODRIGO FERREIRA CAVALCANTI', 'ago': 4450.00, 'set': 0.00, 'out': 0.00},
        {'id': 16224, 'cidade': 'GARANHUNS', 'cliente': 'IMPERIO GARANHUNS ALUMINIO', 'ago': 6476.00, 'set': 3014.00, 'out': 800.00},
        {'id': 15632, 'cidade': 'GOIANA', 'cliente': 'CRIART SOLUCOES GRAFICAS', 'ago': 0.00, 'set': 130.00, 'out': 0.00},
        {'id': 15354, 'cidade': 'GOIANA', 'cliente': 'GRAFICA IDEIA SINALIZACAO', 'ago': 0.00, 'set': 0.00, 'out': 315.35},
        {'id': 12014, 'cidade': 'GOIANA', 'cliente': 'RAMOS', 'ago': 425.00, 'set': 860.00, 'out': 3100.00},
        {'id': 11412, 'cidade': 'ITAMBE', 'cliente': 'ARTE NOSSA COMUNICACAO', 'ago': 892.10, 'set': 305.00, 'out': 200.00},
        {'id': 16242, 'cidade': 'ITAMBE', 'cliente': 'CARLOS DANIEL DA SILVA', 'ago': 100.00, 'set': 0.00, 'out': 0.00},
        {'id': 15117, 'cidade': 'ITAMBE', 'cliente': 'DIGIFAB', 'ago': 0.00, 'set': 1625.00, 'out': 0.00},
        {'id': 16268, 'cidade': 'ITAMBE', 'cliente': 'GILSON FERNANDO LIMA', 'ago': 3593.63, 'set': 840.00, 'out': 4993.00},
        {'id': 15746, 'cidade': 'ITAMBE', 'cliente': 'ITALO ORNILO DE LIMA', 'ago': 2730.00, 'set': 0.00, 'out': 0.00},
        {'id': 16290, 'cidade': 'JABOATAO', 'cliente': 'DRSA SUPORTE', 'ago': 0.00, 'set': 0.00, 'out': 1740.00},
        {'id': 16128, 'cidade': 'JABOATAO', 'cliente': 'POWER JEC INFORMATICA', 'ago': 0.00, 'set': 0.00, 'out': 315.00},
        {'id': 15597, 'cidade': 'LAJEDO', 'cliente': 'STUDIO 19', 'ago': 0.00, 'set': 1670.00, 'out': 965.00},
        {'id': 16269, 'cidade': 'LIMOEIRO', 'cliente': 'FJ EMPREENDIMENTOS', 'ago': 0.00, 'set': 24950.00, 'out': 0.00},
        {'id': 15720, 'cidade': 'LIMOEIRO', 'cliente': 'PLACAS FRANCA', 'ago': 2635.00, 'set': 1895.00, 'out': 0.00},
        {'id': 15259, 'cidade': 'LIMOEIRO', 'cliente': 'SAMUEL FARIAS E SILVA', 'ago': 0.00, 'set': 800.00, 'out': 0.00},
        {'id': 15425, 'cidade': 'MACAPARANA', 'cliente': 'WANDO ADESIVOS', 'ago': 1600.80, 'set': 0.00, 'out': 1256.10},
        {'id': 16282, 'cidade': 'OLINDA', 'cliente': '3 PONTOS STANDS', 'ago': 905.60, 'set': 5433.60, 'out': 0.00},
        {'id': 16234, 'cidade': 'OLINDA', 'cliente': 'IMPRIMA ON', 'ago': 180.00, 'set': 0.00, 'out': 0.00},
        {'id': 16053, 'cidade': 'OROBO', 'cliente': 'JOSE LUCAS DE ABREU', 'ago': 4300.00, 'set': 3315.00, 'out': 0.00},
        {'id': 14912, 'cidade': 'PETROLANDIA', 'cliente': 'MM COMUNICACOES', 'ago': 4992.30, 'set': 3866.00, 'out': 5980.05},
        {'id': 15206, 'cidade': 'PETROLINA', 'cliente': '3S SOLUCOES VISUAIS', 'ago': 0.00, 'set': 6055.00, 'out': 0.00},
        {'id': 15999, 'cidade': 'PETROLINA', 'cliente': 'BANDEIRANTE COMUNICACAO', 'ago': 8860.00, 'set': 7018.00, 'out': 0.00},
        {'id': 16229, 'cidade': 'PETROLINA', 'cliente': 'IMPERIO ALUMINIOS', 'ago': 6631.00, 'set': 10120.11, 'out': 7447.70},
        {'id': 16284, 'cidade': 'PETROLINA', 'cliente': 'JOAO DE ANDRADE SILVA', 'ago': 0.00, 'set': 3745.00, 'out': 0.00},
        {'id': 16255, 'cidade': 'POMBOS', 'cliente': 'MICHELSON MELO GOMES', 'ago': 0.00, 'set': 0.00, 'out': 1755.00},
        {'id': 14436, 'cidade': 'RECIFE', 'cliente': 'BL GRAFICA', 'ago': 14667.05, 'set': 29316.99, 'out': 33057.25},
        {'id': 13759, 'cidade': 'RECIFE', 'cliente': 'FMP SOLUCOES', 'ago': 0.00, 'set': 0.00, 'out': 860.00},
        {'id': 16138, 'cidade': 'RECIFE', 'cliente': 'IGREJAS ASSOCIACAO PE', 'ago': 0.00, 'set': 1130.00, 'out': 0.00},
        {'id': 15623, 'cidade': 'RECIFE', 'cliente': 'JVL OFFICE', 'ago': 0.00, 'set': 0.00, 'out': 2172.10},
        {'id': 14645, 'cidade': 'RECIFE', 'cliente': 'MULTPACK ACABAMENTOS', 'ago': 8093.55, 'set': 18112.65, 'out': 8017.38},
        {'id': 14399, 'cidade': 'RECIFE', 'cliente': 'N1 TONERS', 'ago': 3725.83, 'set': 2050.00, 'out': 0.00},
        {'id': 14800, 'cidade': 'RECIFE', 'cliente': 'VISUAL PROJETA', 'ago': 6930.00, 'set': 0.00, 'out': 3105.00},
        {'id': 11129, 'cidade': 'RECIFE', 'cliente': 'WPRINTER SOLUCOES', 'ago': 476.90, 'set': 29013.33, 'out': 0.00},
        {'id': 14934, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'JB PLACAS', 'ago': 0.00, 'set': 0.00, 'out': 2200.00},
        {'id': 12807, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'SIGN DIGITAL', 'ago': 0.00, 'set': 1020.00, 'out': 0.00},
        {'id': 12834, 'cidade': 'SAO JOSE DO EGITO', 'cliente': 'CARLOS CHAVEIRO', 'ago': 5642.40, 'set': 0.00, 'out': 3565.20},
        {'id': 13802, 'cidade': 'SAO JOSE DO EGITO', 'cliente': 'DESTAK COMUNIC', 'ago': 3786.50, 'set': 0.00, 'out': 0.00},
        {'id': 15163, 'cidade': 'SAO JOSE DO EGITO', 'cliente': 'GRAFICA RAPIDA CRIATIVA', 'ago': 1610.00, 'set': 1177.00, 'out': 660.00},
        {'id': 14050, 'cidade': 'SAO LOURENCO DA MATA', 'cliente': 'ACS PRINT', 'ago': 1921.36, 'set': 0.00, 'out': 0.00},
        {'id': 15685, 'cidade': 'SAO LOURENCO DA MATA', 'cliente': 'NGRAPH', 'ago': 2329.87, 'set': 775.00, 'out': 0.00},
        {'id': 15233, 'cidade': 'SAO VICENTE FERRER', 'cliente': 'ISAQUE ADESIVOS', 'ago': 1854.00, 'set': 5768.62, 'out': 14996.22},
        {'id': 15001, 'cidade': 'SERRA TALHADA', 'cliente': 'APLICK FILM', 'ago': 0.00, 'set': 2369.00, 'out': 0.00},
        {'id': 16231, 'cidade': 'SERRA TALHADA', 'cliente': 'ELETRO CONSULT', 'ago': 0.00, 'set': 0.00, 'out': 1044.00},
        {'id': 12862, 'cidade': 'SERRA TALHADA', 'cliente': 'SERIPLACAS DIGITAL', 'ago': 20821.47, 'set': 1900.00, 'out': 12089.10},
        {'id': 15803, 'cidade': 'SERRA TALHADA', 'cliente': 'SERTAO PLACAS', 'ago': 3106.00, 'set': 4084.00, 'out': 0.00},
        {'id': 11495, 'cidade': 'SERRA TALHADA', 'cliente': 'SUJIL ARTES', 'ago': 6407.00, 'set': 8850.00, 'out': 0.00},
        {'id': 15642, 'cidade': 'TABIRA', 'cliente': 'ARTGRAFICA DIGITAL', 'ago': 2141.89, 'set': 1071.98, 'out': 1660.11},
        {'id': 16330, 'cidade': 'TABIRA', 'cliente': 'JOSE RUFINO DE LUCENA', 'ago': 0.00, 'set': 0.00, 'out': 3956.00},
        {'id': 16182, 'cidade': 'TABIRA', 'cliente': 'TABIRA GELO', 'ago': 0.00, 'set': 0.00, 'out': 445.00},
        {'id': 14433, 'cidade': 'TABIRA', 'cliente': 'TABIRA PLACAS', 'ago': 7995.00, 'set': 11822.00, 'out': 5169.99},
        {'id': 15760, 'cidade': 'TIMBAUBA', 'cliente': 'JOSE ROBERTO DE SOUZA', 'ago': 0.00, 'set': 0.00, 'out': 435.00},
        {'id': 15962, 'cidade': 'TIMBAUBA', 'cliente': 'LEANDRO DE OLIVEIRA', 'ago': 1768.10, 'set': 610.00, 'out': 2337.00},
        {'id': 14818, 'cidade': 'TIMBAUBA', 'cliente': 'MARLON LOPES', 'ago': 2290.35, 'set': 5770.59, 'out': 0.00},
        {'id': 16316, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'JOSE MICLEYTON', 'ago': 0.00, 'set': 764.00, 'out': 924.00},
        {'id': 15603, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'ARTE DESIGN GRAFICA', 'ago': 0.00, 'set': 1582.95, 'out': 898.65},
        {'id': 15698, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'ATTELIER COMUNICACAO', 'ago': 6231.00, 'set': 5572.00, 'out': 11203.00},
        {'id': 16246, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'FX GRAFICOS', 'ago': 1050.00, 'set': 0.00, 'out': 0.00},
        {'id': 16248, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'GURY ARTES', 'ago': 430.00, 'set': 0.00, 'out': 0.00},
        {'id': 15606, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'MV IMMEDIATE SOLUTIONS', 'ago': 543.40, 'set': 7918.95, 'out': 0.00},
    ]

    # Dados Novembro
    dados_nov = [
        {'id': 10672, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'GMF INFORMATICA', 'nov': 2060.60, 'vendedor': 'POLLYANNA'},
        {'id': 16413, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'BRENO HENRIQUE', 'nov': 4050.00, 'vendedor': 'HYGOR'},
        {'id': 12441, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'GRAFICA PAJEU', 'nov': 7973.30, 'vendedor': 'VALDIR'},
        {'id': 15958, 'cidade': 'AFOGADOS DA INGAZEIRA', 'cliente': 'PEDRO AUGUSTO', 'nov': 3550.00, 'vendedor': 'VALDIR'},
        {'id': 16318, 'cidade': 'BELO JARDIM', 'cliente': 'MAYCON FRANKLYN', 'nov': 1866.40, 'vendedor': 'VALDIR'},
        {'id': 15524, 'cidade': 'CARUARU', 'cliente': 'ACTION INK PREMIUM', 'nov': 1986.50, 'vendedor': 'POLLYANNA'},
        {'id': 16415, 'cidade': 'CARUARU', 'cliente': 'JHS PAPEIS', 'nov': 450.00, 'vendedor': 'POLLYANNA'},
        {'id': 16057, 'cidade': 'CARUARU', 'cliente': 'AR PLACAS', 'nov': 1422.00, 'vendedor': 'HYGOR'},
        {'id': 12972, 'cidade': 'CARUARU', 'cliente': 'BRIND GRAF', 'nov': 2736.00, 'vendedor': 'HYGOR'},
        {'id': 15988, 'cidade': 'CARUARU', 'cliente': 'COLOR GRAF', 'nov': 15320.80, 'vendedor': 'HYGOR'},
        {'id': 16161, 'cidade': 'CARUARU', 'cliente': 'COMUNIKAR', 'nov': 2933.23, 'vendedor': 'HYGOR'},
        {'id': 12968, 'cidade': 'CARUARU', 'cliente': 'ROSAEL HENRIQUE', 'nov': 18368.40, 'vendedor': 'HYGOR'},
        {'id': 16166, 'cidade': 'CARUARU', 'cliente': 'SINALIZAR.LED', 'nov': 1450.00, 'vendedor': 'HYGOR'},
        {'id': 16113, 'cidade': 'CARUARU', 'cliente': 'ZE RAUTER LTDA', 'nov': 7000.00, 'vendedor': 'HYGOR'},
        {'id': 14338, 'cidade': 'CARUARU', 'cliente': 'DECOREZ', 'nov': 508.00, 'vendedor': 'WILSON'},
        {'id': 16329, 'cidade': 'CARUARU', 'cliente': 'INOVARTE', 'nov': 5625.50, 'vendedor': 'RENATO'},
        {'id': 16391, 'cidade': 'CARUARU', 'cliente': 'IDEIAGRAF DIGITAL', 'nov': 7181.10, 'vendedor': 'VALDIR'},
        {'id': 16389, 'cidade': 'CARUARU', 'cliente': 'ODON GRAF', 'nov': 3100.00, 'vendedor': 'VALDIR'},
        {'id': 12962, 'cidade': 'CARUARU', 'cliente': 'POLLY GRAFICA', 'nov': 1848.70, 'vendedor': 'VALDIR'},
        {'id': 13258, 'cidade': 'GARANHUNS', 'cliente': 'MTM COMERCIO', 'nov': 1000.50, 'vendedor': 'POLLYANNA'},
        {'id': 15889, 'cidade': 'GARANHUNS', 'cliente': 'GAMA DESIGN', 'nov': 1452.20, 'vendedor': 'HYGOR'},
        {'id': 15649, 'cidade': 'GARANHUNS', 'cliente': 'GRAFICA GARANHUNS', 'nov': 2535.00, 'vendedor': 'HYGOR'},
        {'id': 15659, 'cidade': 'GARANHUNS', 'cliente': 'GRAFICA GUGA', 'nov': 4020.06, 'vendedor': 'HYGOR'},
        {'id': 15955, 'cidade': 'GARANHUNS', 'cliente': 'GRAFICA STUDIO C', 'nov': 7205.00, 'vendedor': 'HYGOR'},
        {'id': 15886, 'cidade': 'GARANHUNS', 'cliente': 'JAIRO COMUNICACAO', 'nov': 7266.00, 'vendedor': 'HYGOR'},
        {'id': 15888, 'cidade': 'GARANHUNS', 'cliente': 'NEW LINE GRAFICA', 'nov': 3464.40, 'vendedor': 'HYGOR'},
        {'id': 15710, 'cidade': 'GARANHUNS', 'cliente': 'OITO7 GRAFICA', 'nov': 3248.45, 'vendedor': 'HYGOR'},
        {'id': 16417, 'cidade': 'GARANHUNS', 'cliente': 'JOSE ALDO DOS SANTOS', 'nov': 945.00, 'vendedor': 'RENATO'},
        {'id': 16224, 'cidade': 'GARANHUNS', 'cliente': 'IMPERIO GARANHUNS', 'nov': 1910.00, 'vendedor': 'VALDIR'},
        {'id': 10547, 'cidade': 'GOIANA', 'cliente': 'MEGA CENTER INFORMATICA', 'nov': 732.00, 'vendedor': 'POLLYANNA'},
        {'id': 15641, 'cidade': 'GOIANA', 'cliente': 'GOIANENSE DIGITAL', 'nov': 6174.40, 'vendedor': 'HYGOR'},
        {'id': 12483, 'cidade': 'GOIANA', 'cliente': 'KCL DIGITAL', 'nov': 6637.10, 'vendedor': 'HYGOR'},
        {'id': 16074, 'cidade': 'GOIANA', 'cliente': 'KEVEN NICOLAS', 'nov': 430.00, 'vendedor': 'HYGOR'},
        {'id': 13329, 'cidade': 'GOIANA', 'cliente': 'M G SINALIZA', 'nov': 2327.00, 'vendedor': 'HYGOR'},
        {'id': 14734, 'cidade': 'GOIANA', 'cliente': 'RM SINALIZACAO', 'nov': 7289.00, 'vendedor': 'HYGOR'},
        {'id': 15542, 'cidade': 'GOIANA', 'cliente': 'SIMAO LASER ART', 'nov': 1320.00, 'vendedor': 'HYGOR'},
        {'id': 15632, 'cidade': 'GOIANA', 'cliente': 'CRIART SOLUCOES', 'nov': 370.00, 'vendedor': 'VALDIR'},
        {'id': 16242, 'cidade': 'ITAMBE', 'cliente': 'CARLOS DANIEL', 'nov': 100.00, 'vendedor': 'POLLYANNA'},
        {'id': 15774, 'cidade': 'ITAMBE', 'cliente': 'RECICLEINFO', 'nov': 105.00, 'vendedor': 'POLLYANNA'},
        {'id': 15877, 'cidade': 'ITAMBE', 'cliente': 'IDEA CRIACAO', 'nov': 1290.00, 'vendedor': 'HYGOR'},
        {'id': 15117, 'cidade': 'ITAMBE', 'cliente': 'DIGIFAB', 'nov': 1374.00, 'vendedor': 'VALDIR'},
        {'id': 16290, 'cidade': 'JABOATAO', 'cliente': 'DRSA SUPORTE', 'nov': 3956.80, 'vendedor': 'POLLYANNA'},
        {'id': 15373, 'cidade': 'JABOATAO', 'cliente': 'ESB GRAPHICS', 'nov': 885.00, 'vendedor': 'POLLYANNA'},
        {'id': 11512, 'cidade': 'JABOATAO', 'cliente': 'REDE OFFICE', 'nov': 2718.70, 'vendedor': 'POLLYANNA'},
        {'id': 14776, 'cidade': 'JABOATAO', 'cliente': 'DIGITAL GRAFICA', 'nov': 1200.15, 'vendedor': 'HYGOR'},
        {'id': 16196, 'cidade': 'JABOATAO', 'cliente': 'FARMACIA DIARIAMENTE', 'nov': 2435.00, 'vendedor': 'HYGOR'},
        {'id': 16398, 'cidade': 'JABOATAO', 'cliente': 'OTAVIO GONCALVES', 'nov': 897.60, 'vendedor': 'HYGOR'},
        {'id': 16387, 'cidade': 'JABOATAO', 'cliente': 'FABIO NASCIMENTO', 'nov': 6920.00, 'vendedor': 'RENATO'},
        {'id': 16294, 'cidade': 'JABOATAO', 'cliente': 'JEFFERSON JOSE', 'nov': 1355.00, 'vendedor': 'RENATO'},
        {'id': 16342, 'cidade': 'JABOATAO', 'cliente': 'PAULO DE LIRA', 'nov': 1390.00, 'vendedor': 'RENATO'},
        {'id': 12799, 'cidade': 'JABOATAO', 'cliente': 'ROBERTO LIDER', 'nov': 2370.00, 'vendedor': 'RENATO'},
        {'id': 14984, 'cidade': 'JABOATAO', 'cliente': 'IMAGEM GRAFICA', 'nov': 567.00, 'vendedor': 'VALDIR'},
        {'id': 14928, 'cidade': 'JABOATAO', 'cliente': 'PONTO1 GRAF', 'nov': 280.00, 'vendedor': 'VALDIR'},
        {'id': 12541, 'cidade': 'LIMOEIRO', 'cliente': 'CASA DA INFORMATICA', 'nov': 1091.00, 'vendedor': 'POLLYANNA'},
        {'id': 11010, 'cidade': 'LIMOEIRO', 'cliente': 'SOS CARTUCHO', 'nov': 2577.40, 'vendedor': 'POLLYANNA'},
        {'id': 10414, 'cidade': 'LIMOEIRO', 'cliente': 'WORLD NET', 'nov': 1219.00, 'vendedor': 'POLLYANNA'},
        {'id': 14430, 'cidade': 'LIMOEIRO', 'cliente': 'ALPRINT GRAFICA', 'nov': 2687.95, 'vendedor': 'HYGOR'},
        {'id': 14939, 'cidade': 'LIMOEIRO', 'cliente': 'SIGN ART', 'nov': 3643.00, 'vendedor': 'HYGOR'},
        {'id': 15504, 'cidade': 'LIMOEIRO', 'cliente': 'XTREME GRAFICOS', 'nov': 3593.47, 'vendedor': 'HYGOR'},
        {'id': 15753, 'cidade': 'LIMOEIRO', 'cliente': 'LM MULTIMARCAS', 'nov': 1640.00, 'vendedor': 'VALDIR'},
        {'id': 12738, 'cidade': 'MACAPARANA', 'cliente': 'RODRIGO FILMS', 'nov': 17915.95, 'vendedor': 'HYGOR'},
        {'id': 15425, 'cidade': 'MACAPARANA', 'cliente': 'WANDO ADESIVOS', 'nov': 406.40, 'vendedor': 'VALDIR'},
        {'id': 15513, 'cidade': 'OLINDA', 'cliente': 'KATIANA SALES', 'nov': 1144.80, 'vendedor': 'HYGOR'},
        {'id': 15324, 'cidade': 'OLINDA', 'cliente': 'PONTO X DIGITAL', 'nov': 3477.85, 'vendedor': 'HYGOR'},
        {'id': 15222, 'cidade': 'OLINDA', 'cliente': 'GV TECNOLOGIA', 'nov': 517.00, 'vendedor': 'ALEXANDRE'},
        {'id': 16244, 'cidade': 'OLINDA', 'cliente': 'ALEXANDRE SEVERINO', 'nov': 3144.00, 'vendedor': 'WILSON'},
        {'id': 16313, 'cidade': 'OLINDA', 'cliente': 'RAMISON DAS NEVES', 'nov': 1547.40, 'vendedor': 'RENATO'},
        {'id': 16279, 'cidade': 'OLINDA', 'cliente': 'ELEVMETAL', 'nov': 3256.00, 'vendedor': 'RENATO'},
        {'id': 16339, 'cidade': 'OLINDA', 'cliente': 'ANTONIO JOSE GOMES', 'nov': 698.00, 'vendedor': 'VALDIR'},
        {'id': 15899, 'cidade': 'OLINDA', 'cliente': 'BUREAU DE IMAGENS', 'nov': 6300.00, 'vendedor': 'VALDIR'},
        {'id': 16053, 'cidade': 'OROBO', 'cliente': 'JOSE LUCAS DE ABREU', 'nov': 540.00, 'vendedor': 'VALDIR'},
        {'id': 14917, 'cidade': 'PETROLANDIA', 'cliente': 'MM COMUNICACOES', 'nov': 2041.00, 'vendedor': 'VALDIR'},
        {'id': 11026, 'cidade': 'PETROLINA', 'cliente': 'CLIPS PAPELARIA', 'nov': 3857.15, 'vendedor': 'MISTO'},
        {'id': 16406, 'cidade': 'PETROLINA', 'cliente': 'APS INDUSTRIA', 'nov': 40188.00, 'vendedor': 'HYGOR'},
        {'id': 14737, 'cidade': 'PETROLINA', 'cliente': 'F5 SERVICOS', 'nov': 3164.73, 'vendedor': 'HYGOR'},
        {'id': 15706, 'cidade': 'PETROLINA', 'cliente': '3 S SOLUCOES', 'nov': 1290.00, 'vendedor': 'VALDIR'},
        {'id': 16255, 'cidade': 'POMBOS', 'cliente': 'MICHELSON MELO', 'nov': 1155.00, 'vendedor': 'POLLYANNA'},
        {'id': 16337, 'cidade': 'POMBOS', 'cliente': 'JOSE HERMENEGILDO', 'nov': 1591.00, 'vendedor': 'HYGOR'},
        {'id': 16333, 'cidade': 'POMBOS', 'cliente': 'WELLINGTON FERNANDO', 'nov': 1409.00, 'vendedor': 'HYGOR'},
        {'id': 11100, 'cidade': 'RECIFE', 'cliente': 'CASA DAS COPIAS', 'nov': 630.00, 'vendedor': 'POLLYANNA'},
        {'id': 15961, 'cidade': 'RECIFE', 'cliente': 'COLOR +', 'nov': 1504.80, 'vendedor': 'POLLYANNA'},
        {'id': 11000, 'cidade': 'RECIFE', 'cliente': 'CONEXAO DIGITAL', 'nov': 494.50, 'vendedor': 'POLLYANNA'},
        {'id': 16392, 'cidade': 'RECIFE', 'cliente': 'FILIPE CONSERTO', 'nov': 1148.00, 'vendedor': 'POLLYANNA'},
        {'id': 13759, 'cidade': 'RECIFE', 'cliente': 'FMD SOLUCOES', 'nov': 2664.00, 'vendedor': 'POLLYANNA'},
        {'id': 13939, 'cidade': 'RECIFE', 'cliente': 'GRAFIX', 'nov': 870.00, 'vendedor': 'POLLYANNA'},
        {'id': 11397, 'cidade': 'RECIFE', 'cliente': 'HI FI INFORMATICA', 'nov': 538.60, 'vendedor': 'POLLYANNA'},
        {'id': 15623, 'cidade': 'RECIFE', 'cliente': 'JVL OFFICE', 'nov': 2827.50, 'vendedor': 'MISTO'},
        {'id': 13514, 'cidade': 'RECIFE', 'cliente': 'LEGITIMA IMPRESSAO', 'nov': 804.00, 'vendedor': 'POLLYANNA'},
        {'id': 14977, 'cidade': 'RECIFE', 'cliente': 'MANTEL INFO SERVICE', 'nov': 2010.00, 'vendedor': 'POLLYANNA'},
        {'id': 13678, 'cidade': 'RECIFE', 'cliente': 'MERAKI TECNOLOGIA', 'nov': 1277.50, 'vendedor': 'POLLYANNA'},
        {'id': 10381, 'cidade': 'RECIFE', 'cliente': 'MILPRINT TECNOLOGIA', 'nov': 768.00, 'vendedor': 'POLLYANNA'},
        {'id': 11015, 'cidade': 'RECIFE', 'cliente': 'R GRAPH', 'nov': 1501.50, 'vendedor': 'POLLYANNA'},
        {'id': 12018, 'cidade': 'RECIFE', 'cliente': 'R&F INFORMATICA', 'nov': 1577.00, 'vendedor': 'POLLYANNA'},
        {'id': 13202, 'cidade': 'RECIFE', 'cliente': 'TONER MAX', 'nov': 3939.40, 'vendedor': 'POLLYANNA'},
        {'id': 11129, 'cidade': 'RECIFE', 'cliente': 'WPRINTER SOLUCOES', 'nov': 1518.10, 'vendedor': 'POLLYANNA'},
        {'id': 12752, 'cidade': 'RECIFE', 'cliente': 'CAROL GRAFICA', 'nov': 1251.25, 'vendedor': 'HYGOR'},
        {'id': 16403, 'cidade': 'RECIFE', 'cliente': 'CASA DAS PLACAS', 'nov': 820.00, 'vendedor': 'HYGOR'},
        {'id': 16253, 'cidade': 'RECIFE', 'cliente': 'CASA DO LASER', 'nov': 2236.45, 'vendedor': 'HYGOR'},
        {'id': 12482, 'cidade': 'RECIFE', 'cliente': 'EXPOMETAL', 'nov': 4990.00, 'vendedor': 'HYGOR'},
        {'id': 13021, 'cidade': 'RECIFE', 'cliente': 'INFOCOLOR GRAFICA', 'nov': 1668.30, 'vendedor': 'HYGOR'},
        {'id': 14174, 'cidade': 'RECIFE', 'cliente': 'MAG GRAFICA LTDA', 'nov': 3259.20, 'vendedor': 'HYGOR'},
        {'id': 11929, 'cidade': 'RECIFE', 'cliente': 'PRINT JET - PE', 'nov': 39620.10, 'vendedor': 'HYGOR'},
        {'id': 15286, 'cidade': 'RECIFE', 'cliente': 'RECIFE CORTES', 'nov': 572.00, 'vendedor': 'HYGOR'},
        {'id': 14388, 'cidade': 'RECIFE', 'cliente': 'RG MIDIA EXTERIOR', 'nov': 800.00, 'vendedor': 'HYGOR'},
        {'id': 14389, 'cidade': 'RECIFE', 'cliente': 'SUPRI GRAFICA DIGITAL', 'nov': 30444.50, 'vendedor': 'HYGOR'},
        {'id': 14600, 'cidade': 'RECIFE', 'cliente': 'INNOVATECH', 'nov': 252.00, 'vendedor': 'ALEXANDRE'},
        {'id': 14399, 'cidade': 'RECIFE', 'cliente': 'N1 TONERS', 'nov': 1290.00, 'vendedor': 'ALEXANDRE'},
        {'id': 12790, 'cidade': 'RECIFE', 'cliente': 'ADESIVART', 'nov': 1080.15, 'vendedor': 'WILSON'},
        {'id': 16386, 'cidade': 'RECIFE', 'cliente': 'MAURICLEIDE QUIRINO', 'nov': 840.00, 'vendedor': 'RENATO'},
        {'id': 14436, 'cidade': 'RECIFE', 'cliente': 'BL GRAFICA', 'nov': 12558.27, 'vendedor': 'RENATO'},
        {'id': 12858, 'cidade': 'RECIFE', 'cliente': 'COMPLACAS', 'nov': 4759.40, 'vendedor': 'RENATO'},
        {'id': 12866, 'cidade': 'RECIFE', 'cliente': 'COOPERATIVA DIGITAL', 'nov': 2332.00, 'vendedor': 'RENATO'},
        {'id': 16358, 'cidade': 'RECIFE', 'cliente': 'EMERSON ANDRE', 'nov': 32985.00, 'vendedor': 'RENATO'},
        {'id': 16334, 'cidade': 'RECIFE', 'cliente': 'JOSE ALVES DE LIMA', 'nov': 3875.00, 'vendedor': 'RENATO'},
        {'id': 16286, 'cidade': 'RECIFE', 'cliente': 'JOSE FARIAS', 'nov': 2440.00, 'vendedor': 'RENATO'},
        {'id': 16327, 'cidade': 'RECIFE', 'cliente': 'NERIVALDO BATISTA', 'nov': 2310.00, 'vendedor': 'RENATO'},
        {'id': 11969, 'cidade': 'RECIFE', 'cliente': 'NOW+PRINT', 'nov': 3090.00, 'vendedor': 'RENATO'},
        {'id': 14994, 'cidade': 'RECIFE', 'cliente': 'PENSE ARTE', 'nov': 1173.80, 'vendedor': 'RENATO'},
        {'id': 16430, 'cidade': 'RECIFE', 'cliente': 'RICARDO ALEXANDRE', 'nov': 406.40, 'vendedor': 'RENATO'},
        {'id': 16412, 'cidade': 'RECIFE', 'cliente': 'VANESSA TALITA', 'nov': 2310.30, 'vendedor': 'RENATO'},
        {'id': 14800, 'cidade': 'RECIFE', 'cliente': 'VISUAL PROJETA', 'nov': 4470.20, 'vendedor': 'RENATO'},
        {'id': 16341, 'cidade': 'RECIFE', 'cliente': 'CARLA BEATRIZ', 'nov': 874.00, 'vendedor': 'VALDIR'},
        {'id': 16428, 'cidade': 'RECIFE', 'cliente': 'CLIPPES DIGITAL', 'nov': 472.00, 'vendedor': 'VALDIR'},
        {'id': 16405, 'cidade': 'RECIFE', 'cliente': 'CONSULT DESIGN', 'nov': 400.00, 'vendedor': 'VALDIR'},
        {'id': 16399, 'cidade': 'RECIFE', 'cliente': 'GRAFICA MORI', 'nov': 1790.00, 'vendedor': 'VALDIR'},
        {'id': 16138, 'cidade': 'RECIFE', 'cliente': 'IGREJAS ASSOCIACAO PE', 'nov': 4300.00, 'vendedor': 'VALDIR'},
        {'id': 14652, 'cidade': 'RECIFE', 'cliente': 'QUEIROZ SIGNAGE', 'nov': 2015.00, 'vendedor': 'VALDIR'},
        {'id': 15008, 'cidade': 'RECIFE', 'cliente': 'TRIAD VISUAL', 'nov': 3909.38, 'vendedor': 'VALDIR'},
        {'id': 10375, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'LMT COMPUTADORES', 'nov': 2059.20, 'vendedor': 'POLLYANNA'},
        {'id': 15591, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'OFICINA GRAFICA', 'nov': 2160.00, 'vendedor': 'HYGOR'},
        {'id': 14934, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'JB PLACAS', 'nov': 1840.00, 'vendedor': 'VALDIR'},
        {'id': 12807, 'cidade': 'SANTA CRUZ CAPIBARIBE', 'cliente': 'SIGN DIGITAL', 'nov': 2467.60, 'vendedor': 'VALDIR'},
        {'id': 12834, 'cidade': 'SAO JOSE DO EGITO', 'cliente': 'CARLOS CHAVEIRO', 'nov': 2906.00, 'vendedor': 'VALDIR'},
        {'id': 11249, 'cidade': 'SAO LOURENCO DA MATA', 'cliente': 'CT SUPRIMENTOS', 'nov': 1512.00, 'vendedor': 'POLLYANNA'},
        {'id': 16323, 'cidade': 'SAO LOURENCO DA MATA', 'cliente': 'RM GRAFICA', 'nov': 2520.20, 'vendedor': 'RENATO'},
        {'id': 15233, 'cidade': 'SAO VICENTE FERRER', 'cliente': 'ISAQUE ADESIVOS', 'nov': 4771.00, 'vendedor': 'VALDIR'},
        {'id': 16420, 'cidade': 'SERRA TALHADA', 'cliente': 'BRUNO ALVES', 'nov': 4290.00, 'vendedor': 'HYGOR'},
        {'id': 15184, 'cidade': 'SERRA TALHADA', 'cliente': 'DIGITAL COPIAS', 'nov': 12744.20, 'vendedor': 'HYGOR'},
        {'id': 14211, 'cidade': 'SERRA TALHADA', 'cliente': 'SERRALHARIA PAULINHO', 'nov': 5790.00, 'vendedor': 'HYGOR'},
        {'id': 12862, 'cidade': 'SERRA TALHADA', 'cliente': 'SERIPLACAS DIGITAL', 'nov': 18671.40, 'vendedor': 'VALDIR'},
        {'id': 15803, 'cidade': 'SERRA TALHADA', 'cliente': 'SERTAO PLACAS', 'nov': 2992.47, 'vendedor': 'VALDIR'},
        {'id': 15598, 'cidade': 'TABIRA', 'cliente': 'HK COMUNICACAO', 'nov': 5230.00, 'vendedor': 'HYGOR'},
        {'id': 15642, 'cidade': 'TABIRA', 'cliente': 'ARTGRAFICA DIGITAL', 'nov': 478.90, 'vendedor': 'VALDIR'},
        {'id': 16330, 'cidade': 'TABIRA', 'cliente': 'JOSE RUFINO', 'nov': 840.00, 'vendedor': 'VALDIR'},
        {'id': 14433, 'cidade': 'TABIRA', 'cliente': 'TABIRA PLACAS', 'nov': 5442.00, 'vendedor': 'VALDIR'},
        {'id': 10777, 'cidade': 'TIMBAUBA', 'cliente': 'CASA DOS CARTUCHOS', 'nov': 445.00, 'vendedor': 'POLLYANNA'},
        {'id': 10410, 'cidade': 'TIMBAUBA', 'cliente': 'TUDO.COM INFORMATICA', 'nov': 1023.10, 'vendedor': 'POLLYANNA'},
        {'id': 12053, 'cidade': 'TIMBAUBA', 'cliente': 'IMAGEM MIDIA', 'nov': 5378.90, 'vendedor': 'HYGOR'},
        {'id': 16214, 'cidade': 'TIMBAUBA', 'cliente': 'GILBERTO TAVARES', 'nov': 1120.00, 'vendedor': 'VALDIR'},
        {'id': 14818, 'cidade': 'TIMBAUBA', 'cliente': 'MARLON LOPES', 'nov': 3755.90, 'vendedor': 'VALDIR'},
        {'id': 15698, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'ATTELIER COMUNICACAO', 'nov': 13710.00, 'vendedor': 'HYGOR'},
        {'id': 16246, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'FX GRAFICOS', 'nov': 4640.80, 'vendedor': 'HYGOR'},
        {'id': 16248, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'GURY ARTES', 'nov': 3760.00, 'vendedor': 'HYGOR'},
        {'id': 16243, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'INFOARTE', 'nov': 7492.00, 'vendedor': 'HYGOR'},
        {'id': 16402, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'JEZIEL ENOQUE', 'nov': 265.00, 'vendedor': 'HYGOR'},
        {'id': 16265, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'JOSE ALFREDO', 'nov': 745.00, 'vendedor': 'HYGOR'},
        {'id': 16300, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'JOSE CARLOS DA SILVA', 'nov': 1635.00, 'vendedor': 'HYGOR'},
        {'id': 16238, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'KAL DECOR', 'nov': 736.70, 'vendedor': 'HYGOR'},
        {'id': 16263, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'MARCOS ANTONIO', 'nov': 183.60, 'vendedor': 'HYGOR'},
        {'id': 15606, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'MV IMMEDIATE', 'nov': 1066.80, 'vendedor': 'HYGOR'},
        {'id': 16233, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'PRINTYCELLO', 'nov': 3141.50, 'vendedor': 'HYGOR'},
        {'id': 12710, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'PRONTO GRAFICA', 'nov': 8837.04, 'vendedor': 'HYGOR'},
        {'id': 16267, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'RIVONALDO FERREIRA', 'nov': 1887.00, 'vendedor': 'HYGOR'},
        {'id': 16252, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'TIAGO VIEIRA', 'nov': 3997.00, 'vendedor': 'HYGOR'},
        {'id': 15022, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'TOP GRAFICA', 'nov': 2390.00, 'vendedor': 'HYGOR'},
        {'id': 16314, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'VADINHO SERRALHERIA', 'nov': 2535.00, 'vendedor': 'HYGOR'},
        {'id': 15515, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'VISAGGEM DIGITAL', 'nov': 1000.00, 'vendedor': 'HYGOR'},
        {'id': 16377, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'AURUM CONCEPT', 'nov': 4800.00, 'vendedor': 'RENATO'},
        {'id': 16332, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'LUCAS LIMA', 'nov': 1170.00, 'vendedor': 'RENATO'},
        {'id': 16307, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'MICHELL VICTOR', 'nov': 40.00, 'vendedor': 'RENATO'},
        {'id': 16296, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'ROBSON LEANDRO', 'nov': 165.00, 'vendedor': 'RENATO'},
        {'id': 16316, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'JOSE MICLEYTON', 'nov': 973.00, 'vendedor': 'VALDIR'},
        {'id': 15603, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'ARTE DESIGN GRAFICA', 'nov': 769.00, 'vendedor': 'VALDIR'},
        {'id': 16397, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'DANILO FELIPE', 'nov': 457.20, 'vendedor': 'VALDIR'},
        {'id': 16400, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'DANUSA VIEIRA', 'nov': 289.00, 'vendedor': 'VALDIR'},
        {'id': 16376, 'cidade': 'VITORIA DE SANTO ANTAO', 'cliente': 'GRAFICA POSITIVA', 'nov': 1595.50, 'vendedor': 'VALDIR'}
    ]

    return pd.DataFrame(dados_thales), pd.DataFrame(dados_nov), coords

df_thales, df_nov, coords_dict = load_data()

# --- 2. PROCESSAMENTO DE DADOS ---
# Agrupar Thales
df_thales_ag = df_thales.groupby(['id', 'cidade', 'cliente'])[['ago', 'set', 'out']].sum().reset_index()
df_thales_ag['Total_Trimestre'] = df_thales_ag['ago'] + df_thales_ag['set'] + df_thales_ag['out']
df_thales_ag['Media_Thales'] = df_thales_ag['Total_Trimestre'] / 3

# Agrupar Novembro
df_nov_ag = df_nov.groupby(['id', 'cidade', 'cliente', 'vendedor'])['nov'].sum().reset_index()

# Merge
df_full = pd.merge(df_thales_ag, df_nov_ag, on='id', how='outer', suffixes=('_ant', '_nov'))

# Limpeza
df_full['Cliente'] = df_full['cliente_nov'].combine_first(df_full['cliente_ant'])
df_full['Cidade'] = df_full['cidade_nov'].combine_first(df_full['cidade_ant'])
df_full.fillna(0, inplace=True)
df_full['vendedor'] = df_full['vendedor'].replace(0, 'Sem Venda')

# Status e Cores
def definir_status(row):
    thales_ativo = row['Media_Thales'] > 0
    nov_ativo = row['nov'] > 0
    if thales_ativo and not nov_ativo: return '🔴 Churn (Perdido)'
    elif thales_ativo and nov_ativo:
        if row['nov'] > row['Media_Thales']: return '🟢 Retido (Cresceu)'
        else: return '🔵 Retido (Caiu)'
    elif not thales_ativo and nov_ativo: return '🟡 Novo/Recuperado'
    else: return '⚪ Inativo'

df_full['Status'] = df_full.apply(definir_status, axis=1)

# Adicionar Coordenadas
def get_lat(cidade): return coords_dict.get(cidade, {}).get('lat', None)
def get_lon(cidade): return coords_dict.get(cidade, {}).get('lon', None)
df_full['lat'] = df_full['Cidade'].apply(get_lat)
df_full['lon'] = df_full['Cidade'].apply(get_lon)

# --- SIDEBAR: FILTROS INTERATIVOS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
st.sidebar.title("Comando")

cidade_filtro = st.sidebar.selectbox("🗺️ Filtrar Cidade", ['TODAS'] + sorted(df_full['Cidade'].unique().tolist()))
status_filtro = st.sidebar.multiselect("🏷️ Filtrar Status", df_full['Status'].unique(), default=df_full['Status'].unique())

# Aplicar Filtros
df_view = df_full.copy()
if cidade_filtro != 'TODAS':
    df_view = df_view[df_view['Cidade'] == cidade_filtro]
if status_filtro:
    df_view = df_view[df_view['Status'].isin(status_filtro)]

# --- HEADER: MÉTRICAS GRANDES ---
st.title("🚀 Painel de Inteligência: Transição de Carteira")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><h3>💰 Faturamento Nov</h3><h2>R$ {:,.2f}</h2></div>'.format(df_view['nov'].sum()), unsafe_allow_html=True)
with col2:
    perc_novos = df_view[df_view['Status'] == '🟡 Novo/Recuperado']['nov'].sum()
    st.markdown(f'<div class="metric-card"><h3>✨ Novos Negócios</h3><h2>R$ {perc_novos:,.2f}</h2></div>', unsafe_allow_html=True)
with col3:
    churn_val = df_view[df_view['Status'] == '🔴 Churn (Perdido)']['Media_Thales'].sum()
    st.markdown(f'<div class="metric-card"><h3>⚠️ Potencial Perdido</h3><h2 style="color:#FF4B4B">R$ {churn_val:,.2f}</h2></div>', unsafe_allow_html=True)
with col4:
    total_clientes = df_view[df_view['nov'] > 0].shape[0]
    st.markdown(f'<div class="metric-card"><h3>👥 Clientes Ativos</h3><h2>{total_clientes}</h2></div>', unsafe_allow_html=True)

st.write("") 

# --- ABAS DE ANÁLISE ---
tab_map, tab_pareto, tab_equipe, tab_retencao, tab_sim, tab_detalhe = st.tabs([
    "🗺️ Mapa", 
    "📉 Perdas (Pareto)", 
    "🏆 Equipe de Vendas", 
    "⚖️ Comparativo Clientes",
    "🎮 Simulador", 
    "📋 Tabela"
])

# --- ABA 1: MAPA GEOGRÁFICO (ATUALIZADO E LIMPO) ---
with tab_map:
    st.subheader("📍 Geografia das Vendas")
    
    # Preparação dos dados para o Mapa
    df_map = df_view.groupby(['Cidade', 'lat', 'lon'])[['nov', 'Media_Thales']].sum().reset_index()
    
    # Criar colunas formatadas para o Tooltip (para ficar R$ bonito ao passar o mouse)
    df_map['Faturamento Nov'] = df_map['nov'].apply(lambda x: f"R$ {x:,.2f}")
    df_map['Média Histórica'] = df_map['Media_Thales'].apply(lambda x: f"R$ {x:,.2f}")
    
    # Definir Status e Tamanho da Bolha
    df_map['Status_Cidade'] = df_map.apply(lambda x: 'Crescimento' if x['nov'] > x['Media_Thales'] else 'Queda', axis=1)
    # Ajuste matemático suave para a bolha não ficar nem gigante nem invisível
    df_map['Tamanho_Bolha'] = (df_map['nov'] + df_map['Media_Thales']).apply(lambda x: x**0.5) 

    # Criando o Mapa
    fig_map = px.scatter_mapbox(
        df_map, 
        lat="lat", 
        lon="lon", 
        hover_name="Cidade",
        # Aqui definimos o que aparece no mouse:
        hover_data={
            "lat": False, "lon": False, "Tamanho_Bolha": False, "Status_Cidade": False, # Esconde dados técnicos
            "Faturamento Nov": True, 
            "Média Histórica": True
        },
        size="Tamanho_Bolha", 
        color="Status_Cidade",
        color_discrete_map={'Crescimento': '#00CC96', 'Queda': '#FF4B4B'},
        zoom=6.5, # Zoom inicial um pouco mais perto
        height=600, # Mapa mais alto
        size_max=40 # Bolhas maiores
    )

    # Estilização Fina (Limpeza total)
    fig_map.update_layout(
        mapbox_style="carto-positron", # Estilo de mapa limpo (cinza claro), destaca os dados
        margin={"r":0,"t":0,"l":0,"b":0}, # Remove margens brancas, mapa sangrado
        legend=dict(
            yanchor="top",
            y=0.95,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)" # Fundo da legenda semi-transparente
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

# --- ABA 2: PARETO ---
with tab_pareto:
    st.subheader("🕵️ Maiores Clientes Perdidos")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        df_lost = df_view[df_view['Status'] == '🔴 Churn (Perdido)'].sort_values(by='Media_Thales', ascending=False).head(10)
        if not df_lost.empty:
            fig_bar = px.bar(df_lost, x='Media_Thales', y='Cliente', orientation='h', text_auto='.2s', 
                             title="Top 10 Clientes Perdidos", color_discrete_sequence=['#FF4B4B'])
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.success("Zero perdas!")

# --- ABA 3: EQUIPE DE VENDAS (NOVO) ---
with tab_equipe:
    st.subheader("🏆 Ranking de Vendedores (Novembro)")
    
    # Agrupar dados por vendedor
    df_vendedores = df_view[df_view['nov'] > 0].groupby('vendedor')['nov'].sum().reset_index().sort_values(by='nov', ascending=False)
    
    col_e1, col_e2 = st.columns([2, 1])
    
    with col_e1:
        fig_vend = px.bar(df_vendedores, x='vendedor', y='nov', text_auto='.2s',
                          title="Faturamento por Vendedor",
                          color='nov', color_continuous_scale='Teal')
        st.plotly_chart(fig_vend, use_container_width=True)
        
    with col_e2:
        fig_pie_vend = px.pie(df_vendedores, names='vendedor', values='nov', title="Share de Vendas")
        st.plotly_chart(fig_pie_vend, use_container_width=True)

# --- ABA 4: COMPARATIVO CLIENTES (NOVO) ---
with tab_retencao:
    st.subheader("⚖️ Thales vs. Atual (Mesmo Cliente)")
    st.markdown("Comparação direta de quanto o cliente comprava (Média) e quanto comprou agora.")
    
    # Filtrar apenas clientes que compraram em pelo menos um dos períodos
    df_comp = df_view[(df_view['Media_Thales'] > 0) | (df_view['nov'] > 0)].copy()
    
    # Pegar os Top 20 maiores clientes (soma dos dois períodos) para o gráfico não ficar gigante
    df_comp['Total_Volume'] = df_comp['Media_Thales'] + df_comp['nov']
    df_top20 = df_comp.sort_values(by='Total_Volume', ascending=False).head(20)
    
    # Transformar para formato longo para o gráfico agrupado
    df_long = df_top20.melt(id_vars='Cliente', value_vars=['Media_Thales', 'nov'], 
                            var_name='Periodo', value_name='Valor')
    
    fig_group = px.bar(df_long, x='Cliente', y='Valor', color='Periodo', barmode='group',
                       title="Top 20 Clientes: Antes (Thales) vs Depois (Novembro)",
                       color_discrete_map={'Media_Thales': '#FFA07A', 'nov': '#20B2AA'},
                       text_auto='.2s')
    
    st.plotly_chart(fig_group, use_container_width=True)

# --- ABA 5: SIMULADOR ---
with tab_sim:
    st.subheader("🎲 Simulador de Metas")
    col_sim1, col_sim2 = st.columns([1, 2])
    with col_sim1:
        meta = st.slider("Meta Recuperação (%)", 0, 100, 20)
    with col_sim2:
        recup = churn_val * (meta / 100)
        total_proj = df_view['nov'].sum() + recup
        st.metric("Potencial Extra", f"+ R$ {recup:,.2f}")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=total_proj, 
                                           title={'text': "Projeção"}, gauge={'bar': {'color': "#20B2AA"}}))
        st.plotly_chart(fig_gauge, use_container_width=True, height=250)

# --- ABA 6: DETALHES ---
with tab_detalhe:
    st.subheader("📋 Lista Detalhada")
    def highlight_rows(val):
        if 'Churn' in str(val): return 'background-color: #ffe6e6'
        if 'Cresceu' in str(val): return 'background-color: #e6fffa'
        return ''
    
    cols = ['id', 'Cidade', 'Cliente', 'vendedor', 'Media_Thales', 'nov', 'Status']
    st.dataframe(df_view[cols].sort_values(by='Status').style.applymap(highlight_rows, subset=['Status'])
                 .format({'Media_Thales': 'R$ {:.2f}', 'nov': 'R$ {:.2f}'}), use_container_width=True)
    
    # Botão de Download
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", data=csv, file_name="relatorio_printmais.csv", mime="text/csv")