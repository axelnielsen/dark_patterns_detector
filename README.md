# Sistema de Detección de Patrones Oscuros en Sitios Web

![Versión](https://img.shields.io/badge/versión-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)

## Descripción General

El Sistema de Detección de Patrones Oscuros es una plataforma automatizada diseñada para identificar, analizar y documentar prácticas manipulativas en interfaces web conocidas como "patrones oscuros" (dark patterns). Estos patrones son técnicas de diseño que engañan o manipulan a los usuarios para que tomen decisiones que no necesariamente están alineadas con sus intereses, sino con los objetivos comerciales del sitio web.

Esta herramienta permite a investigadores, desarrolladores, reguladores y profesionales de UX/UI:

- **Analizar automáticamente** múltiples sitios web en busca de patrones oscuros
- **Documentar con evidencias** las prácticas manipulativas encontradas
- **Generar informes detallados** en múltiples formatos (HTML, JSON, CSV)
- **Visualizar resultados** a través de una interfaz web intuitiva

## Características Principales

- **Carga flexible de URLs**: Importación desde archivos CSV, JSON, TXT o entrada directa
- **Navegación automatizada**: Exploración de sitios web con captura de pantallas y extracción de DOM
- **Detección avanzada**: Identificación de 7 tipos de patrones oscuros mediante análisis heurístico
- **Generación de informes**: Creación de informes detallados con evidencias y recomendaciones
- **Interfaz web completa**: Dashboard interactivo con estadísticas, gráficos y tablas detalladas
- **Exportación versátil**: Descarga de informes en formatos HTML, JSON y CSV

## Tipos de Patrones Detectados

| Patrón | Descripción | Método de Detección |
|--------|-------------|---------------------|
| **Confirmshaming** | Textos que avergüenzan al usuario por rechazar | Análisis de texto en botones de rechazo |
| **Preselección** | Opciones marcadas por defecto que benefician al proveedor | Análisis de elementos input preseleccionados |
| **Cargos ocultos** | Costos adicionales revelados tarde en el proceso | Seguimiento de cambios en precios durante el proceso |
| **Suscripciones difíciles de cancelar** | Proceso de cancelación innecesariamente complejo | Análisis de rutas de navegación para cancelación |
| **Publicidad engañosa** | Anuncios camuflados como contenido normal | Análisis visual de elementos que parecen controles |
| **Falsos contadores de urgencia** | Contadores que crean falsa sensación de urgencia | Análisis de contadores regresivos y mensajes de escasez |
| **Interfaces confusas** | Diseños deliberadamente confusos | Análisis de contraste y jerarquías visuales |

## Arquitectura del Sistema

El sistema sigue una arquitectura modular con cinco componentes principales:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Cargador de    │────▶│   Navegador     │────▶│  Detectores de  │
│     URLs        │     │  Automatizado   │     │    Patrones     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Interfaz Web   │◀────│   Generador de  │◀────│   Evidencias y  │
│                 │     │    Informes     │     │  Capturas       │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

Para más detalles sobre la arquitectura, consulte la [documentación técnica completa](docs/DOCUMENTACION_TECNICA.md).

## Requisitos del Sistema

- **Python**: 3.10 o superior
- **Node.js**: 14 o superior (para Playwright)
- **Navegadores**: Chrome, Firefox o Edge
- **RAM**: 4GB mínimo (8GB recomendado)
- **Almacenamiento**: 1GB mínimo para instalación y datos
- **Conexión a Internet**: Requerida para análisis de sitios web

## Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/usuario/dark-patterns-detector.git
cd dark-patterns-detector

# Instalar dependencias
pip install -r requirements.txt
python -m playwright install

# Configurar directorios
mkdir -p data/{uploads,reports,screenshots,evidence}

# Iniciar aplicación
cd src/web
python app.py
```

Después de la instalación, acceda a la interfaz web en `http://localhost:5000`

## Guía de Uso

### 1. Carga de URLs

- **Desde archivo**: Suba un archivo CSV, JSON o TXT con las URLs a analizar
- **Entrada directa**: Ingrese URLs manualmente en el campo de texto
- **Formato CSV**: `url,categoría,prioridad` (solo URL es obligatoria)
- **Formato JSON**: Array de objetos con al menos la propiedad `url`

### 2. Ejecución del Análisis

- Seleccione los tipos de patrones a detectar
- Configure opciones avanzadas (profundidad de análisis, tiempo máximo)
- Inicie el análisis y monitoree el progreso en tiempo real

### 3. Visualización de Resultados

- Consulte el dashboard para estadísticas generales
- Revise la tabla detallada de sitios y patrones detectados
- Explore los informes individuales con evidencias y capturas

### 4. Exportación de Informes

- **HTML**: Informes visuales con capturas de pantalla (se abren en nueva pestaña)
- **JSON**: Datos estructurados completos para integración con otros sistemas
- **CSV**: Formato tabular para análisis en hojas de cálculo

## Estructura del Proyecto

```
dark_patterns_detector/
├── src/                    # Código fuente
│   ├── crawlers/           # Navegador automatizado y crawlers
│   │   ├── web_crawler.py  # Implementación principal con Playwright
│   │   └── ...
│   ├── detectors/          # Detectores de patrones oscuros
│   │   ├── base_detector.py           # Clase base abstracta
│   │   ├── confirmshaming_detector.py # Detector específico
│   │   ├── preselection_detector.py   # Detector específico
│   │   └── ...
│   ├── utils/              # Utilidades y herramientas
│   │   ├── url_loader.py   # Carga y validación de URLs
│   │   └── ...
│   ├── reports/            # Generadores de informes
│   │   ├── report_generator.py # Generación de informes
│   │   └── ...
│   └── web/                # Interfaz web
│       ├── app.py          # Aplicación Flask
│       ├── templates/      # Plantillas HTML
│       └── static/         # Recursos estáticos (CSS, JS)
├── data/                   # Datos de entrada y salida
│   ├── uploads/            # Archivos de URLs subidos
│   ├── reports/            # Informes generados
│   ├── screenshots/        # Capturas de pantalla
│   └── evidence/           # Evidencias adicionales
├── tests/                  # Pruebas unitarias y de integración
│   ├── test_url_loader.py  # Pruebas para cargador de URLs
│   └── ...
└── docs/                   # Documentación
    ├── DOCUMENTACION_TECNICA.md  # Documentación técnica completa
    ├── INSTALACION.md      # Guía detallada de instalación
    ├── USO.md              # Manual de usuario
    └── ...
```

## Tecnologías Utilizadas

### Backend
- **Python**: Lenguaje principal de desarrollo
- **Flask**: Framework web para la interfaz de usuario
- **Playwright**: Automatización de navegador web
- **BeautifulSoup**: Análisis y manipulación de HTML/XML
- **Pandas**: Manipulación y análisis de datos

### Frontend
- **HTML5/CSS3**: Estructura y estilos de la interfaz
- **JavaScript**: Interactividad y funcionalidades dinámicas
- **Chart.js**: Visualización de datos y gráficos
- **Font Awesome**: Iconos e indicadores visuales

## Documentación Adicional

- [Documentación Técnica Completa](docs/DOCUMENTACION_TECNICA.md)
- [Guía de Instalación Detallada](docs/INSTALACION.md)
- [Manual de Usuario](docs/USO.md)
- [Arquitectura del Sistema](docs/ARQUITECTURA.md)
- [Ejemplos de Uso](docs/EJEMPLOS.md)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Fork del repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios y añada pruebas
4. Ejecute las pruebas (`python -m unittest discover tests`)
5. Commit de sus cambios (`git commit -m 'Añade nueva funcionalidad'`)
6. Push a la rama (`git push origin feature/nueva-funcionalidad`)
7. Abra un Pull Request

## Licencia

Este proyecto está disponible bajo la licencia MIT. Consulte el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para preguntas, sugerencias o reportes de errores, por favor abra un issue en el repositorio o contacte al equipo de desarrollo.

---

**Nota**: Este sistema está diseñado con fines educativos, de investigación y mejora de interfaces. Utilícelo de manera ética y responsable.
