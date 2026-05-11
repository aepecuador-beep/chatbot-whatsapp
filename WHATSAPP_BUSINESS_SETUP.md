# 📱 Configurar WhatsApp Business con tu Número

Hay 3 formas de usar tu propio número de WhatsApp para el bot:

---

## 🥇 Opción 1: WhatsApp Cloud API (Meta) - GRATIS

**Ventajas:**
- ✅ Completamente gratis
- ✅ 1,000 conversaciones gratis/mes
- ✅ Usa tu propio número

**Desventajas:**
- ⚠️ Proceso de verificación más largo
- ⚠️ Requiere Facebook Business Manager
- ⚠️ Número no puede estar en WhatsApp personal

### Pasos:

1. **Crear cuenta de Facebook Business**
   - Ve a: https://business.facebook.com
   - Crea una cuenta de negocio
   - Verifica tu identidad

2. **Crear App en Meta for Developers**
   - Ve a: https://developers.facebook.com
   - Crea una nueva app de tipo "Business"
   - Agrega el producto "WhatsApp"

3. **Configurar número de teléfono**
   - En WhatsApp → Getting Started
   - Agrega tu número de teléfono
   - Verifica con código SMS
   - ⚠️ El número NO puede estar registrado en WhatsApp personal

4. **Obtener credenciales**
   - Phone Number ID
   - WhatsApp Business Account ID
   - Access Token (temporal 24h o permanente)

5. **Actualizar código**
   - Modifica `whatsapp_service.py` para usar Meta Cloud API
   - Usa las nuevas credenciales

### Código para Meta Cloud API:

```python
# En whatsapp_service.py
import requests

class WhatsAppService:
    def __init__(self):
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def send_message(self, to_number: str, message: str):
        # Remover prefijo whatsapp: si existe
        to_number = to_number.replace('whatsapp:', '').replace('+', '')
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': to_number,
            'type': 'text',
            'text': {'body': message}
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        return response.status_code == 200
```

### Variables de entorno (.env):

```env
# Meta WhatsApp Cloud API
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_ACCESS_TOKEN=tu_access_token
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id
```

---

## 🥈 Opción 2: Twilio con Número Propio - PAGO

**Ventajas:**
- ✅ Más fácil de configurar
- ✅ Soporte técnico
- ✅ Documentación completa

**Desventajas:**
- 💰 Costo: ~$15/mes por número
- 💰 $0.005 por mensaje enviado
- ⚠️ Requiere aprobación de Meta

### Pasos:

1. **Solicitar número de WhatsApp en Twilio**
   - Ve a: https://console.twilio.com
   - Messaging → WhatsApp → Request Access
   - Completa el formulario de solicitud

2. **Proceso de aprobación**
   - Meta revisa tu solicitud (1-2 semanas)
   - Necesitas:
     * Nombre del negocio
     * Sitio web
     * Descripción del uso
     * Logo de la empresa

3. **Una vez aprobado**
   - Twilio te asigna un número
   - Configuras el webhook
   - Actualizas `TWILIO_WHATSAPP_NUMBER` en `.env`

### Costos aproximados:
- Número WhatsApp: $15/mes
- Mensajes entrantes: GRATIS
- Mensajes salientes: $0.005 c/u
- Ejemplo: 1,000 mensajes/mes = $15 + $5 = $20/mes

---

## 🥉 Opción 3: Proveedores Alternativos

### 360Dialog
- https://www.360dialog.com
- Desde €49/mes
- Incluye número y mensajes

### Twilio SendGrid
- Integración con email y WhatsApp
- Planes desde $15/mes

### MessageBird
- https://messagebird.com
- API similar a Twilio
- Precios competitivos

---

## 🆓 Recomendación para empezar:

**Para pruebas:**
- Usa el Sandbox de Twilio (gratis, sin tu número)

**Para producción pequeña:**
- WhatsApp Cloud API de Meta (gratis, con tu número)

**Para producción profesional:**
- Twilio con número propio ($20-50/mes)

---

## 📝 Pasos para migrar de Sandbox a tu número:

### Si usas Meta Cloud API:

1. Obtén credenciales de Meta
2. Actualiza `whatsapp_service.py` con el código de arriba
3. Actualiza `.env`:
```env
WHATSAPP_PROVIDER=meta
WHATSAPP_PHONE_NUMBER_ID=tu_id
WHATSAPP_ACCESS_TOKEN=tu_token
```

### Si usas Twilio con número propio:

1. Solicita y espera aprobación
2. Una vez aprobado, actualiza `.env`:
```env
TWILIO_WHATSAPP_NUMBER=whatsapp:+593XXXXXXXXX
```
3. Configura el webhook con tu URL

---

## ⚠️ Importante:

**Limitaciones del Sandbox:**
- ❌ Solo usuarios que envíen código de unión
- ❌ Mensaje de "Sandbox" en cada respuesta
- ❌ No profesional para clientes

**Con número propio:**
- ✅ Cualquier usuario puede escribirte
- ✅ Sin mensajes de sandbox
- ✅ Imagen profesional
- ✅ Verificación de negocio (check verde)

---

## 🚀 ¿Cuál elegir?

**¿Tienes presupuesto $0?**
→ WhatsApp Cloud API (Meta) - Gratis pero más complejo

**¿Quieres algo simple y tienes $20/mes?**
→ Twilio con número propio

**¿Solo para pruebas?**
→ Sandbox de Twilio (actual)

---

## 📞 Ayuda adicional:

- Meta Cloud API Docs: https://developers.facebook.com/docs/whatsapp/cloud-api
- Twilio WhatsApp Docs: https://www.twilio.com/docs/whatsapp
- Tutorial Meta: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

¿Necesitas ayuda para configurar alguna de estas opciones?
