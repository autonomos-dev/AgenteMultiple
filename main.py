import os
import json
import dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
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
    llm_config=llm_config,
    system_message=f'''
    Eres el Gerente de Proyecto, enfocado en {brand_task}. 
    Describe las tareas paso a paso para {user_task} con el equipo. 
    Actúa como centro de comunicación, mantén entregables de alta calidad y actualiza regularmente a todos los interesados sobre el progreso. 
    Termina la conversación con "TERMINATE" cuando todas las tareas estén completadas.
    '''
)

agency_researcher = AssistantAgent(
    name="Agency_Researcher",
    llm_config=llm_config,
    system_message=f'''
    Como Investigador Principal para {brand_task}, investiga sobre {user_task}.
    Utiliza la función de investigación para recopilar información detallada.
    Proporciona estos conocimientos de manera proactiva.
    ''',
    function_map={
        "research": research,
        "scrape_website": scrape_website
    }
)

agency_strategist = AssistantAgent(
    name="Agency_Strategist",
    llm_config=llm_config,
    system_message=f'''
    Como Estratega para {brand_task}, desarrolla estrategias para {user_task}.
    Analiza la investigación y propón soluciones estratégicas.
    '''
)

agency_writer = AssistantAgent(
    name="Agency_Writer",
    llm_config=llm_config,
    system_message=f'''
    Como Redactor Creativo para {brand_task}, crea contenido para {user_task}.
    Escribe de manera persuasiva y atractiva.
    ''',
    function_map={
        "write_content": write_content,
    }
)

writing_assistant = AssistantAgent(
    name="Writing_Assistant",
    llm_config=llm_config,
    system_message=f'''
    Como Asistente de Redacción para {brand_task}, ayuda a mejorar el contenido para {user_task}.
    Revisa y optimiza los textos.
    '''
)

agency_marketer = AssistantAgent(
    name="Agency_Marketer",
    llm_config=llm_config,
    system_message=f'''
    Como Especialista en Marketing para {brand_task}, desarrolla estrategias para {user_task}.
    Propón tácticas de marketing efectivas.
    '''
)

agency_mediaplanner = AssistantAgent(
    name="Agency_MediaPlanner",
    llm_config=llm_config,
    system_message=f'''
    Como Planificador de Medios para {brand_task}, desarrolla planes para {user_task}.
    Optimiza la distribución en diferentes canales.
    '''
)

agency_director = AssistantAgent(
    name="Agency_Director",
    llm_config=llm_config,
    system_message=f'''
    Como Director Creativo para {brand_task}, supervisa {user_task}.
    Asegura la calidad y coherencia del trabajo.
    '''
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