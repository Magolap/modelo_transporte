import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
archivo = "transporte.csv"
df = pd.read_csv(archivo)

# Ver columnas disponibles
print("Columnas disponibles en el archivo:")
print(df.columns)

# Seleccionar columnas numéricas con los nombres correctos
columnas_usadas = ['hora_pico', 'lluvia', 'retraso', 'costo']
for col in columnas_usadas:
    if col not in df.columns:
        raise ValueError(f"La columna '{col}' no existe en el archivo CSV.")

X = df[columnas_usadas]

# Aplicar KMeans con 3 grupos
kmeans = KMeans(n_clusters=3, random_state=42)
df['grupo'] = kmeans.fit_predict(X)

# Ver grupos asignados
print(df[['origen', 'destino', 'grupo']])

# Visualización
sns.pairplot(df, vars=columnas_usadas, hue='grupo', diag_kind='kde')
plt.suptitle('Visualización de Agrupamientos', y=1.02)
plt.show()
