"""
Script de prueba para verificar que la configuración es correcta
"""
import sys
import os

def test_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (se requiere 3.10+)")
        return False

def test_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    required = ['flask', 'requests', 'dotenv', 'twilio', 'groq']
    missing = []
    
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (no instalado)")
            missing.append(package)
    
    if missing:
        print(f"\n   💡 Instala las dependencias faltantes:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True

def test_env_file():
    """Verifica que el archivo .env exista"""
    print("\n📄 Verificando archivo .env...")
    if os.path.exists('.env'):
        print("   ✅ Archivo .env encontrado")
        return True
    else:
        print("   ❌ Archivo .env no encontrado")
        print("   💡 Copia .env.example a .env y configura tus credenciales:")
        print("   cp .env.example .env")
        return False

def test_config():
    """Verifica la configuración"""
    print("\n⚙️  Verificando configuración...")
    try:
        import config
        
        # Verificar AI Provider
        if config.AI_PROVIDER:
            print(f"   ✅ AI Provider: {config.AI_PROVIDER}")
        else:
            print("   ❌ AI_PROVIDER no configurado")
            return False
        
        # Verificar API Key según el proveedor
        if config.AI_PROVIDER == 'groq':
            if config.GROQ_API_KEY and config.GROQ_API_KEY != 'gsk_your-groq-api-key-here':
                print(f"   ✅ GROQ_API_KEY configurada")
            else:
                print("   ❌ GROQ_API_KEY no configurada o usando valor de ejemplo")
                return False
        elif config.AI_PROVIDER == 'cohere':
            if config.COHERE_API_KEY:
                print(f"   ✅ COHERE_API_KEY configurada")
            else:
                print("   ❌ COHERE_API_KEY no configurada")
                return False
        elif config.AI_PROVIDER == 'huggingface':
            if config.HUGGINGFACE_API_KEY:
                print(f"   ✅ HUGGINGFACE_API_KEY configurada")
            else:
                print("   ❌ HUGGINGFACE_API_KEY no configurada")
                return False
        
        # Verificar Twilio
        if config.TWILIO_ACCOUNT_SID and config.TWILIO_ACCOUNT_SID != 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
            print(f"   ✅ TWILIO_ACCOUNT_SID configurado")
        else:
            print("   ❌ TWILIO_ACCOUNT_SID no configurado o usando valor de ejemplo")
            return False
        
        if config.TWILIO_AUTH_TOKEN and config.TWILIO_AUTH_TOKEN != 'your-twilio-auth-token-here':
            print(f"   ✅ TWILIO_AUTH_TOKEN configurado")
        else:
            print("   ❌ TWILIO_AUTH_TOKEN no configurado o usando valor de ejemplo")
            return False
        
        print(f"   ✅ Puerto: {config.PORT}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error al cargar configuración: {e}")
        return False

def test_ai_connection():
    """Prueba la conexión con la API de IA"""
    print("\n🤖 Probando conexión con IA...")
    try:
        from ai_service import ai_service
        
        # Mensaje de prueba simple
        test_messages = [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Di 'hola' en una palabra."}
        ]
        
        response = ai_service.get_response(test_messages)
        
        if response and len(response) > 0:
            print(f"   ✅ Conexión exitosa con {ai_service.provider}")
            print(f"   📝 Respuesta de prueba: {response[:50]}...")
            return True
        else:
            print(f"   ❌ Respuesta vacía de {ai_service.provider}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error al conectar con IA: {e}")
        print(f"   💡 Verifica tu API key y conexión a internet")
        return False

def test_twilio_connection():
    """Prueba la conexión con Twilio"""
    print("\n📱 Probando conexión con Twilio...")
    try:
        from whatsapp_service import whatsapp_service
        
        # Solo verificar que el cliente se inicializó
        if whatsapp_service.client:
            print(f"   ✅ Cliente de Twilio inicializado")
            print(f"   📞 Número WhatsApp: {whatsapp_service.from_number}")
            return True
        else:
            print("   ❌ Error al inicializar cliente de Twilio")
            return False
            
    except Exception as e:
        print(f"   ❌ Error al conectar con Twilio: {e}")
        print(f"   💡 Verifica tus credenciales de Twilio")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DEL CHATBOT")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Environment File", test_env_file()))
    results.append(("Configuration", test_config()))
    results.append(("AI Connection", test_ai_connection()))
    results.append(("Twilio Connection", test_twilio_connection()))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡TODO LISTO! Puedes iniciar el servidor con:")
        print("   python main.py")
        print("\n   Y en otra terminal:")
        print("   ngrok http 5000")
    else:
        print("⚠️  Hay problemas que resolver antes de continuar.")
        print("   Revisa los errores arriba y consulta INICIO_RAPIDO.md")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    exit(main())
