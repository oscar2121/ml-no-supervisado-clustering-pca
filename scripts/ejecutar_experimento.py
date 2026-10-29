import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

OUT_DIR = r"C:\Users\oscar\.gemini\antigravity\scratch\ml_no_supervisado\figures"
os.makedirs(OUT_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 150

# 1. Dataset & Scaling
raw_data = load_wine()
df = pd.DataFrame(data=raw_data.data, columns=raw_data.feature_names)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)
df_scaled = pd.DataFrame(X_scaled, columns=df.columns)

# Fig 1: Correlation
plt.figure(figsize=(9, 7))
corr_matrix = df_scaled.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, cmap='vlag', center=0, annot=True, fmt='.2f', 
            linewidths=0.5, cbar_kws={'label': 'Coeficiente de Correlación de Pearson'})
plt.title("Figura 1. Matriz de Correlaciones Físico-Químicas", pad=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig1_correlation.png"))
plt.close()

# Fig 2: PCA Scree
pca_full = PCA(random_state=42)
pca_full.fit(X_scaled)
var_exp = pca_full.explained_variance_ratio_
cum_var_exp = np.cumsum(var_exp)

fig, ax1 = plt.subplots(figsize=(8, 4.5))
color = '#1f77b4'
ax1.set_xlabel('Componente Principal (PC)')
ax1.set_ylabel('Varianza Explicada Individual', color=color)
ax1.bar(range(1, 14), var_exp, alpha=0.7, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(range(1, 14))

ax2 = ax1.twinx()
color = '#d62728'
ax2.set_ylabel('Varianza Explicada Acumulada', color=color)
ax2.plot(range(1, 14), cum_var_exp, color=color, marker='o', linewidth=2)
ax2.axhline(y=0.80, color='gray', linestyle='--', alpha=0.7, label='Umbral 80%')
ax2.tick_params(axis='y', labelcolor=color)
plt.title('Figura 2. Gráfico de Sedimentación (Scree Plot) y Varianza Acumulada', fontweight='bold')
fig.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig2_pca_scree.png"))
plt.close()

# Fig 3: PCA Loadings
loadings = pd.DataFrame(pca_full.components_[:2].T, columns=['PC1', 'PC2'], index=df.columns)
plt.figure(figsize=(10, 5))
sns.barplot(data=loadings.reset_index().melt(id_vars='index'), x='index', y='value', hue='variable', palette='Set1')
plt.xticks(rotation=45, ha='right')
plt.title("Figura 3. Cargas Factoriales (Loadings) en PC1 y PC2", fontweight='bold')
plt.xlabel("Variables Físico-Químicas")
plt.ylabel("Carga Factorial (Peso)")
plt.axhline(0, color='black', linewidth=0.8)
plt.legend(title='Componente')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig3_pca_loadings.png"))
plt.close()

# Fig 4: PCA vs SVD
pca_2d = PCA(n_components=2, random_state=42)
X_pca_2d = pca_2d.fit_transform(X_scaled)
svd = TruncatedSVD(n_components=2, random_state=42)
X_svd_2d = svd.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], color='#2ca02c', alpha=0.7, edgecolors='k')
axes[0].set_title(f"Proyección PCA 2D ({pca_2d.explained_variance_ratio_.sum()*100:.1f}% Varianza)")
axes[0].set_xlabel("PC1")
axes[0].set_ylabel("PC2")

axes[1].scatter(X_svd_2d[:, 0], X_svd_2d[:, 1], color='#9467bd', alpha=0.7, edgecolors='k')
axes[1].set_title(f"Proyección TruncatedSVD 2D ({svd.explained_variance_ratio_.sum()*100:.1f}% Varianza)")
axes[1].set_xlabel("Dimensión Singular 1")
axes[1].set_ylabel("Dimensión Singular 2")
plt.suptitle("Figura 4. Comparación Geométrica entre Proyecciones PCA y SVD", fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig4_pca_vs_svd.png"))
plt.close()

# Fig 5: Elbow & Silhouette
k_range = range(2, 9)
inertias, silhouettes = [], []
for k in k_range:
    km = KMeans(n_clusters=k, n_init=15, random_state=42)
    labs = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labs))

fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
color = '#1f77b4'
ax1.set_xlabel('Número de Clusters (k)')
ax1.set_ylabel('Inercia WCSS', color=color)
ax1.plot(k_range, inertias, marker='s', color=color, linewidth=2)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel('Silhouette Score Promedio', color=color)
ax2.plot(k_range, silhouettes, marker='o', color=color, linewidth=2, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)
ax1.axvline(x=3, color='#d62728', linestyle=':', linewidth=2, label='k óptimo = 3')
plt.title('Figura 5. Determinación de k Óptimo: Método del Codo vs Coeficiente de Silueta', fontweight='bold')
fig.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig5_elbow_silhouette.png"))
plt.close()

# Fig 6: KMeans 2D PCA
kmeans_opt = KMeans(n_clusters=3, n_init=20, random_state=42)
kmeans_labels = kmeans_opt.fit_predict(X_scaled)
centroids_pca = pca_2d.transform(kmeans_opt.cluster_centers_)

plt.figure(figsize=(8, 5))
palette = ['#e41a1c', '#377eb8', '#4daf4a']
for c_idx in range(3):
    pts = X_pca_2d[kmeans_labels == c_idx]
    plt.scatter(pts[:, 0], pts[:, 1], s=50, alpha=0.8, color=palette[c_idx], label=f'Cluster {c_idx}')
plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], s=220, c='yellow', marker='*', edgecolors='black', linewidth=1.5, label='Centroides')
plt.title('Figura 6. Clusters Asignados por K-Means (k=3) Proyectados en PC1 y PC2', fontweight='bold')
plt.xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% varianza)')
plt.ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% varianza)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig6_kmeans_pca.png"))
plt.close()

# Fig 7: Dendrogram
linkage_matrix = linkage(X_scaled, method='ward', metric='euclidean')
plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix, truncate_mode='lastp', p=30, leaf_rotation=90., leaf_font_size=9., show_contracted=True)
plt.axhline(y=25.0, color='black', linestyle='--', linewidth=1.5, label='Línea de Corte (h = 25.0)')
plt.title('Figura 7. Dendrograma de Clustering Jerárquico Aglomerativo (Ward)', fontweight='bold')
plt.xlabel('Sub-clusters fusionados')
plt.ylabel('Distancia de Ward')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig7_dendrogram.png"))
plt.close()

# Fig 8: KMeans vs Hierarchical
agg_clustering = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
agg_labels = agg_clustering.fit_predict(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
for i, (labels, title) in enumerate([(kmeans_labels, "K-Means (k=3)"), (agg_labels, "Clustering Jerárquico Ward (k=3)")]):
    for c_idx in range(3):
        pts = X_pca_2d[labels == c_idx]
        axes[i].scatter(pts[:, 0], pts[:, 1], s=40, alpha=0.8, label=f'Cluster {c_idx}')
    axes[i].set_title(title)
    axes[i].set_xlabel("PC1")
    axes[i].set_ylabel("PC2")
    axes[i].legend()
plt.suptitle("Figura 8. Comparativa de Particiones: K-Means vs Clustering Jerárquico", fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig8_kmeans_vs_hierarchical.png"))
plt.close()

# Fig 9: Profiling Boxplots
df['Cluster'] = kmeans_labels
features_clave = ['alcohol', 'flavanoids', 'total_phenols', 'color_intensity', 'proline']
fig, axes = plt.subplots(1, len(features_clave), figsize=(14, 3.8))
for idx, feat in enumerate(features_clave):
    sns.boxplot(data=df, x='Cluster', y=feat, ax=axes[idx], palette='Set2')
    axes[idx].set_title(feat)
    axes[idx].set_xlabel("Cluster")
plt.suptitle("Figura 9. Distribución de Variables Clave en los 3 Conglomerados", fontweight='bold', y=1.04)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig9_cluster_profiles.png"))
plt.close()

print("¡Todas las figuras han sido generadas y guardadas exitosamente en 'figures/'!")
