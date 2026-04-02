import pyodbc
import pandas as pd
import warnings

# Silenciar el warning de Pandas
warnings.filterwarnings('ignore', category=UserWarning)

def extraer_datos_fidelmira():
    server = '172.16.40.16'
    database = 'Fidelmira'
    user = 'consulta'
    password = 'cs654321$'
    
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
    )
    
    # Query construida con los nombres de columna EXACTOS de tu base de datos
    query = """
    SELECT 
        LEFT(c.PCCODI, 1) as Tipo,
        c.PCCODI as Codigo, 
        c.PCDESC as Cuenta,
        SUM(m.MovDebe - m.MovHaber) as Saldo_Actual
    FROM softland.cwmovim m
    INNER JOIN softland.cwpctas c ON m.PctCod = c.PCCODI
    WHERE m.CpbFec >= '2026-01-01' 
    GROUP BY c.PCCODI, c.PCDESC
    HAVING SUM(m.MovDebe - m.MovHaber) <> 0
    ORDER BY c.PCCODI
    """
    
    try:
        print(f"🔗 Conectando a {database} en {server}...")
        with pyodbc.connect(conn_str, timeout=10) as conn:
            print("✅ ¡CONEXIÓN EXITOSA!")
            df = pd.read_sql(query, conn)
            return df
            
    except Exception as e:
        print(f"❌ Error al conectar o consultar: {e}")
        return None

if __name__ == "__main__":
    df = extraer_datos_fidelmira()
    
    if df is not None and not df.empty:
        print("\n--- Vista previa de saldos ---")
        print(df.head())
        
        # 1. Generamos el JSON estructurado para cargar en Vue.js
        df.to_json("fidelmira_dashboard.json", orient="records")
        print(f"\n🚀 Archivo 'fidelmira_dashboard.json' generado con {len(df)} registros.")
        
        # 2. Validación de negocio
        activos = df[df['Tipo'] == '1']['Saldo_Actual'].sum()
        pasivos = df[df['Tipo'] == '2']['Saldo_Actual'].sum()
        
        print(f"💰 Total Activos (Tipo 1): ${activos:,.0f}")
        print(f"📉 Total Pasivos (Tipo 2): ${pasivos:,.0f}")
    else:
        print("\n⚠️ No se obtuvieron datos. Verifica si hay movimientos en 2026.")