"""
Chatbot de WhatsApp para Asesoría Contable
Servidor Flask con webhook para recibir mensajes de Twilio
"""
import logging
from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse

import config
from ai_service import get_ai_response
from whatsapp_service import whatsapp_service
from conversation_manager import conversation_manager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)


def detect_human_advisor_request(message: str) -> bool:
    """
    Detecta si el usuario está solicitando hablar con un asesor humano
    
    Args:
        message: Mensaje del usuario
    
    Returns:
        True si se detecta solicitud de asesor humano
    """
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in config.HUMAN_ADVISOR_KEYWORDS)


@app.route('/')
def home():
    """Endpoint de salud del servidor"""
    stats = conversation_manager.get_stats()
    return jsonify({
        'status': 'online',
        'service': 'ContaBot WhatsApp',
        'ai_provider': config.AI_PROVIDER,
        'active_conversations': stats['active_conversations'],
        'total_messages': stats['total_messages']
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook para recibir mensajes de WhatsApp vía Twilio
    """
    try:
        # Parsear mensaje entrante
        incoming_data = whatsapp_service.parse_incoming_message(request.form)
        user_phone = incoming_data['from']
        user_message = incoming_data['body']
        profile_name = incoming_data['profile_name']
        
        logger.info(f"📱 Mensaje recibido de {profile_name} ({user_phone}): {user_message}")
        
        # Validar que el mensaje no esté vacío
        if not user_message.strip():
            logger.warning("⚠️ Mensaje vacío recibido")
            return str(MessagingResponse())
        
        # Agregar mensaje del usuario al historial
        conversation_manager.add_message(user_phone, 'user', user_message)
        
        # Detectar si solicita asesor humano
        if detect_human_advisor_request(user_message):
            logger.info(f"👨‍💼 Solicitud de asesor humano detectada de {user_phone}")
            response_text = config.HUMAN_ADVISOR_MESSAGE
        else:
            # Obtener historial completo con system prompt
            conversation_history = conversation_manager.get_conversation_history(user_phone)
            
            # Obtener respuesta de la IA
            logger.info(f"🤖 Consultando IA ({config.AI_PROVIDER})...")
            response_text = get_ai_response(conversation_history)
            logger.info(f"✅ Respuesta de IA obtenida: {response_text[:100]}...")
        
        # Agregar respuesta del bot al historial
        conversation_manager.add_message(user_phone, 'assistant', response_text)
        
        # Enviar respuesta por WhatsApp
        whatsapp_service.send_message(user_phone, response_text)
        
        # Responder al webhook de Twilio (vacío porque ya enviamos el mensaje)
        return str(MessagingResponse())
        
    except Exception as e:
        logger.error(f"❌ Error en webhook: {e}", exc_info=True)
        
        # Enviar mensaje de error al usuario
        try:
            error_message = "Disculpa, estoy teniendo problemas técnicos. Por favor, intenta de nuevo en un momento. 🔧"
            whatsapp_service.send_message(request.form.get('From', ''), error_message)
        except:
            pass
        
        return str(MessagingResponse())


@app.route('/clear/<phone_number>', methods=['POST'])
def clear_conversation(phone_number):
    """
    Endpoint para limpiar el historial de conversación de un usuario
    Útil para pruebas y debugging
    """
    try:
        # Agregar prefijo whatsapp: si no lo tiene
        if not phone_number.startswith('whatsapp:'):
            phone_number = f'whatsapp:{phone_number}'
        
        conversation_manager.clear_conversation(phone_number)
        return jsonify({
            'status': 'success',
            'message': f'Conversación limpiada para {phone_number}'
        })
    except Exception as e:
        logger.error(f"Error al limpiar conversación: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/stats')
def stats():
    """Endpoint para ver estadísticas del bot"""
    return jsonify(conversation_manager.get_stats())


@app.route('/health')
def health():
    """Endpoint de health check para servicios de deployment"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/dashboard')
def dashboard():
    """Dashboard web para visualizar mensajes y editar prompt"""
    return render_template('dashboard.html')


@app.route('/api/messages')
def api_messages():
    """API para obtener todos los mensajes"""
    messages = []
    
    for phone, data in conversation_manager.conversations.items():
        for msg in data['messages']:
            messages.append({
                'phone': phone,
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': data['last_activity'].strftime('%H:%M:%S')
            })
    
    # Ordenar por timestamp
    messages.sort(key=lambda x: x['timestamp'])
    
    stats = conversation_manager.get_stats()
    
    return jsonify({
        'messages': messages,
        'stats': stats,
        'ai_provider': config.AI_PROVIDER
    })


@app.route('/api/prompt', methods=['GET', 'POST'])
def api_prompt():
    """API para obtener y actualizar el system prompt"""
    if request.method == 'GET':
        return jsonify({'prompt': config.SYSTEM_PROMPT})
    
    elif request.method == 'POST':
        try:
            data = request.json
            new_prompt = data.get('prompt', '')
            
            if not new_prompt:
                return jsonify({'success': False, 'error': 'Prompt vacío'}), 400
            
            # Actualizar el prompt en el archivo config.py
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Encontrar y reemplazar el SYSTEM_PROMPT
            import re
            pattern = r'SYSTEM_PROMPT = """.*?"""'
            replacement = f'SYSTEM_PROMPT = """{new_prompt}"""'
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Recargar el módulo config
            import importlib
            importlib.reload(config)
            
            logger.info("✅ System prompt actualizado correctamente")
            
            return jsonify({'success': True, 'message': 'Prompt actualizado'})
        
        except Exception as e:
            logger.error(f"Error al actualizar prompt: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/prompt/reset', methods=['POST'])
def api_prompt_reset():
    """API para restaurar el prompt original"""
    try:
        # Restaurar desde el backup si existe
        import os
        if os.path.exists('config_backup.py'):
            with open('config_backup.py', 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            # Recargar el módulo config
            import importlib
            importlib.reload(config)
            
            return jsonify({'success': True, 'message': 'Prompt restaurado'})
        else:
            return jsonify({'success': False, 'error': 'No hay backup disponible'}), 404
    
    except Exception as e:
        logger.error(f"Error al restaurar prompt: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Validar configuración antes de iniciar
    try:
        config.validate_config()
        logger.info("✅ Configuración validada correctamente")
        logger.info(f"🤖 Usando proveedor de IA: {config.AI_PROVIDER}")
        logger.info(f"📱 Número de WhatsApp: {config.TWILIO_WHATSAPP_NUMBER}")
    except ValueError as e:
        logger.error(f"❌ Error de configuración: {e}")
        exit(1)
    
    # Iniciar servidor
    logger.info(f"🚀 Iniciando servidor en puerto {config.PORT}...")
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
