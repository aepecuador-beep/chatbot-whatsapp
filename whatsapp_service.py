"""
Servicio para interactuar con WhatsApp vía Twilio
"""
import logging
from twilio.rest import Client
import config

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Servicio para enviar y recibir mensajes de WhatsApp usando Twilio"""
    
    def __init__(self):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        self.from_number = config.TWILIO_WHATSAPP_NUMBER
        logger.info("✅ Cliente de Twilio inicializado correctamente")
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Envía un mensaje de WhatsApp (divide mensajes largos si es necesario)
        
        Args:
            to_number: Número de destino en formato 'whatsapp:+1234567890'
            message: Contenido del mensaje
        
        Returns:
            True si el mensaje se envió correctamente, False en caso contrario
        """
        try:
            # Asegurar que el número tenga el prefijo 'whatsapp:'
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Límite de WhatsApp: 1600 caracteres
            MAX_LENGTH = 1500  # Dejamos margen de seguridad
            
            # Si el mensaje es corto, enviarlo directamente
            if len(message) <= MAX_LENGTH:
                message_obj = self.client.messages.create(
                    from_=self.from_number,
                    body=message,
                    to=to_number
                )
                logger.info(f"✅ Mensaje enviado a {to_number} - SID: {message_obj.sid}")
                return True
            
            # Si el mensaje es largo, dividirlo en partes
            parts = []
            current_part = ""
            
            # Dividir por párrafos (saltos de línea)
            paragraphs = message.split('\n')
            
            for paragraph in paragraphs:
                # Si agregar este párrafo excede el límite, guardar la parte actual
                if len(current_part) + len(paragraph) + 1 > MAX_LENGTH:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = paragraph + '\n'
                else:
                    current_part += paragraph + '\n'
            
            # Agregar la última parte
            if current_part:
                parts.append(current_part.strip())
            
            # Enviar cada parte
            for i, part in enumerate(parts):
                # Agregar indicador de parte si hay múltiples
                if len(parts) > 1:
                    part_message = f"[{i+1}/{len(parts)}]\n\n{part}"
                else:
                    part_message = part
                
                message_obj = self.client.messages.create(
                    from_=self.from_number,
                    body=part_message,
                    to=to_number
                )
                logger.info(f"✅ Parte {i+1}/{len(parts)} enviada a {to_number} - SID: {message_obj.sid}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al enviar mensaje a {to_number}: {e}")
            return False
    
    def parse_incoming_message(self, request_data: dict) -> dict:
        """
        Parsea un mensaje entrante del webhook de Twilio
        
        Args:
            request_data: Datos del request POST de Twilio
        
        Returns:
            Diccionario con 'from', 'body' y 'message_sid'
        """
        return {
            'from': request_data.get('From', ''),
            'body': request_data.get('Body', ''),
            'message_sid': request_data.get('MessageSid', ''),
            'profile_name': request_data.get('ProfileName', 'Usuario')
        }


# Instancia global del servicio
whatsapp_service = WhatsAppService()
