# 🚀 Desplegar en Railway (5 minutos)

Railway es una plataforma gratuita que te da una URL permanente para tu bot.

## 📋 Pasos:

### 1. Crear cuenta en Railway
1. Ve a: https://railway.app
2. Haz clic en **"Start a New Project"**
3. Sign up con GitHub (gratis)

### 2. Subir tu código a GitHub

```bash
# Inicializar git (si no lo has hecho)
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Chatbot de WhatsApp para asesoría contable"

# Crear repositorio en GitHub
# Ve a: https://github.com/new
# Crea un repositorio llamado "whatsapp-contabot"

# Conectar y subir
git remote add origin https://github.com/TU_USUARIO/whatsapp-contabot.git
git branch -M main
git push -u origin main
```

### 3. Desplegar en Railway

1. En Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Autoriza Railway a acceder a tu GitHub
4. Selecciona el repositorio **"whatsapp-contabot"**
5. Railway detectará automáticamente que es Python

### 4. Configurar Variables de Entorno

En Railway, ve a la pestaña **"Variables"** y agrega:

```
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
PORT=5000
FLASK_ENV=production
```

### 5. Obtener la URL

1. Railway desplegará automáticamente tu app
2. Ve a la pestaña **"Settings"**
3. En **"Domains"**, haz clic en **"Generate Domain"**
4. Copia la URL (ej: `https://whatsapp-contabot-production.up.railway.app`)

### 6. Configurar Webhook en Twilio

1. Ve a: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
2. Pestaña **"Sandbox settings"**
3. En **"WHEN A MESSAGE COMES IN"**:
   - URL: `https://TU-URL-DE-RAILWAY.up.railway.app/webhook`
   - Método: `HTTP POST`
4. **Save**

---

## ✅ ¡Listo!

Tu bot ahora tiene una URL permanente que nunca se cae. Railway es gratis para proyectos pequeños.

---

## 🔧 Comandos útiles

```bash
# Ver logs en Railway
# Ve a la pestaña "Deployments" → Click en el deployment → "View Logs"

# Actualizar el bot
git add .
git commit -m "Actualización"
git push

# Railway desplegará automáticamente los cambios
```

---

## 💡 Ventajas de Railway

✅ URL permanente (no se cae)
✅ Despliegue automático desde GitHub
✅ Logs en tiempo real
✅ Gratis para proyectos pequeños
✅ SSL/HTTPS incluido
✅ No requiere tarjeta de crédito

---

## 🆘 Problemas comunes

**Error: "Application failed to respond"**
- Verifica que el `PORT` en las variables de entorno sea `5000`
- Revisa los logs en Railway

**Bot no responde**
- Verifica que el webhook en Twilio tenga la URL correcta
- Revisa los logs en Railway para ver si llegan las peticiones

**Variables de entorno no funcionan**
- Asegúrate de haber agregado TODAS las variables
- Redeploy el proyecto después de agregar variables
