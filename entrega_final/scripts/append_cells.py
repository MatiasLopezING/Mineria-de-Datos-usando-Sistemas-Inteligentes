import json

def update_analisis():
    path = '/home/taci/unlp/midusi/entrega_final/notebooks/analisis_tecnico.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells_to_add = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Justificación de k=3 y clustering de más atributos\n", "Se utilizará el método del codo y el puntaje de silueta para justificar la elección de $k=3$."]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "execution_count": None,
            "source": [
                "from sklearn.cluster import KMeans\n",
                "from sklearn.preprocessing import StandardScaler\n",
                "from sklearn.metrics import silhouette_score\n",
                "import matplotlib.pyplot as plt\n",
                "import pandas as pd\n",
                "\n",
                "cols_cluster = ['splm', 'str_acc', 'sapm', 'str_def', 'td_avg', 'td_acc', 'td_def', 'sub_avg']\n",
                "X_cluster = fighters_long[cols_cluster].dropna()\n",
                "scaler = StandardScaler()\n",
                "X_scaled = scaler.fit_transform(X_cluster)\n",
                "\n",
                "inertias = []\n",
                "sil_scores = []\n",
                "K_range = range(2, 8)\n",
                "\n",
                "for k in K_range:\n",
                "    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
                "    kmeans.fit(X_scaled)\n",
                "    inertias.append(kmeans.inertia_)\n",
                "    sil_scores.append(silhouette_score(X_scaled, kmeans.labels_))\n",
                "\n",
                "fig, ax1 = plt.subplots(figsize=(8,5))\n",
                "ax1.plot(K_range, inertias, marker='o', color='b', label='Inercia (Elbow)')\n",
                "ax1.set_xlabel('Número de clusters (k)')\n",
                "ax1.set_ylabel('Inercia', color='b')\n",
                "\n",
                "ax2 = ax1.twinx()\n",
                "ax2.plot(K_range, sil_scores, marker='s', color='r', label='Silhouette')\n",
                "ax2.set_ylabel('Silhouette Score', color='r')\n",
                "plt.title('Método del Codo y Silhouette')\n",
                "plt.show()\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["El gráfico anterior permite justificar la elección de $k=3$. Procedemos a analizar los centroides para describir los clusters, atributo por atributo."]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "execution_count": None,
            "source": [
                "kmeans3 = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
                "fighters_long['cluster'] = kmeans3.fit_predict(X_scaled)\n",
                "\n",
                "# Inversión del escalado para interpretar los centroides en su escala original\n",
                "centroids_original = scaler.inverse_transform(kmeans3.cluster_centers_)\n",
                "df_centroids = pd.DataFrame(centroids_original, columns=cols_cluster)\n",
                "df_centroids.index.name = 'Cluster'\n",
                "display(df_centroids)\n"
            ]
        }
    ]
    
    nb['cells'].extend(cells_to_add)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

def update_conclusiones():
    path = '/home/taci/unlp/midusi/entrega_final/notebooks/conclusiones.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells_to_add = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Evaluación extendida y Baseline\n", "Se presenta el modelo base (baseline), un Árbol de Decisión, y las métricas detalladas por clase tanto en Train como en Test (matriz de confusión, precision, recall, f1)."]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "execution_count": None,
            "source": [
                "from sklearn.tree import DecisionTreeClassifier\n",
                "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score\n",
                "import time\n",
                "\n",
                "# Baseline\n",
                "baseline_rojo = 711\n",
                "baseline_azul = 506\n",
                "total_baseline = baseline_rojo + baseline_azul\n",
                "baseline_acc = baseline_rojo / total_baseline\n",
                "print(f\"Baseline: {baseline_rojo} victorias del rojo, {baseline_azul} del azul => {baseline_acc:.2%} de predecir siempre rojo.\")\n",
                "\n",
                "# Entrenar Árbol de Decisión\n",
                "dt_model = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42, class_weight='balanced')\n",
                "start_time = time.time()\n",
                "dt_model.fit(X_train, y_train)\n",
                "dt_time = time.time() - start_time\n",
                "print(f\"Tiempo de entrenamiento (Árbol de Decisión): {dt_time:.4f} segundos\")\n",
                "\n",
                "y_train_pred = dt_model.predict(X_train)\n",
                "y_test_pred = dt_model.predict(X_test)\n",
                "\n",
                "tree_acc = accuracy_score(y_test, y_test_pred)\n",
                "mejora_pp = (tree_acc - baseline_acc) * 100\n",
                "print(f\"Precisión del árbol en test: {tree_acc:.2%}\")\n",
                "print(f\"Mejora con respecto al baseline: {mejora_pp:.2f} puntos porcentuales (pp).\")\n",
                "\n",
                "print(\"\\n--- Métricas en Train ---\")\n",
                "print(classification_report(y_train, y_train_pred, target_names=['Gana Azul (0)', 'Gana Rojo (1)']))\n",
                "print(\"\\nMatriz de Confusión (Train):\")\n",
                "print(confusion_matrix(y_train, y_train_pred))\n",
                "\n",
                "print(\"\\n--- Métricas en Test ---\")\n",
                "print(classification_report(y_test, y_test_pred, target_names=['Gana Azul (0)', 'Gana Rojo (1)']))\n",
                "print(\"\\nMatriz de Confusión (Test):\")\n",
                "print(confusion_matrix(y_test, y_test_pred))\n"
            ]
        }
    ]

    nb['cells'].extend(cells_to_add)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

if __name__ == '__main__':
    update_analisis()
    update_conclusiones()
