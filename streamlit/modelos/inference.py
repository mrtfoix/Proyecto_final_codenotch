from joblib import load
import pandas as pd

model = load('streamlit/modelos/modelo_proyecto.joblib')

def inference1(X):
    y_proba = model.predict_proba([X])[0]
    return y_proba[1]

def inference2(X):
    resultados = {'inferencia': [], 'probabilidad de cancelación (%)': []}
    y_prob = model.predict_proba(X)[:,1]
    for i,prob in enumerate(y_prob):
        porcentaje = round(prob*100,2)
        resultados['inferencia'].append(i+1)
        resultados['probabilidad de cancelación (%)'].append(porcentaje)
        resultados_df = pd.DataFrame(resultados)
    return resultados_df
