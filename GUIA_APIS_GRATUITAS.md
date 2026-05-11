# 🆓 Guía Completa: APIs de IA Gratuitas

Esta guía te muestra cómo obtener API keys **100% GRATUITAS** para el chatbot. Todas las opciones son sin tarjeta de crédito.

---

## 🥇 Opción 1: Groq (RECOMENDADO)

**¿Por qué Groq?**
- ✅ Completamente gratis, sin tarjeta de crédito
- ✅ Extremadamente rápido (más rápido que GPT-4)
- ✅ Límite generoso: 14,400 requests/día
- ✅ Modelos potentes: Llama 3.1 70B, Mixtral 8x7B
- ✅ Configuración en 2 minutos

### Pasos para obtener API Key de Groq:

1. **Ir a Groq Console**
   - Visita: https://console.groq.com

2. **Crear cuenta**
   - Haz clic en "Sign Up"
   - Puedes usar Google, GitHub o email
   - NO requiere tarjeta de crédito

3. **Obtener API Key**
   - Una vez dentro, ve a la sección "API Keys"
   - Haz clic en "Create API Key"
   - Dale un nombre (ej: "ContaBot")
   - Copia la key que empieza con `gsk_...`
   - ⚠️ Guárdala en un lugar seguro, solo se muestra una vez

4. **Configurar en el proyecto**
   ```bash
   # En tu archivo .env
   AI_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Límites gratuitos**
   - 14,400 requests por día
   - 30 requests por minuto
   - Suficiente para ~500 conversaciones diarias

---

## 🥈 Opción 2: Cohere

**¿Por qué Cohere?**
- ✅ Gratis sin tarjeta de crédito
- ✅ Modelo Command R+ muy potente
- ✅ Límite: 1,000 requests/mes (Trial)
- ✅ Especializado en chat y conversaciones

### Pasos para obtener API Key de Cohere:

1. **Ir a Cohere Dashboard**
   - Visita: https://dashboard.cohere.com

2. **Crear cuenta**
   - Haz clic en "Sign Up"
   - Usa Google, GitHub o email
   - NO requiere tarjeta de crédito

3. **Obtener API Key**
   - En el dashboard, ve a "API Keys"
   - Copia la "Trial Key" que ya está creada
   - O crea una nueva con "Create API Key"

4. **Configurar en el proyecto**
   ```bash
   # En tu archivo .env
   AI_PROVIDER=cohere
   COHERE_API_KEY=tu_cohere_api_key_aqui
   ```

5. **Límites gratuitos (Trial)**
   - 1,000 requests por mes
   - Suficiente para ~30 conversaciones diarias

---

## 🥉 Opción 3: HuggingFace

**¿Por qué HuggingFace?**
- ✅ Completamente gratis
- ✅ Acceso a miles de modelos
- ✅ Sin límites estrictos (rate limiting flexible)
- ✅ Comunidad open source

### Pasos para obtener Token de HuggingFace:

1. **Ir a HuggingFace**
   - Visita: https://huggingface.co

2. **Crear cuenta**
   - Haz clic en "Sign Up"
   - Usa email, Google o GitHub
   - NO requiere tarjeta de crédito

3. **Obtener Access Token**
   - Ve a tu perfil → Settings
   - O directamente: https://huggingface.co/settings/tokens
   - Haz clic en "New token"
   - Tipo: "Read" (suficiente para inference)
   - Dale un nombre (ej: "ContaBot")
   - Copia el token que empieza con `hf_...`

4. **Configurar en el proyecto**
   ```bash
   # En tu archivo .env
   AI_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=hf_tu_token_aqui
   ```

5. **Límites gratuitos**
   - Rate limiting flexible
   - Puede ser más lento que Groq
   - Gratis indefinidamente

---

## 📊 Comparación de Opciones

| Característica | Groq | Cohere | HuggingFace |
|---------------|------|--------|-------------|
| **Velocidad** | ⚡⚡⚡ Muy rápido | ⚡⚡ Rápido | ⚡ Moderado |
| **Límite diario** | 14,400 req/día | ~33 req/día | Flexible |
| **Tarjeta requerida** | ❌ No | ❌ No | ❌ No |
| **Calidad respuestas** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Facilidad setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Recomendado para** | Producción | Pruebas | Desarrollo |

---

## 🎯 Recomendación Final

**Para empezar:** Usa **Groq** (Opción 1)
- Es el más rápido y con mejor límite gratuito
- Perfecto para producción con tráfico moderado
- Configuración súper simple

**Si Groq no funciona:** Usa **Cohere** (Opción 2)
- Excelente calidad de respuestas
- Límite suficiente para pruebas

**Para experimentar:** Usa **HuggingFace** (Opción 3)
- Acceso a múltiples modelos
- Sin límites estrictos

---

## 🔄 Cambiar entre proveedores

Puedes cambiar de proveedor en cualquier momento editando el archivo `.env`:

```bash
# Cambiar a Groq
AI_PROVIDER=groq
GROQ_API_KEY=gsk_...

# O cambiar a Cohere
AI_PROVIDER=cohere
COHERE_API_KEY=...

# O cambiar a HuggingFace
AI_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_...
```

Reinicia el servidor después de cambiar:
```bash
# Detener el servidor (Ctrl+C)
# Volver a iniciar
python main.py
```

---

## ❓ Preguntas Frecuentes

**¿Cuál es realmente gratis?**
- Todas las opciones son 100% gratuitas sin tarjeta de crédito

**¿Cuál tiene mejor límite?**
- Groq: 14,400 requests/día (mejor)
- HuggingFace: Flexible
- Cohere: 1,000 requests/mes

**¿Cuál es más rápido?**
- Groq es el más rápido (respuestas en <1 segundo)

**¿Puedo usar varias a la vez?**
- Sí, puedes configurar todas y cambiar según necesites

**¿Necesito tarjeta de crédito?**
- NO, ninguna de estas opciones requiere tarjeta

---

## 🆘 Solución de Problemas

**Error: "Invalid API Key"**
- Verifica que copiaste la key completa
- Asegúrate de no tener espacios al inicio/final
- Revisa que el proveedor en `.env` coincida con la key

**Error: "Rate limit exceeded"**
- Espera unos minutos antes de reintentar
- Considera cambiar a otro proveedor
- Groq tiene el límite más alto

**Respuestas muy lentas**
- HuggingFace puede ser lento en horas pico
- Cambia a Groq para mejor velocidad

**El bot no responde**
- Verifica que el servidor esté corriendo
- Revisa los logs: `tail -f app.log`
- Confirma que la API key sea válida

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `tail -f app.log`
2. Verifica tu archivo `.env`
3. Prueba con otro proveedor
4. Consulta la documentación oficial de cada API

**Enlaces útiles:**
- Groq Docs: https://console.groq.com/docs
- Cohere Docs: https://docs.cohere.com
- HuggingFace Docs: https://huggingface.co/docs
