# 🚀 Inicio Rápido - 5 Minutos

Guía express para tener tu chatbot funcionando en menos de 5 minutos.

---

## ✅ Checklist Rápido

- [ ] Python 3.10+ instalado
- [ ] Cuenta de Groq (gratis, sin tarjeta)
- [ ] Cuenta de Twilio (gratis, $15 de crédito)
- [ ] ngrok instalado

---

## 📝 Paso 1: Obtener API Keys (2 minutos)

### Groq (IA Gratuita)
1. Ve a: https://console.groq.com
2. Sign Up con Google/GitHub
3. Crea API Key → Copia la key `gsk_...`

### Twilio (WhatsApp)
1. Ve a: https://www.twilio.com/try-twilio
XHCK5MNJ7E3R5R41GHBES84F
2. Sign Up (gratis, $15 de crédito)
3. Ve a Console → Copia **Account SID** y **Auth Token**
4. Ve a Messaging → WhatsApp Sandbox
5. Anota el número de WhatsApp (ej: `+14155238886`)

---

## 💻 Paso 2: Configurar Proyecto (2 minutos)

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
```

Edita `.env` con tus credenciales:
```env
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

## 🌐 Paso 3: Exponer con ngrok (1 minuto)

```bash
# Terminal 1: Iniciar servidor
python main.py

# Terminal 2: Exponer con ngrok
ngrok http 5000
```

Copia la URL HTTPS de ngrok (ej: `https://abc123.ngrok.io`)

---

## 🔗 Paso 4: Configurar Webhook en Twilio (30 segundos)

1. Ve a: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
2. En "When a message comes in":
   - Pega: `https://tu-url-de-ngrok.ngrok.io/webhook`
   - Método: POST
3. Save

---

## 📱 Paso 5: Probar el Bot (30 segundos)

1. Abre WhatsApp en tu teléfono
2. Envía el código de unión al número de Twilio
   - Ejemplo: `join <código>` (lo ves en el sandbox de Twilio)
3. Envía: "Hola, ¿qué es el RESICO?"
4. ¡El bot debería responder! 🎉

---

## 🎯 Verificación Rápida

Si algo no funciona, verifica:

```bash
# Ver logs del servidor
tail -f app.log

# Probar que el servidor responde
curl http://localhost:5000/

# Verificar variables de entorno
cat .env
```

**Checklist de errores comunes:**
- [ ] ¿El servidor está corriendo? (`python main.py`)
- [ ] ¿ngrok está corriendo? (`ngrok http 5000`)
- [ ] ¿El webhook en Twilio tiene la URL correcta?
- [ ] ¿Las API keys en `.env` son correctas?
- [ ] ¿Enviaste el código de unión al sandbox?

---

## 🆘 Ayuda Rápida

**Error: "Invalid API Key"**
```bash
# Verifica tu .env
cat .env | grep GROQ_API_KEY
```

**Bot no responde**
```bash
# Revisa los logs
tail -f app.log
```

**Webhook error 500**
```bash
# Verifica que todas las variables estén configuradas
python -c "import config; config.validate_config()"
```

---

## 🎊 ¡Listo!

Tu chatbot está funcionando. Ahora puedes:

1. **Personalizar el system prompt** en `config.py`
2. **Cambiar el proveedor de IA** en `.env`
3. **Desplegar en producción** (ver README.md)

---

## 📚 Próximos Pasos

- Lee `README.md` para deployment en Railway/Render
- Lee `GUIA_APIS_GRATUITAS.md` para otras opciones de IA
- Personaliza el `SYSTEM_PROMPT` en `config.py`
- Agrega tu teléfono y email en `HUMAN_ADVISOR_MESSAGE`

---

## 💡 Tips

**Reiniciar el bot:**
```bash
# Ctrl+C para detener
python main.py  # Volver a iniciar
```

**Cambiar de IA:**
```bash
# Edita .env
AI_PROVIDER=cohere  # o huggingface
COHERE_API_KEY=tu_key

# Reinicia el servidor
```

**Limpiar conversación de prueba:**
```bash
curl -X POST http://localhost:5000/clear/whatsapp:+1234567890
```

---

¡Disfruta tu chatbot! 🤖💬
