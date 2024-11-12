 AI Agents Project

Sistema de agentes de IA para automatización de tareas usando OpenAI y Autogen.

## Configuración

1. Clonar el repositorio:

bash
git clone https://github.com/USER/REPO.git
cd REPO

2. Crear entorno virtual:
bash
python -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate

3. Instalar dependencias:
bash
pip install -r requirements.txt


4. Crear archivo .env con las API keys:
bash
OPENAI_API_KEY=tu_api_key_aqui
SERPER_API_KEY=tu_serper_key_aqui

## Uso
bash
python main.py


## Estructura

- `main.py`: Archivo principal con la configuración de OpenAI
- `new.py`: Versión alternativa del código
- `tools.py`: Herramientas y utilidades para los agentes
- `workspace/`: Directorio para outputs generados

## Características

- Múltiples agentes especializados:
  - Agency_Manager: Gestión de proyectos
  - Agency_Researcher: Investigación y recopilación de datos
  - Agency_Strategist: Desarrollo de estrategias
  - Agency_Writer: Creación de contenido
  - Writing_Assistant: Optimización de textos
  - Agency_Marketer: Estrategias de marketing
  - Agency_MediaPlanner: Planificación de medios
  - Agency_Director: Supervisión creativa

- Integración con APIs:
  - OpenAI GPT-3.5/4 para procesamiento de lenguaje natural
  - Serper para búsquedas web
  - Selenium para web scraping

- Funcionalidades:
  - Investigación automática
  - Generación de contenido
  - Análisis estratégico
  - Planificación de marketing
  - Web scraping
  - Gestión de proyectos

## Requisitos

- Python 3.8 o superior
- Cuenta de OpenAI con API key
- Cuenta de Serper con API key
- Chrome/Chromium para web scraping

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto

Tu Nombre - [@tutwitter](https://twitter.com/tutwitter)

Project Link: [https://github.com/USER/REPO](https://github.com/USER/REPO)

## Agradecimientos

- [Autogen](https://github.com/microsoft/autogen)
- [OpenAI](https://openai.com/)
- [Serper](https://serper.dev/)
- [Selenium](https://www.selenium.dev/)