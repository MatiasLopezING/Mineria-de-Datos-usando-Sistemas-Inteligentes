import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import time
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

print("--- CLUSTERING ---")
df_podado = pd.read_csv('/home/taci/unlp/midusi/entrega_final/data/df_podado.csv')
red_cols = {
    'r_splm': 'splm', 'r_str_acc': 'str_acc', 'r_sapm': 'sapm', 'r_str_def': 'str_def',
    'r_td_avg': 'td_avg', 'r_td_avg_acc': 'td_acc', 'r_td_def': 'td_def', 'r_sub_avg': 'sub_avg'
}
blue_cols = {
    'b_splm': 'splm', 'b_str_acc': 'str_acc', 'b_sapm': 'sapm', 'b_str_def': 'str_def',
    'b_td_avg': 'td_avg', 'b_td_avg_acc': 'td_acc', 'b_td_def': 'td_def', 'b_sub_avg': 'sub_avg'
}
red_df = df_podado[list(red_cols.keys())].rename(columns=red_cols)
blue_df = df_podado[list(blue_cols.keys())].rename(columns=blue_cols)
fighters_long = pd.concat([red_df, blue_df], ignore_index=True).dropna()

cols_cluster = ['splm', 'str_acc', 'sapm', 'str_def', 'td_avg', 'td_acc', 'td_def', 'sub_avg']
X_cluster = fighters_long[cols_cluster]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

for k in range(2, 5):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia = kmeans.inertia_
    sil = silhouette_score(X_scaled, kmeans.labels_)
    print(f"k={k}: Inertia={inertia:.2f}, Silhouette={sil:.4f}")

kmeans3 = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans3.fit(X_scaled)
centroids_original = scaler.inverse_transform(kmeans3.cluster_centers_)
df_centroids = pd.DataFrame(centroids_original, columns=cols_cluster)
df_centroids.index.name = 'Cluster'
print("\nCentroids:")
print(df_centroids)

print("\n--- DECISION TREE ---")
eda_wl_clean = pd.read_csv('/home/taci/unlp/midusi/entrega_final/data/eda_wl_clean.csv')
w_cols = ['w_height', 'w_reach', 'w_str_acc', 'w_td_acc', 'w_str_def', 'w_td_def', 'w_sapm', 'w_splm']
l_cols = ['l_height', 'l_reach', 'l_str_acc', 'l_td_acc', 'l_str_def', 'l_td_def', 'l_sapm', 'l_splm']
features = ['height', 'reach', 'str_acc', 'td_acc', 'str_def', 'td_def', 'sapm', 'splm']
df_w = eda_wl_clean[w_cols].copy()
df_w.columns = features
df_w['is_winner'] = 1
df_l = eda_wl_clean[l_cols].copy()
df_l.columns = features
df_l['is_winner'] = 0
df_q1 = pd.concat([df_w, df_l], ignore_index=True).dropna(subset=['is_winner'])
X = df_q1[features]
y = df_q1['is_winner']

imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

baseline_rojo = 711
baseline_azul = 506
total_baseline = baseline_rojo + baseline_azul
baseline_acc = baseline_rojo / total_baseline
print(f"Baseline: {baseline_rojo} rojo, {baseline_azul} azul => {baseline_acc:.2%}")

dt_model = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42, class_weight='balanced')
start_time = time.time()
dt_model.fit(X_train, y_train)
dt_time = time.time() - start_time
print(f"Time: {dt_time:.4f}s")

y_train_pred = dt_model.predict(X_train)
y_test_pred = dt_model.predict(X_test)
tree_acc = accuracy_score(y_test, y_test_pred)
print(f"Accuracy Test: {tree_acc:.2%}, Mejora: {(tree_acc - baseline_acc)*100:.2f}pp")

print("\nTrain metrics:")
print(classification_report(y_train, y_train_pred))
print(confusion_matrix(y_train, y_train_pred))
print("\nTest metrics:")
print(classification_report(y_test, y_test_pred))
print(confusion_matrix(y_test, y_test_pred))
