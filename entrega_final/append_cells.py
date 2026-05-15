import json

c1 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, roc_curve, auc

# ==========================================
# 1. Preparación de variables y Manejo de NaNs
# ==========================================
# Armamos un dataset apilado (ganadores vs perdedores) a partir de eda_wl_clean
w_cols = ['w_height', 'w_reach', 'w_str_acc', 'w_td_acc', 'w_str_def', 'w_td_def', 'w_sapm', 'w_splm']
l_cols = ['l_height', 'l_reach', 'l_str_acc', 'l_td_acc', 'l_str_def', 'l_td_def', 'l_sapm', 'l_splm']
common_cols = ['height', 'reach', 'str_acc', 'td_acc', 'str_def', 'td_def', 'sapm', 'splm']

df_w = eda_wl_clean[w_cols].copy()
df_w.columns = common_cols
df_w['is_winner'] = 1

df_l = eda_wl_clean[l_cols].copy()
df_l.columns = common_cols
df_l['is_winner'] = 0

df_q1 = pd.concat([df_w, df_l], ignore_index=True)
df_q1 = df_q1.dropna(subset=['is_winner'])

X = df_q1[common_cols]
y = df_q1['is_winner']

# Imputación de NaNs usando la mediana
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# ==========================================
# 2. Entrenamiento del Modelo (Random Forest)
# ==========================================
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, class_weight='balanced')
rf_model.fit(X_train, y_train)

# ==========================================
# 3. Función predictiva
# ==========================================
def predict_win_probability(fighter_stats, model, imp):
    stats_imputed = imp.transform(fighter_stats)
    return model.predict_proba(stats_imputed)[0][1]

# ==========================================
# 4. Evaluación del Modelo (Matriz y Curva ROC)
# ==========================================
y_pred = rf_model.predict(X_test)
y_proba = rf_model.predict_proba(X_test)[:, 1]

fig, ax = plt.subplots(1, 2, figsize=(14, 5))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title('Matriz de Confusión', fontsize=14)
ax[0].set_xlabel('Predicción (0=Pierde, 1=Gana)')
ax[0].set_ylabel('Realidad')

fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)
ax[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (AUC = {roc_auc:.2f})')
ax[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
ax[1].set_title('Curva ROC', fontsize=14)
ax[1].set_xlabel('Tasa de Falsos Positivos (FPR)')
ax[1].set_ylabel('Tasa de Verdaderos Positivos (TPR)')
ax[1].legend(loc="lower right")

plt.tight_layout()
plt.show()"""

c2 = """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules

# ==========================================
# 1. Discretización de variables continuas
# ==========================================
df_q2 = df_q1.copy()

df_q2['Altura_Rango'] = pd.qcut(df_q2['height'], q=3, labels=['Baja', 'Media', 'Alta'])
df_q2['Alcance_Rango'] = pd.qcut(df_q2['reach'], q=3, labels=['Corto', 'Medio', 'Largo'])
df_q2['Resultado'] = df_q2['is_winner'].map({1: 'Victoria', 0: 'Derrota'})

cols_apriori = ['Altura_Rango', 'Alcance_Rango', 'Resultado'] 
df_apriori = df_q2[cols_apriori].dropna()
df_dummies = pd.get_dummies(df_apriori).astype(bool)

# ==========================================
# 2. Algoritmo Apriori para extracción de reglas
# ==========================================
frequent_itemsets = apriori(df_dummies, min_support=0.03, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

# ==========================================
# 3. Filtrado por "Victoria"
# ==========================================
reglas_victoria = rules[rules['consequents'].apply(lambda x: 'Resultado_Victoria' in x)].copy()
reglas_top = reglas_victoria.sort_values(by=['lift', 'confidence'], ascending=[False, False])
print("Top 5 reglas que maximizan las chances de victoria:")
display(reglas_top.head(5)[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# ==========================================
# 4. Visualización de Soporte vs Confianza
# ==========================================
plt.figure(figsize=(10, 6))
reglas_victoria['Cant_Condiciones'] = reglas_victoria['antecedents'].apply(lambda x: len(x))

sns.scatterplot(
    x="support", y="confidence", 
    size="lift", hue="Cant_Condiciones", 
    data=reglas_victoria, palette="deep", sizes=(50, 400), alpha=0.8
)
plt.title("Reglas de Asociación para Victoria (Apriori)", fontsize=16)
plt.xlabel("Soporte (¿Qué tan común es este perfil en UFC?)")
plt.ylabel("Confianza (Tasa de victoria de este perfil)")
plt.axhline(y=0.5, color='r', linestyle='--', label='50% Win Rate')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.show()"""

c3 = """from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ==========================================
# 1. Selección y Normalización
# ==========================================
vars_fisicas = ['height', 'reach'] 
df_q3 = df_q1.dropna(subset=vars_fisicas).copy()
X_fisico = df_q3[vars_fisicas]

scaler_km = StandardScaler()
X_scaled = scaler_km.fit_transform(X_fisico)

# ==========================================
# 2. Búsqueda del K Óptimo (Elbow Method)
# ==========================================
sse = []
K_range = range(2, 9)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    sse.append(km.inertia_)

fig, ax = plt.subplots(1, 2, figsize=(16, 5))
ax[0].plot(K_range, sse, marker='o', color='purple', lw=2)
ax[0].set_title('Método del Codo (Elbow Method)', fontsize=14)
ax[0].set_xlabel('Número de clusters (K)')
ax[0].set_ylabel('Inercia (SSE)')

# ==========================================
# 3. Aplicar K-Means con K Óptimo
# ==========================================
K_optimo = 3 
kmeans = KMeans(n_clusters=K_optimo, random_state=42, n_init=10)
df_q3['Biotipo_Cluster'] = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_q3['PCA1'] = X_pca[:, 0]
df_q3['PCA2'] = X_pca[:, 1]

sns.scatterplot(x='PCA1', y='PCA2', hue='Biotipo_Cluster', palette='tab10', data=df_q3, alpha=0.7, ax=ax[1])
ax[1].set_title(f'Visualización 2D de Perfiles (PCA) - {K_optimo} Biotipos', fontsize=14)

# ==========================================
# 4. Cruce Morfológico con Estilos de Lucha
# ==========================================
vars_estilo = ['str_acc', 'td_acc', 'splm', 'sapm'] 
df_perfiles = df_q3.dropna(subset=vars_estilo)

resumen_clusters = df_perfiles.groupby('Biotipo_Cluster')[vars_fisicas + vars_estilo].mean().round(2)
print("Características Físicas Promedio + Métricas de Estilo de Lucha:")
display(resumen_clusters)

win_rate_cluster = df_perfiles.groupby('Biotipo_Cluster')['is_winner'].mean().round(3) * 100
print("\\nTasa de Victorias por Biotipo (%):")
display(win_rate_cluster)

# ==========================================
# 5. Visualización: Parallel Coordinates (Estilos de Lucha)
# ==========================================
from sklearn.preprocessing import MinMaxScaler
scaler_pc = MinMaxScaler()
df_estilos_scaled = pd.DataFrame(scaler_pc.fit_transform(df_perfiles[vars_estilo]), columns=vars_estilo)
df_estilos_scaled['Biotipo_Cluster'] = df_perfiles['Biotipo_Cluster'].values
df_sample_pc = df_estilos_scaled.groupby('Biotipo_Cluster').sample(n=50, random_state=42)

plt.figure(figsize=(12, 6))
pd.plotting.parallel_coordinates(df_sample_pc, 'Biotipo_Cluster', colormap=plt.cm.tab10, alpha=0.3, linewidth=2)
plt.title('Parallel Coordinates: Comparativa de Estilos de Lucha por Biotipo Físico', fontsize=16)
plt.xticks(rotation=15)
promedios_scaled = df_estilos_scaled.groupby('Biotipo_Cluster').mean()
for i, cluster in enumerate(promedios_scaled.index):
    plt.plot(promedios_scaled.columns, promedios_scaled.loc[cluster], lw=4, label=f'Promedio Cluster {cluster}', color=plt.cm.tab10(i))

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[-K_optimo:], labels[-K_optimo:], loc='upper right')
plt.tight_layout()
plt.show()"""

with open('Pfinal.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for code in [c1, c2, c3]:
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")]
    }
    nb["cells"].append(new_cell)

with open('Pfinal.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cells added.")
