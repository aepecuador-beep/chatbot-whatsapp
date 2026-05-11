"""
Gestor de conversaciones para mantener el historial por usuario
"""
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import config

logger = logging.getLogger(__name__)


class ConversationManager:
    """Gestiona el historial de conversaciones por número de teléfono"""
    
    def __init__(self):
        # Estructura: {phone_number: {"messages": [...], "last_activity": datetime}}
        self.conversations: Dict[str, Dict] = {}
        self.max_messages = config.MAX_HISTORY_MESSAGES
        self.timeout = config.CONVERSATION_TIMEOUT
    
    def add_message(self, phone_number: str, role: str, content: str):
        """
        Agrega un mensaje al historial de conversación
        
        Args:
            phone_number: Número de teléfono del usuario
            role: 'user' o 'assistant'
            content: Contenido del mensaje
        """
        # Inicializar conversación si no existe
        if phone_number not in self.conversations:
            self.conversations[phone_number] = {
                "messages": [],
                "last_activity": datetime.now()
            }
        
        # Agregar mensaje
        self.conversations[phone_number]["messages"].append({
            "role": role,
            "content": content
        })
        
        # Actualizar timestamp de última actividad
        self.conversations[phone_number]["last_activity"] = datetime.now()
        
        # Mantener solo los últimos N mensajes (sin contar el system prompt)
        messages = self.conversations[phone_number]["messages"]
        if len(messages) > self.max_messages:
            self.conversations[phone_number]["messages"] = messages[-self.max_messages:]
        
        logger.info(f"📝 Mensaje agregado para {phone_number}: {role}")
    
    def get_conversation_history(self, phone_number: str) -> List[Dict[str, str]]:
        """
        Obtiene el historial completo de conversación con el system prompt
        
        Args:
            phone_number: Número de teléfono del usuario
        
        Returns:
            Lista de mensajes incluyendo el system prompt al inicio
        """
        # Limpiar conversaciones antiguas
        self._cleanup_old_conversations()
        
        # Siempre incluir el system prompt al inicio
        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT}
        ]
        
        # Agregar historial del usuario si existe
        if phone_number in self.conversations:
            messages.extend(self.conversations[phone_number]["messages"])
        
        return messages
    
    def clear_conversation(self, phone_number: str):
        """
        Limpia el historial de conversación de un usuario
        
        Args:
            phone_number: Número de teléfono del usuario
        """
        if phone_number in self.conversations:
            del self.conversations[phone_number]
            logger.info(f"🗑️ Conversación limpiada para {phone_number}")
    
    def _cleanup_old_conversations(self):
        """Limpia conversaciones inactivas que exceden el timeout"""
        now = datetime.now()
        to_delete = []
        
        for phone_number, data in self.conversations.items():
            last_activity = data["last_activity"]
            if (now - last_activity).total_seconds() > self.timeout:
                to_delete.append(phone_number)
        
        for phone_number in to_delete:
            del self.conversations[phone_number]
            logger.info(f"🧹 Conversación expirada limpiada para {phone_number}")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de las conversaciones activas"""
        return {
            "active_conversations": len(self.conversations),
            "total_messages": sum(len(conv["messages"]) for conv in self.conversations.values())
        }


# Instancia global del gestor de conversaciones
conversation_manager = ConversationManager()
