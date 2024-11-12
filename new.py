import os
import dotenv
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from tools import research, write_content, scrape_website

# Cargar variables de entorno
dotenv.load_dotenv()

# Configuración para OpenAI
config_list = [{
    "model": "gpt-3.5-turbo",
    "api_key": os.getenv("OPENAI_API_KEY"),
}]

# Configuración del asistente
llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.7,
}

# Solicitar información al usuario
brand_task = input("Por favor, ingrese el nombre de la marca o empresa: ")
user_task = input("Por favor, ingrese su objetivo, brief o planteamiento del problema: ")

# Definición de los agentes
user_proxy = UserProxyAgent(
    name="User_Proxy",
    system_message="Un proxy para interactuar con el usuario.",
    human_input_mode="TERMINATE",
    code_execution_config={"last_n_messages": 2, "work_dir": "workspace"},
    llm_config=llm_config
)

agency_manager = AssistantAgent(
    name="Agency_Manager",
    system_message=f'''
    Eres el Gerente de Proyecto, enfocado en {brand_task}. 
    Describe las tareas paso a paso para {user_task} con el equipo. 
    Actúa como centro de comunicación, mantén entregables de alta calidad y actualiza regularmente a todos los interesados sobre el progreso. 
    Termina la conversación con "TERMINATE" cuando todas las tareas estén completadas.
    ''',
    llm_config=llm_config
)

agency_researcher = AssistantAgent(
    name="Agency_Researcher",
    system_message=f'''
    Como Investigador Principal para {brand_task}, investiga sobre {user_task}.
    Utiliza la función de investigación para recopilar información detallada.
    Proporciona estos conocimientos de manera proactiva.
    ''',
    llm_config=llm_config,
    function_map={
        "research": research,
        "scrape_website": scrape_website
    }
)

agency_strategist = AssistantAgent(
    name="Agency_Strategist",
    system_message=f'''
    Como Estratega para {brand_task}, desarrolla estrategias para {user_task}.
    Analiza la investigación y propón soluciones estratégicas.
    ''',
    llm_config=llm_config
)

agency_writer = AssistantAgent(
    name="Agency_Writer",
    system_message=f'''
    Como Redactor Creativo para {brand_task}, crea contenido para {user_task}.
    Escribe de manera persuasiva y atractiva.
    ''',
    llm_config=llm_config,
    function_map={
        "write_content": write_content,
    }
)

writing_assistant = AssistantAgent(
    name="Writing_Assistant",
    system_message=f'''
    Como Asistente de Redacción para {brand_task}, ayuda a mejorar el contenido para {user_task}.
    Revisa y optimiza los textos.
    ''',
    llm_config=llm_config
)

agency_marketer = AssistantAgent(
    name="Agency_Marketer",
    system_message=f'''
    Como Especialista en Marketing para {brand_task}, desarrolla estrategias para {user_task}.
    Propón tácticas de marketing efectivas.
    ''',
    llm_config=llm_config
)

agency_mediaplanner = AssistantAgent(
    name="Agency_MediaPlanner",
    system_message=f'''
    Como Planificador de Medios para {brand_task}, desarrolla planes para {user_task}.
    Optimiza la distribución en diferentes canales.
    ''',
    llm_config=llm_config
)

agency_director = AssistantAgent(
    name="Agency_Director",
    system_message=f'''
    Como Director Creativo para {brand_task}, supervisa {user_task}.
    Asegura la calidad y coherencia del trabajo.
    ''',
    llm_config=llm_config
)

# Configuración del chat grupal
groupchat = GroupChat(
    agents=[
        user_proxy, agency_manager, agency_researcher, agency_strategist,
        agency_writer, writing_assistant, agency_marketer, agency_mediaplanner,
        agency_director
    ],
    messages=[],
    max_round=20
)

# Configuración del gestor del chat
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Registro de funciones para el proxy de usuario
user_proxy.register_function(
    function_map={
        "research": research,
        "write_content": write_content,
        "scrape_website": scrape_website
    }
)

# Crear directorio de trabajo si no existe
if not os.path.exists("workspace"):
    os.makedirs("workspace")

# Iniciar el chat
user_proxy.initiate_chat(
    manager,
    message=user_task,
)