#!/usr/bin/env python3
"""
Script para iniciar ngrok y exponer el servidor Flask.
Muestra la URL pública que debes configurar en Twilio.
"""

import subprocess
import sys
import time
import requests
import json

def check_ngrok_installed():
    """Verifica si ngrok está instalado."""
    try:
        subprocess.run(["ngrok", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def start_ngrok(port=5000):
    """Inicia ngrok en el puerto especificado."""
    print("=" * 60)
    print("🚇 Iniciando ngrok...")
    print("=" * 60)
    print()
    
    if not check_ngrok_installed():
        print("❌ ngrok no está instalado.")
        print("\n📥 Para instalarlo:")
        print("\nEn macOS:")
        print("  brew install ngrok")
        print("\nO descárgalo de: https://ngrok.com/download")
        print("\nDespués de instalarlo, ejecuta:")
        print("  ngrok config add-authtoken TU_TOKEN")
        print("  (Obtén tu token de: https://dashboard.ngrok.com/get-started/your-authtoken)")
        return False
    
    try:
        # Iniciar ngrok
        print(f"🔄 Exponiendo puerto {port} al internet...")
        process = subprocess.Popen(
            ["ngrok", "http", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Esperar a que ngrok inicie
        print("⏳ Esperando a que ngrok inicie...")
        time.sleep(3)
        
        # Obtener la URL pública de ngrok
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()
            
            if tunnels.get("tunnels"):
                public_url = tunnels["tunnels"][0]["public_url"]
                
                print("\n" + "=" * 60)
                print("✅ ngrok está corriendo!")
                print("=" * 60)
                print(f"\n🌐 URL Pública: {public_url}")
                print(f"\n📱 Webhook URL para Twilio:")
                print(f"   {public_url}/whatsapp")
                print(f"\n🧪 Para probar el calendario (desde tu navegador):")
                print(f"   {public_url}/test-calendar")
                print(f"\n❤️  Health Check:")
                print(f"   {public_url}/health")
                print("\n" + "=" * 60)
                print("\n📋 Pasos siguientes:")
                print("1. Ve a https://console.twilio.com/")
                print("2. Navega a: Messaging → Try it out → WhatsApp Sandbox")
                print("3. En 'When a message comes in', pega:")
                print(f"   {public_url}/whatsapp")
                print("4. Selecciona método: POST")
                print("5. Guarda los cambios")
                print("\n💡 ngrok seguirá corriendo. Presiona Ctrl+C para detener.")
                print("=" * 60)
                print()
                
                # Mantener el proceso corriendo
                process.wait()
                
            else:
                print("❌ No se pudo obtener la URL de ngrok")
                print("Intenta manualmente: ngrok http 5000")
                return False
                
        except requests.exceptions.ConnectionError:
            print("⚠️  No se pudo conectar a la API de ngrok")
            print(f"✅ Pero ngrok debería estar corriendo en el puerto {port}")
            print("\n🌐 Para ver la URL, abre: http://localhost:4040")
            print("💡 ngrok seguirá corriendo. Presiona Ctrl+C para detener.")
            
            # Mantener el proceso corriendo
            process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo ngrok...")
        process.terminate()
        print("✅ ngrok detenido.")
        return True
    except Exception as e:
        print(f"\n❌ Error al iniciar ngrok: {e}")
        return False

if __name__ == "__main__":
    port = 5000
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("⚠️  Puerto inválido. Usando puerto 5000 por defecto.")
    
    print("🚀 Script de inicio de ngrok para WhatsApp Calendar Bot\n")
    start_ngrok(port)
