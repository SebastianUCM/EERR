from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse # <-- NUEVA IMPORTACIÓN
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import json

# 1. Configuración de la API
genai.configure(api_key="AIzaSyC2966gZooFxYRb3Z4hDgbCc9Sa6h1pF94") # <-- ¡TU CLAVE REAL AQUÍ!
modelo = genai.GenerativeModel('models/gemini-2.5-flash')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConsultaIA(BaseModel):
    mensaje: str
    rol: str
    empresa: str
    anio: int
    mes: int

def cargar_contexto_financiero(empresa: str, anio: int, mes: int):
    try:
        with open('datos_vue.json', 'r', encoding='utf-8') as f:
            datos_completos = json.load(f)
            
        resumen_cuentas = {}
        for d in datos_completos:
            if d.get('Empresa') == empresa and int(d.get('Anio')) == anio and int(d.get('Mes')) <= mes:
                cta = d.get("CodigoCuenta")
                if cta not in resumen_cuentas:
                    resumen_cuentas[cta] = {"Debe": 0, "Haber": 0}
                resumen_cuentas[cta]["Debe"] += d.get("TotalDebe", 0)
                resumen_cuentas[cta]["Haber"] += d.get("TotalHaber", 0)

        datos_optimizados = [
            {"Cta": k, "D": round(v["Debe"]), "H": round(v["Haber"])}
            for k, v in resumen_cuentas.items() if v["Debe"] > 0 or v["Haber"] > 0
        ]
                    
        cuentas_activas = set(resumen_cuentas.keys())
        with open('plan_cuentas.json', 'r', encoding='utf-8') as f:
            plan_completo = json.load(f)
            
        plan_optimizado = [
            {"Cta": c.get("CodigoCuenta"), "Nom": c.get("NombreCuenta")}
            for c in plan_completo
            if c.get('Empresa') == empresa and c.get("CodigoCuenta") in cuentas_activas
        ]

        return json.dumps(datos_optimizados, separators=(',', ':')), json.dumps(plan_optimizado, separators=(',', ':'))
    except Exception as e:
        print(f"Error agrupando JSON: {e}")
        return "[]", "[]"

@app.post("/chat")
async def chat_financiero(consulta: ConsultaIA):
    
    datos_json, plan_json = cargar_contexto_financiero(consulta.empresa, consulta.anio, consulta.mes)

    if consulta.rol == 'analista':
        prompt_sistema = f"""
        Eres un Analista Financiero Senior. Analiza el Balance de Comprobación acumulado a MES {consulta.mes} del AÑO {consulta.anio} de {consulta.empresa}.
        DATOS: {datos_json}
        CUENTAS: {plan_json}
        Responde la pregunta del usuario evaluando rentabilidad y gastos. Sé directo y usa montos en pesos chilenos.
        """
    else: 
        prompt_sistema = f"""
        Eres un Auditor Técnico Contable. Revisa el Balance al MES {consulta.mes} del AÑO {consulta.anio} de {consulta.empresa}.
        CUENTAS: {plan_json}
        SALDOS: {datos_json}
        Responde dudas técnicas sobre cuentas y descuadres.
        """

    prompt_final = f"{prompt_sistema}\n\nPregunta: {consulta.mensaje}"

    try:
        # AQUÍ OCURRE LA MAGIA DEL STREAMING
        respuesta_stream = modelo.generate_content(prompt_final, stream=True)

        def generador_respuesta():
            for pedazo in respuesta_stream:
                if pedazo.text:
                    yield pedazo.text # Vamos enviando palabra por palabra

        # Devolvemos un flujo continuo en lugar de un bloque de texto estático
        return StreamingResponse(generador_respuesta(), media_type="text/plain")

    except Exception as e:
        print(f"\n❌ ERROR DE GEMINI: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)