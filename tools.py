import os
import json
import requests
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def research(query: str) -> List[Dict[str, Any]]:
    """
    Realiza búsquedas web usando Serper API
    """
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "gl": "es",
        "hl": "es"
    }
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def scrape_website(url: str) -> str:
    """
    Extrae contenido de una página web usando Selenium
    """
    try:
        # Configurar Chrome en modo headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Inicializar el navegador
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Obtener la página
        driver.get(url)
        content = driver.page_source
        driver.quit()
        
        # Procesar el contenido
        soup = BeautifulSoup(content, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        
        return text
        
    except Exception as e:
        return f"Error al extraer contenido: {str(e)}"

def write_content(topic: str, content_type: str = "article", length: str = "medium", 
                 research_results: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Genera contenido basado en un tema y resultados de investigación
    
    Args:
        topic: Tema principal del contenido
        content_type: Tipo de contenido (article, social, blog, etc.)
        length: Longitud deseada (short, medium, long)
        research_results: Resultados de investigación previos (opcional)
    """
    if research_results is None:
        research_results = research(topic)
    
    content = {
        "topic": topic,
        "type": content_type,
        "length": length,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": ""
    }
    
    try:
        if isinstance(research_results, dict) and "organic" in research_results:
            # Procesar resultados de búsqueda
            content["research_summary"] = []
            for result in research_results["organic"][:3]:
                content["research_summary"].append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
                
                # Intentar extraer contenido adicional de las URLs
                if result.get("link"):
                    additional_content = scrape_website(result["link"])
                    if additional_content and not additional_content.startswith("Error"):
                        content["research_summary"][-1]["detailed_content"] = additional_content
        
        # Formatear el contenido final
        formatted_content = f"# {topic}\n\n"
        formatted_content += "## Resumen de la Investigación\n\n"
        
        for item in content.get("research_summary", []):
            formatted_content += f"### {item['title']}\n"
            formatted_content += f"{item['snippet']}\n\n"
            if "detailed_content" in item:
                formatted_content += f"Contenido Detallado:\n{item['detailed_content'][:500]}...\n\n"
        
        content["content"] = formatted_content
        return content
        
    except Exception as e:
        return {
            "error": f"Error generando contenido: {str(e)}",
            "topic": topic,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def save_content(content: Dict[str, Any], filename: Optional[str] = None) -> str:
    """
    Guarda el contenido generado en un archivo
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_slug = content["topic"].lower().replace(" ", "_")[:30]
        filename = f"content_{topic_slug}_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        return f"Contenido guardado exitosamente en {filename}"
    except Exception as e:
        return f"Error guardando el contenido: {str(e)}"

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analiza el sentimiento del texto (placeholder para futura implementación)
    """
    return {
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": "Pendiente de implementación"
    }

def format_content_for_platform(content: Dict[str, Any], platform: str) -> str:
    """
    Formatea el contenido para diferentes plataformas
    """
    platforms = {
        "twitter": 280,
        "instagram": 2200,
        "facebook": 63206,
        "linkedin": 3000
    }
    
    max_length = platforms.get(platform.lower(), 1000)
    
    try:
        if "content" in content:
            text = content["content"]
            if len(text) > max_length:
                text = text[:max_length-3] + "..."
            
            return {
                "platform": platform,
                "formatted_content": text,
                "length": len(text),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        return {"error": f"Error formateando contenido: {str(e)}"}
