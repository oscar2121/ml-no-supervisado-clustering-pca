# Técnicas de Machine Learning No Supervisado: Clustering y Reducción de Dimensionalidad

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oscar2121/ml-no-supervisado-clustering-pca/blob/main/notebooks/Machine_Learning_No_Supervisado_Clustering_PCA_SVD.ipynb)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-v1.3%2B-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Este repositorio contiene la implementación experimental, el análisis conceptual y los entregables correspondientes al proyecto de **Machine Learning No Supervisado**, enfocado en la aplicación rigurosa de algoritmos de **Clustering** (K-Means y Clustering Jerárquico Aglomerativo) y técnicas de **Reducción de Dimensionalidad** (Análisis de Componentes Principales - PCA y Descomposición en Valores Singulares - SVD).

---

## 📌 Contenido del Proyecto

1. **Comprensión Conceptual**:
   - Fundamentos del aprendizaje no supervisado y modelado de distribuciones $p(x)$ sin etiquetas de entrenamiento.
   - La *Maldición de la Dimensionalidad* (*Curse of Dimensionality*) y su impacto en distancias euclidianas.
   - Reducción lineal de dimensionalidad: PCA (descomposición espectral y varianza proyectada) y SVD (factorización de matrices $X = U \Sigma V^T$).
   - Algoritmos de clustering: optimización iterativa de Lloyd en K-Means y jerarquía ascendente de Ward en Clustering Jerárquico.
   - Validación intrínseca: Método del Codo (WCSS), Coeficiente de Silueta (*Silhouette Score*), Índice de Davies-Bouldin e Índice de Calinski-Harabasz.

2. **Aplicación Práctica en Google Colab**:
   - Implementación sobre el **Wine Recognition Dataset** (178 muestras, 13 variables físico-químicas continuas).
   - Preprocesamiento indispensable con estandarización $Z$-score (`StandardScaler`).
   - Reducción a 2D y 3D mediante PCA (55.41% y 66.53% de varianza explicada) y demostración de equivalencia con SVD ($|r| = 1.000$).
   - Búsqueda sistemática de $k$ óptimo en K-Means ($k=3$) contrastada con el corte del Dendrograma de Ward ($h = 25.0$).
   - Visualización y perfilamiento agronómico de los conglomerados descubiertos.

---

## 📂 Estructura del Repositorio

```text
├── notebooks/
│   └── Machine_Learning_No_Supervisado_Clustering_PCA_SVD.ipynb  # Notebook interactivo para Google Colab
├── informe/
│   ├── Informe_Machine_Learning_No_Supervisado.pdf              # Informe formal final en PDF (Normas APA 7ma ed.)
│   └── Informe_Machine_Learning_No_Supervisado.docx             # Versión editable en formato Word
├── figures/                                                     # Gráficas y visualizaciones generadas
│   ├── fig1_correlation.png
│   ├── fig2_pca_scree.png
│   ├── fig3_pca_loadings.png
│   ├── fig4_pca_vs_svd.png
│   ├── fig5_elbow_silhouette.png
│   ├── fig6_kmeans_pca.png
│   ├── fig7_dendrogram.png
│   ├── fig8_kmeans_vs_hierarchical.png
│   └── fig9_cluster_profiles.png
├── scripts/
│   ├── crear_notebook.py
│   ├── ejecutar_experimento.py
│   └── generar_informe_completo.py
└── README.md
```

---

## 🚀 Cómo Ejecutar el Proyecto en Google Colab

1. **Opción Directa (1 Clic)**:
   Haz clic en el botón superior **"Open in Colab"** para abrir y ejecutar el notebook directamente en los servidores de Google sin necesidad de instalar nada en tu computadora.

2. **Opción Manual desde GitHub**:
   - Abre [Google Colab](https://colab.research.google.com/).
   - Ve a la pestaña **GitHub**.
   - Ingresa la URL de este repositorio: `https://github.com/oscar2121/ml-no-supervisado-clustering-pca`.
   - Selecciona el archivo `Machine_Learning_No_Supervisado_Clustering_PCA_SVD.ipynb`.
   - En el menú superior, selecciona **Entorno de ejecución** > **Ejecutar todas**.

---

## 📊 Resumen de Resultados Principales

| Métrica / Técnica | K-Means ($k=3$) | Clustering Jerárquico (Ward, $k=3$) |
| :--- | :---: | :---: |
| **Silhouette Score** ($-1 \le s \le 1$) | **0.2849** | 0.2774 |
| **Davies-Bouldin Index** ($\downarrow$ mejor) | **1.3892** | 1.4187 |
| **Calinski-Harabasz Index** ($\uparrow$ mejor) | **70.94** | 67.07 |
| **Varianza Explicada PCA (2 componentes)** | **55.41%** (PC1: 36.20%, PC2: 19.21%) | — |
| **Correlación Cruzada PCA vs SVD** | **\|r\| = 1.000000** | — |

---

## 📚 Referencias Bibliográficas (Normas APA 7ma Edición)

- Bishop, C. M. (2006). *Pattern recognition and machine learning*. Springer Science & Business Media.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT Press. http://www.deeplearningbook.org
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical learning: Data mining, inference, and prediction* (2nd ed.). Springer New York. https://doi.org/10.1007/978-0-387-84858-7
- Jain, A. K. (2010). Data clustering: 50 years beyond K-means. *Pattern Recognition Letters*, 31(8), 651-666. https://doi.org/10.1016/j.patrec.2009.09.011
- Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: A review and recent developments. *Philosophical Transactions of the Royal Society A*, 374(2065), 20150202. https://doi.org/10.1098/rsta.2015.0202
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
- Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65. https://doi.org/10.1016/0377-0427(87)90125-7
- Strang, G. (2016). *Introduction to linear algebra* (5th ed.). Wellesley-Cambridge Press.
- Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association*, 58(301), 236-244. https://doi.org/10.1080/01621459.1963.10500845

---
**Autor:** Oscar David  
**Curso:** Inteligencia Artificial y Machine Learning  
**Año:** 2026
