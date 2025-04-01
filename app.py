import streamlit as st
import yfinance as yf
from google import genai
import plotly.graph_objects as go
from datetime import datetime, timedelta

###########################################################
tokenGenAI = "AIzaSyDZjMVo9-ViYTYmSN5zv3OX_AYr534yAoo"
client = genai.Client(api_key=tokenGenAI)
###########################################################


# Configuración de la aplicación
st.set_page_config(page_title="Descripción de Empresa", page_icon="📈", layout="centered")

# Estilo CSS para hacer que el buscador se parezca a Google
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            font-size: 25px;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
            width: 100%;
            text-align: center;
        }
        .stTextInput>div>div {
            display: flex;
            justify-content: center;
        }
        .stMarkdown {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.title("Riesgo Retorno de una Acción")

# Entrada de texto para el ticker
symbol = st.text_input("Ingresa el símbolo de la acción (Ej: AAPL, TSLA, MSFT)", "").upper().strip()
######  Yahooo Finance Code ############## 

end_date = datetime.today()
start_date = end_date - timedelta(days=5*365)


# Si el usuario ha ingresado un símbolo
if symbol:
    try:
        # Obtener la información de la empresa desde Yahoo Finance
        company = yf.Ticker(symbol)
        company_info = company.info
        
        # Validar si existe información
        if "longBusinessSummary" in company_info and "longName" in company_info and "website" in company_info:
            # Mostrar el nombre de la empresa como título
            st.markdown(f"## {company_info['longName']}")
            # Mostrar la descripción de la empresa
            #st.write(company_info["longBusinessSummary"])
            
            prompt = "Por favor traduce el siguiente texto al español en máximo 200 palabras :" + company_info["longBusinessSummary"]
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            st.write(response.text)
            st.write(company_info["website"])
            st.write("Sector: " + company_info["sector"])

            # Rango de tiempo: últimos 5 años desde hoy
            # Descargar precios históricos desde Yahoo Finance
            hist = company.history(start=start_date, end=end_date)
            
            # Verificamos si hay datos
            if not hist.empty:
                st.markdown("### 📊 Gráfico de Precios Históricos (5 años) 📊")

                # Crear la figura tipo velas japonesas (Candlestick)
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name='Precio'
                )])

                # Personalización del gráfico
                fig.update_layout(
                    xaxis_title="Fecha",
                    yaxis_title="Precio (USD)",
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark",
                    height=600
                )

                # Mostrar el gráfico en Streamlit
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ No se encontraron datos históricos para este símbolo.")

        else:
            st.warning("⚠ No se encontró una descripción para esta empresa en Yahoo Finance.")
    
    except Exception as e:
        st.error("❌ Ocurrió un error al obtener los datos. Verifica que el símbolo sea correcto.")

from google import genai

