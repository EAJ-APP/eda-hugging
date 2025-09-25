# 📊 GA4 Explorer - Análisis de Consentimiento

Una herramienta web para analizar datos de consentimiento de cookies en Google Analytics 4 usando BigQuery.

## 🚀 Demo en Vivo

**[🔗 Pruébalo aquí](https://huggingface.co/spaces/TU-USERNAME/ga4-explorer)** *(actualiza con tu URL)*

## ✨ Características

- 🍪 **Análisis de Consentimiento**: Visualiza el estado de consentimiento de analytics y ads storage
- 📱 **Análisis por Dispositivo**: Segmentación por tipo de dispositivo (móvil, desktop, tablet)
- 📊 **Gráficos Interactivos**: Visualizaciones con Plotly
- 🔒 **Seguro**: Tus credenciales se procesan solo en tu sesión

## 🛠️ Tecnologías

- **Gradio**: Interfaz web interactiva
- **Google Cloud BigQuery**: Base de datos de GA4
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Procesamiento de datos

## 📋 Requisitos

1. **Proyecto de Google Cloud** con GA4 conectado a BigQuery
2. **Cuenta de servicio** con permisos de BigQuery
3. **Credenciales JSON** de la cuenta de servicio

## 🔧 Configuración Local

```bash
# Clonar repositorio
git clone https://github.com/TU-USERNAME/ga4-explorer.git
cd ga4-explorer

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

## 📊 Uso

1. **Introduce datos de tu proyecto**:
   - ID del proyecto GCP
   - Nombre del dataset GA4 en BigQuery
   - Rango de fechas a analizar

2. **Pega las credenciales JSON** de tu cuenta de servicio

3. **Haz clic en Analizar** para ver los resultados

## 🔐 Seguridad

- Las credenciales se procesan solo en tu sesión
- No se almacenan datos en el servidor
- Conexión segura con Google Cloud

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 📞 Contacto

Tu Nombre - [@tu_twitter](https://twitter.com/tu_twitter)

Link del Proyecto: [https://github.com/TU-USERNAME/ga4-explorer](https://github.com/TU-USERNAME/ga4-explorer)
