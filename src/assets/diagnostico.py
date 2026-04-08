import google.generativeai as genai

genai.configure(api_key="AIzaSyC2966gZooFxYRb3Z4hDgbCc9Sa6h1pF94")

print("🔍 Buscando modelos disponibles para tu cuenta...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Modelo válido encontrado: {m.name}")
except Exception as e:
    print(f"Error al conectar: {e}")