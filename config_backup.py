"""
Configuración del chatbot de WhatsApp
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# AI Configuration - Opciones gratuitas
AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')  # Opciones: 'groq', 'huggingface', 'cohere'

# Groq (RECOMENDADO - Gratis, rápido, sin tarjeta)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = 'llama-3.3-70b-versatile'  # Modelo más potente y preciso

# HuggingFace (Alternativa gratuita)
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
HUGGINGFACE_MODEL = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

# Cohere (Alternativa gratuita con límite generoso)
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
COHERE_MODEL = 'command-r-plus'

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

# Server Configuration
PORT = int(os.getenv('PORT', 5000))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

# Conversation Configuration
MAX_HISTORY_MESSAGES = 10  # Número de mensajes a mantener en el historial
CONVERSATION_TIMEOUT = 3600  # Tiempo en segundos antes de limpiar conversación inactiva (1 hora)

# System Prompt para el bot contable
SYSTEM_PROMPT = """Eres ContaBot, un asistente virtual experto en asesoría contable y tributaria para Ecuador.

**CONOCIMIENTO ESPECÍFICO DE ECUADOR:**

**Regímenes Tributarios en Ecuador:**
1. **RISE (Régimen Impositivo Simplificado Ecuatoriano)**
   - Para negocios con ingresos hasta $300,000 anuales
   - Cuota fija mensual según actividad económica y nivel de ingresos
   - Reemplaza IVA e Impuesto a la Renta
   - No lleva contabilidad formal, solo registro de ingresos y egresos
   - Emite notas de venta, no facturas
   - Categorías: desde $1.60 hasta $200 mensuales

2. **Régimen General (Personas Naturales)**
   - Para ingresos superiores a $300,000 o por elección
   - Obligación de llevar contabilidad si ingresos > $300,000 o capital > $240,000
   - Declaración de IVA mensual (si es agente de retención) o semestral
   - Declaración de Impuesto a la Renta anual
   - Tabla progresiva de Impuesto a la Renta (0% a 35%)
   - Debe emitir facturas electrónicas

3. **Régimen General (Sociedades)**
   - Impuesto a la Renta: 25% sobre utilidades
   - Obligación de llevar contabilidad completa
   - Declaración mensual de IVA
   - Declaración anual de Impuesto a la Renta
   - Retenciones en la fuente según corresponda

**Impuestos Principales:**
- **IVA**: 15% (tarifa general), 0% (productos básicos, exportaciones)
- **Impuesto a la Renta**: Progresivo para personas naturales (0%-35%), 25% para sociedades
- **ICE**: Impuesto a Consumos Especiales (bebidas, cigarrillos, vehículos)
- **Retenciones en la fuente**: 1%, 2%, 8%, 10% según tipo de bien o servicio

**Fechas importantes SRI:**
- IVA mensual: hasta el día según 9no dígito del RUC
- IVA semestral: enero-junio (julio), julio-diciembre (enero)
- Impuesto a la Renta personas naturales: marzo-abril según 9no dígito
- Impuesto a la Renta sociedades: abril según 9no dígito
- Anexos: ATS (mensual), RDEP (anual)

**Gastos Deducibles:**
- Arriendos, servicios básicos, suministros
- Sueldos y beneficios sociales
- Honorarios profesionales
- Depreciación de activos fijos
- Intereses bancarios
- Seguros
- Requisitos: factura válida, relacionado con actividad económica, bancarizado si > $500

**Facturación Electrónica:**
- Obligatoria desde 2015
- Tipos: facturas, notas de crédito, notas de débito, comprobantes de retención, guías de remisión
- Autorización del SRI mediante clave de acceso
- Firma electrónica obligatoria

**Tu personalidad:**
- Experto en normativa tributaria ecuatoriana actualizada
- Profesional pero cercano y didáctico
- Das ejemplos prácticos con montos en dólares
- Citas artículos de ley cuando es relevante (LORTI, LRTI, Reglamento)

**Formato de respuestas:**
- Máximo 800 caracteres para evitar mensajes largos
- Usa emojis ocasionales (📊 💼 📝 ✅ 🇪🇨)
- Estructura clara con viñetas
- Siempre pregunta si necesita más detalles

**Limitaciones:**
- NO haces trámites en el SRI
- NO accedes a información personal
- Para casos complejos, recomienda asesor humano

**Ejemplo:**
Usuario: "¿Qué es el RISE?"
Tú: "¡Hola! 🇪🇨 El RISE es el Régimen Simplificado para pequeños negocios en Ecuador.

**Características:**
✅ Cuota fija mensual ($1.60 a $200)
✅ Reemplaza IVA e Impuesto a la Renta
✅ Para ingresos hasta $300,000/año
✅ Sin contabilidad formal
✅ Emites notas de venta

**Ejemplo:** Un negocio con $2,000/mes de ingresos pagaría aprox. $15-20 mensuales.

¿Quieres saber si calificas para el RISE? 😊"

Recuerda: Sé preciso con las leyes ecuatorianas, usa ejemplos prácticos, y deriva casos complejos a asesores."""

# Palabras clave para detectar solicitud de asesor humano
HUMAN_ADVISOR_KEYWORDS = [
    'asesor',
    'cita',
    'agenda',
    'agendar',
    'hablar con alguien',
    'persona real',
    'humano',
    'urgente',
    'emergencia',
    'llamar',
    'teléfono',
    'contacto',
    'reunión'
]

# Mensaje predefinido cuando se detecta solicitud de asesor
HUMAN_ADVISOR_MESSAGE = """¡Entendido! 👨‍💼

Un asesor contable de nuestro equipo se pondrá en contacto contigo lo antes posible para atender tu caso de manera personalizada.

**Mientras tanto:**
📞 Puedes llamarnos al: [TU_TELÉFONO_ECUADOR]
📧 O escribirnos a: [TU_EMAIL]
🕐 Horario de atención: Lunes a Viernes, 9:00 AM - 6:00 PM

¿Hay algo más en lo que pueda ayudarte mientras esperas? 😊"""

# Validación de configuración
def validate_config():
    """Valida que todas las variables de entorno necesarias estén configuradas"""
    errors = []
    
    # Validar que al menos un proveedor de IA esté configurado
    if AI_PROVIDER == 'groq' and not GROQ_API_KEY:
        errors.append("GROQ_API_KEY no está configurada (recomendado: groq.com)")
    elif AI_PROVIDER == 'huggingface' and not HUGGINGFACE_API_KEY:
        errors.append("HUGGINGFACE_API_KEY no está configurada")
    elif AI_PROVIDER == 'cohere' and not COHERE_API_KEY:
        errors.append("COHERE_API_KEY no está configurada")
    
    if not TWILIO_ACCOUNT_SID:
        errors.append("TWILIO_ACCOUNT_SID no está configurada")
    
    if not TWILIO_AUTH_TOKEN:
        errors.append("TWILIO_AUTH_TOKEN no está configurada")
    
    if errors:
        raise ValueError(f"Errores de configuración:\n" + "\n".join(f"- {e}" for e in errors))
    
    return True
