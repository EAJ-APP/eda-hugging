# app.py - Archivo principal para HuggingFace Spaces
import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
import json
import warnings
from datetime import datetime, date

# Suprimir warnings
warnings.filterwarnings("ignore")

# Configuración de la app
TITLE = "📊 GA4 Explorer - Análisis de Consentimiento"
DESCRIPTION = """
## 🍪 Analizador de Consentimiento GA4

Esta herramienta analiza los datos de consentimiento de cookies en Google Analytics 4.

### 📋 Instrucciones:
1. Introduce tu **Proyecto GCP** y **Dataset GA4**
2. Selecciona el **rango de fechas**
3. Pega las **credenciales JSON** de tu cuenta de servicio
4. Haz clic en **Analizar** para ver los resultados

### 🔑 Credenciales:
Necesitas un archivo JSON de cuenta de servicio con permisos de BigQuery.
"""

def format_date_for_bq(date_input):
    """Convierte fecha a formato BigQuery"""
    if isinstance(date_input, str):
        return date_input.replace('-', '')
    return date_input.strftime('%Y%m%d')

def analyze_basic_consent(project, dataset, start_date, end_date, credentials_json):
    """Análisis básico de consentimiento"""
    if not all([project, dataset, start_date, end_date, credentials_json]):
        return "⚠️ Por favor completa todos los campos", None, None
    
    try:
        # Configurar cliente BigQuery
        creds_dict = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = bigquery.Client(credentials=credentials)
        
        # Formatear fechas
        start_date_str = format_date_for_bq(start_date)
        end_date_str = format_date_for_bq(end_date)
        
        # Consulta básica
        query = f"""
        SELECT
          privacy_info.analytics_storage AS analytics_storage_status,
          privacy_info.ads_storage AS ads_storage_status,
          COUNT(*) AS total_events,
          COUNT(DISTINCT user_pseudo_id) AS total_users
        FROM `{project}.{dataset}.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '{start_date_str}' AND '{end_date_str}'
        GROUP BY 1, 2
        ORDER BY 3 DESC
        """
        
        df = client.query(query).to_dataframe()
        
        if df.empty:
            return "📭 No se encontraron datos para el rango seleccionado", None, None
        
        # Crear tabla HTML
        table_html = df.to_html(index=False, classes='table table-striped')
        
        # Crear gráfico de pastel
        fig_pie = px.pie(df, 
                        names='analytics_storage_status', 
                        values='total_events',
                        title='📊 Distribución de Consentimiento Analytics',
                        color_discrete_map={
                            'true': '#4CAF50',
                            'false': '#F44336', 
                            'null': '#FFC107',
                            None: '#9E9E9E'
                        })
        
        # Crear gráfico de barras
        fig_bar = px.bar(df,
                        x='ads_storage_status',
                        y='total_users', 
                        title='👥 Usuarios por Consentimiento de Ads',
                        color='ads_storage_status',
                        color_discrete_map={
                            'true': '#4CAF50',
                            'false': '#F44336',
                            'null': '#FFC107',
                            None: '#9E9E9E'
                        })
        
        return table_html, fig_pie, fig_bar
        
    except json.JSONDecodeError:
        return "❌ Error: Credenciales JSON inválidas", None, None
    except Exception as e:
        return f"❌ Error: {str(e)}", None, None

def analyze_device_consent(project, dataset, start_date, end_date, credentials_json):
    """Análisis de consentimiento por dispositivo"""
    if not all([project, dataset, start_date, end_date, credentials_json]):
        return "⚠️ Por favor completa todos los campos", None
    
    try:
        # Configurar cliente BigQuery
        creds_dict = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = bigquery.Client(credentials=credentials)
        
        # Formatear fechas
        start_date_str = format_date_for_bq(start_date)
        end_date_str = format_date_for_bq(end_date)
        
        # Consulta por dispositivo
        query = f"""
        SELECT
            device.category AS device_type,
            CASE
                WHEN privacy_info.analytics_storage IS NULL THEN 'No Definido'
                WHEN LOWER(CAST(privacy_info.analytics_storage AS STRING)) IN ('false', 'no', '0') THEN 'Denegado'
                ELSE 'Aceptado'
            END AS consent_status,
            COUNT(*) AS total_events
        FROM `{project}.{dataset}.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '{start_date_str}' AND '{end_date_str}'
        GROUP BY 1, 2
        ORDER BY 1, 3 DESC
        """
        
        df = client.query(query).to_dataframe()
        
        if df.empty:
            return "📭 No se encontraron datos para el rango seleccionado", None
        
        # Crear gráfico apilado
        fig = px.bar(df,
                    x='device_type',
                    y='total_events',
                    color='consent_status',
                    title='📱 Consentimiento por Tipo de Dispositivo',
                    barmode='stack',
                    color_discrete_map={
                        'Aceptado': '#4CAF50',
                        'Denegado': '#F44336',
                        'No Definido': '#FFC107'
                    })
        
        # Tabla HTML
        table_html = df.to_html(index=False, classes='table table-striped')
        
        return table_html, fig
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Crear interfaz Gradio
with gr.Blocks(title="GA4 Explorer", theme=gr.themes.Soft()) as app:
    
    gr.Markdown(DESCRIPTION)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔧 Configuración")
            
            project = gr.Textbox(
                label="🏢 Proyecto GCP", 
                placeholder="mi-proyecto-ga4-123",
                info="El ID de tu proyecto en Google Cloud Platform"
            )
            
            dataset = gr.Textbox(
                label="📊 Dataset GA4", 
                placeholder="analytics_123456789",
                info="El nombre de tu dataset de GA4 en BigQuery"
            )
            
            with gr.Row():
                start_date = gr.Textbox(
                    label="📅 Fecha inicio", 
                    placeholder="2024-01-01",
                    info="Formato: YYYY-MM-DD"
                )
                end_date = gr.Textbox(
                    label="📅 Fecha fin", 
                    placeholder="2024-01-31",
                    info="Formato: YYYY-MM-DD"
                )
            
            credentials = gr.TextArea(
                label="🔑 Credenciales JSON",
                placeholder="{\n  \"type\": \"service_account\",\n  \"project_id\": \"...\",\n  ...\n}",
                lines=8,
                info="Pega aquí el contenido completo del archivo JSON de tu cuenta de servicio"
            )
        
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Resultados")
            
            with gr.Tab("🛡️ Análisis Básico"):
                basic_btn = gr.Button("🔍 Analizar Consentimiento Básico", variant="primary", size="lg")
                basic_table = gr.HTML(label="📋 Datos")
                
                with gr.Row():
                    basic_pie = gr.Plot(label="📊 Analytics Storage")
                    basic_bar = gr.Plot(label="📊 Ads Storage") 
                
                basic_btn.click(
                    fn=analyze_basic_consent,
                    inputs=[project, dataset, start_date, end_date, credentials],
                    outputs=[basic_table, basic_pie, basic_bar]
                )
            
            with gr.Tab("📱 Por Dispositivo"):
                device_btn = gr.Button("🔍 Analizar por Dispositivo", variant="secondary", size="lg")
                device_table = gr.HTML(label="📋 Datos por Dispositivo")
                device_chart = gr.Plot(label="📊 Gráfico por Dispositivo")
                
                device_btn.click(
                    fn=analyze_device_consent,
                    inputs=[project, dataset, start_date, end_date, credentials],
                    outputs=[device_table, device_chart]
                )

# Configurar app
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # HuggingFace maneja el sharing
    )
