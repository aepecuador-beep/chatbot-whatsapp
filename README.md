# Chatbot de WhatsApp para Asesoría Contable

Bot inteligente para asesoría contable usando WhatsApp, IA Gratuita (Groq/Cohere/HuggingFace) y Twilio.

## 📋 Estructura del Proyecto

```
whatsapp-contabot/
├── main.py                 # Servidor Flask y lógica del chatbot
├── config.py              # Configuración y variables de entorno
├── ai_service.py          # Integración con APIs de IA gratuitas (Groq/Cohere/HuggingFace)
├── whatsapp_service.py    # Integración con Twilio/Meta
├── conversation_manager.py # Gestión del historial de conversaciones
├── requirements.txt       # Dependencias Python
├── .env.example          # Ejemplo de variables de entorno
├── .gitignore            # Archivos a ignorar en git
└── README.md             # Este archivo
```

## 🚀 Guía de Configuración Paso a Paso

### 1. Obtener Credenciales de Twilio (Opción Recomendada para Empezar)

1. Ve a [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Crea una cuenta gratuita (incluye $15 de crédito)
3. Ve a la consola: [console.twilio.com](https://console.twilio.com)
4. Anota tu **Account SID** y **Auth Token**
5. Ve a **Messaging** → **Try it out** → **Send a WhatsApp message**
6. Sigue las instrucciones para unirte al sandbox de WhatsApp
7. Anota el número de WhatsApp de Twilio (ej: +14155238886)

### 2. Obtener API Key de IA Gratuita (Groq - RECOMENDADO)

**Opción 1: Groq (Más rápido y mejor límite)**
1. Ve a [console.groq.com](https://console.groq.com)
2. Crea una cuenta GRATIS (sin tarjeta de crédito)
3. Ve a **API Keys** y crea una nueva
4. Copia la key que empieza con `gsk_...`
5. Límite gratuito: 14,400 requests/día ⚡

**Otras opciones gratuitas:**
- **Cohere**: [dashboard.cohere.com](https://dashboard.cohere.com) - 1,000 req/mes
- **HuggingFace**: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) - Sin límite estricto

📖 **Ver guía detallada**: `GUIA_APIS_GRATUITAS.md`

### 3. Configuración Local

```bash
# Clonar o crear el proyecto
mkdir whatsapp-contabot
cd whatsapp-contabot

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales:
# - AI_PROVIDER=groq
# - GROQ_API_KEY=tu_key_de_groq
# - TWILIO_ACCOUNT_SID=tu_sid
# - TWILIO_AUTH_TOKEN=tu_token
```

### 4. Configurar ngrok para Pruebas Locales

```bash
# Instalar ngrok
# macOS: brew install ngrok
# O descarga desde: https://ngrok.com/download

# Autenticar ngrok (crea cuenta gratis en ngrok.com)
ngrok config add-authtoken TU_TOKEN_DE_NGROK

# Ejecutar el servidor Flask
python main.py

# En otra terminal, exponer el puerto
ngrok http 5000

# Copiar la URL HTTPS que ngrok te da (ej: https://abc123.ngrok.io)
```

### 5. Configurar Webhook en Twilio

1. Ve a [console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
2. En **"When a message comes in"**, pega tu URL de ngrok + `/webhook`
   - Ejemplo: `https://abc123.ngrok.io/webhook`
3. Método: **POST**
4. Guarda los cambios

### 6. Probar el Bot

1. Envía el código de unión al número de Twilio desde tu WhatsApp
   - Ejemplo: `join <código-único>`
2. Envía un mensaje de prueba: "Hola, necesito ayuda con mis impuestos"
3. El bot debería responder usando la IA configurada (Groq por defecto)

## 🚀 Despliegue en Producción

### Opción A: Railway (Recomendado)

1. Ve a [railway.app](https://railway.app) y crea una cuenta
2. Crea un nuevo proyecto → **Deploy from GitHub repo**
3. Conecta tu repositorio
4. Agrega las variables de entorno en **Variables**:
   - `AI_PROVIDER=groq`
   - `GROQ_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER`
5. Railway detectará automáticamente Python y desplegará
6. Copia la URL del dominio generado
7. Actualiza el webhook en Twilio con la nueva URL

### Opción B: Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Crea un nuevo **Web Service**
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
5. Agrega las variables de entorno
6. Despliega y copia la URL
7. Actualiza el webhook en Twilio

## 🔧 Variables de Entorno Requeridas

```env
# AI Provider (elige uno: groq, cohere, huggingface)
AI_PROVIDER=groq

# Groq (RECOMENDADO - Gratis y rápido)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Servidor
PORT=5000
FLASK_ENV=production
```

## 📱 Alternativa: WhatsApp Cloud API (Meta)

Si prefieres usar la API oficial de Meta (más compleja pero sin costos):

1. Ve a [developers.facebook.com](https://developers.facebook.com)
2. Crea una app de tipo **Business**
3. Agrega el producto **WhatsApp**
4. Obtén el **Access Token** temporal (válido 24h)
5. Para producción, necesitas un **Business Manager** verificado
6. Modifica `whatsapp_service.py` para usar Meta Cloud API

## 🧪 Comandos Útiles

```bash
# Ejecutar en desarrollo
python main.py

# Ver logs en tiempo real
tail -f app.log

# Probar la API directamente
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"From":"whatsapp:+1234567890","Body":"Hola"}'
```

## 📝 Notas Importantes

- El historial de conversaciones se guarda en memoria (se pierde al reiniciar)
- Para producción, considera usar SQLite o PostgreSQL
- Twilio sandbox requiere que los usuarios envíen un código de unión primero
- Groq tiene límites de rate: 14,400 requests/día en plan gratuito
- Para producción con Twilio, necesitas un número de WhatsApp Business aprobado

## 🆘 Solución de Problemas

**Error: "Webhook returned 500"**
- Revisa los logs del servidor
- Verifica que las credenciales sean correctas

**El bot no responde**
- Verifica que ngrok esté corriendo
- Confirma que el webhook en Twilio tenga la URL correcta
- Revisa que hayas enviado el código de unión al sandbox

**Error de API de IA**
- Verifica tu API key del proveedor configurado
- Revisa que no hayas excedido el límite de requests
- Prueba cambiando a otro proveedor en `.env`
- Consulta `GUIA_APIS_GRATUITAS.md` para más ayuda

## 📄 Licencia

MIT
