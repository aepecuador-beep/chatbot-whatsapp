"""
Servicio de IA con soporte para múltiples proveedores GRATUITOS
"""
import logging
from typing import List, Dict
import config

logger = logging.getLogger(__name__)


class AIService:
    """Servicio para interactuar con diferentes APIs de IA gratuitas"""
    
    def __init__(self):
        self.provider = config.AI_PROVIDER
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente según el proveedor configurado"""
        try:
            if self.provider == 'openai':
                from openai import OpenAI
                self.client = OpenAI(api_key=config.OPENAI_API_KEY)
                self.model = config.OPENAI_MODEL
                logger.info("✅ Cliente OpenAI inicializado correctamente")
                
            elif self.provider == 'groq':
                from groq import Groq
                # Inicializar sin el parámetro proxies para compatibilidad
                self.client = Groq(api_key=config.GROQ_API_KEY)
                self.model = config.GROQ_MODEL
                logger.info("✅ Cliente Groq inicializado correctamente")
                
            elif self.provider == 'cohere':
                import cohere
                self.client = cohere.Client(config.COHERE_API_KEY)
                self.model = config.COHERE_MODEL
                logger.info("✅ Cliente Cohere inicializado correctamente")
                
            elif self.provider == 'huggingface':
                from huggingface_hub import InferenceClient
                self.client = InferenceClient(token=config.HUGGINGFACE_API_KEY)
                self.model = config.HUGGINGFACE_MODEL
                logger.info("✅ Cliente HuggingFace inicializado correctamente")
                
            else:
                raise ValueError(f"Proveedor de IA no soportado: {self.provider}")
                
        except Exception as e:
            logger.error(f"❌ Error al inicializar cliente de IA: {e}")
            raise
    
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Obtiene una respuesta del modelo de IA
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user/assistant/system", "content": "..."}]
        
        Returns:
            Respuesta del modelo como string
        """
        try:
            if self.provider == 'openai':
                return self._get_openai_response(messages)
            elif self.provider == 'groq':
                return self._get_groq_response(messages)
            elif self.provider == 'cohere':
                return self._get_cohere_response(messages)
            elif self.provider == 'huggingface':
                return self._get_huggingface_response(messages)
            else:
                return "Lo siento, hay un problema con la configuración del servicio de IA."
                
        except Exception as e:
            logger.error(f"❌ Error al obtener respuesta de IA: {e}")
            return "Disculpa, estoy teniendo problemas técnicos. Por favor, intenta de nuevo en un momento."
    
    def _get_openai_response(self, messages: List[Dict[str, str]]) -> str:
        """Obtiene respuesta usando OpenAI (GPT-4)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error en OpenAI API: {e}")
            raise
    
    def _get_groq_response(self, messages: List[Dict[str, str]]) -> str:
        """Obtiene respuesta usando Groq (RECOMENDADO - Rápido y gratuito)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error en Groq API: {e}")
            raise
    
    def _get_cohere_response(self, messages: List[Dict[str, str]]) -> str:
        """Obtiene respuesta usando Cohere"""
        try:
            # Cohere usa un formato diferente - convertir mensajes
            chat_history = []
            user_message = ""
            
            for msg in messages:
                if msg['role'] == 'system':
                    # El system prompt se maneja como preamble en Cohere
                    preamble = msg['content']
                elif msg['role'] == 'user':
                    user_message = msg['content']
                elif msg['role'] == 'assistant':
                    if user_message:  # Solo agregar si hay un mensaje de usuario previo
                        chat_history.append({
                            "role": "USER",
                            "message": user_message
                        })
                        chat_history.append({
                            "role": "CHATBOT",
                            "message": msg['content']
                        })
                        user_message = ""
            
            # El último mensaje debe ser del usuario
            if not user_message and messages[-1]['role'] == 'user':
                user_message = messages[-1]['content']
            
            response = self.client.chat(
                message=user_message,
                chat_history=chat_history if chat_history else None,
                preamble=preamble if 'preamble' in locals() else None,
                model=self.model,
                temperature=0.7
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error en Cohere API: {e}")
            raise
    
    def _get_huggingface_response(self, messages: List[Dict[str, str]]) -> str:
        """Obtiene respuesta usando HuggingFace Inference API"""
        try:
            # Convertir mensajes al formato de prompt para HuggingFace
            prompt = self._format_messages_for_huggingface(messages)
            
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Error en HuggingFace API: {e}")
            raise
    
    def _format_messages_for_huggingface(self, messages: List[Dict[str, str]]) -> str:
        """Formatea mensajes para modelos de HuggingFace"""
        prompt_parts = []
        
        for msg in messages:
            role = msg['role']
            content = msg['content']
            
            if role == 'system':
                prompt_parts.append(f"<s>[INST] <<SYS>>\n{content}\n<</SYS>>\n\n")
            elif role == 'user':
                if prompt_parts and not prompt_parts[-1].endswith('[INST] '):
                    prompt_parts.append(f"[INST] {content} [/INST]")
                else:
                    prompt_parts.append(f"{content} [/INST]")
            elif role == 'assistant':
                prompt_parts.append(f"{content}</s><s>")
        
        return "".join(prompt_parts)


# Instancia global del servicio
ai_service = AIService()


def get_ai_response(conversation_history: List[Dict[str, str]]) -> str:
    """
    Función helper para obtener respuesta de IA
    
    Args:
        conversation_history: Historial de conversación con system prompt incluido
    
    Returns:
        Respuesta del modelo de IA
    """
    return ai_service.get_response(conversation_history)
