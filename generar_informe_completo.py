import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage, Table, TableStyle
)
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\oscar\.gemini\antigravity\scratch\ml_no_supervisado"
FIG_DIR = os.path.join(BASE_DIR, "figures")
DOCX_OUT = os.path.join(BASE_DIR, "Informe_Machine_Learning_No_Supervisado.docx")
PDF_OUT = os.path.join(BASE_DIR, "Informe_Machine_Learning_No_Supervisado.pdf")

# =============================================================================
# 1. GENERACIÓN DEL DOCUMENTO EN MICROSOFT WORD (.DOCX) - APA 7MA EDICIÓN
# =============================================================================
def construir_docx():
    doc = docx.Document()
    
    # Configuración de márgenes estándar APA (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_head = p_head.add_run("Informe Académico: ML No Supervisado (Clustering y Reducción)")
        r_head.font.name = 'Times New Roman'
        r_head.font.size = Pt(9)
        r_head.font.color.rgb = RGBColor(110, 110, 110)

    def h1(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(texto)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        return p

    def h2(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(texto)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        return p

    def h3(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(texto)
        run.bold = True
        run.font.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    def parrafo(texto, sangria=True, espacio_despues=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(espacio_despues)
        p.paragraph_format.line_spacing = 1.15
        if sangria:
            p.paragraph_format.first_line_indent = Inches(0.5)
        run = p.add_run(texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    def agregar_imagen(nombre_archivo, titulo_figura, nota_figura, ancho=Inches(5.8)):
        ruta = os.path.join(FIG_DIR, nombre_archivo)
        if os.path.exists(ruta):
            p_tit = doc.add_paragraph()
            p_tit.paragraph_format.space_before = Pt(10)
            p_tit.paragraph_format.space_after = Pt(4)
            r_num = p_tit.add_run(titulo_figura.split('.')[0] + ".")
            r_num.bold = True
            r_num.font.name = 'Times New Roman'
            r_num.font.size = Pt(10)
            
            r_desc = p_tit.add_run(" " + ".".join(titulo_figura.split('.')[1:]))
            r_desc.font.italic = True
            r_desc.font.name = 'Times New Roman'
            r_desc.font.size = Pt(10)
            
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(ruta, width=ancho)
            
            p_nota = doc.add_paragraph()
            p_nota.paragraph_format.space_after = Pt(10)
            r_n = p_nota.add_run("Nota. ")
            r_n.font.italic = True
            r_n.font.name = 'Times New Roman'
            r_n.font.size = Pt(9)
            r_n_txt = p_nota.add_run(nota_figura)
            r_n_txt.font.name = 'Times New Roman'
            r_n_txt.font.size = Pt(9)

    def referencia_apa(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)

    # PORTADA
    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(40)
    
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(12)
    r_tit = p_tit.add_run("Implementación y Análisis Crítico de Algoritmos de Aprendizaje No Supervisado: Reducción de Dimensionalidad (PCA, SVD) y Modelos de Clustering (K-Means, Jerárquico Aglomerativo)")
    r_tit.bold = True
    r_tit.font.name = 'Times New Roman'
    r_tit.font.size = Pt(15)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("Informe Técnico-Práctico Desarrollado en Google Colaboratory y Repositorio en GitHub")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11.5)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    runs_meta = [
        ("Oscar David\n", True, 12),
        ("Facultad de Ingeniería\n", False, 11),
        ("Curso: Inteligencia Artificial y Machine Learning\n", False, 11),
        ("Trabajo Práctico: Modelos No Supervisados y Extracción de Patrones\n", False, 11),
        ("Docente Asesor: Tutor de Área\n", False, 11),
        ("Repositorio GitHub: https://github.com/oscar2121/ml-no-supervisado-clustering-pca\n", True, 10.5),
        ("Octubre de 2026", False, 11)
    ]
    for texto, negrita, tam in runs_meta:
        r = p_meta.add_run(texto)
        r.bold = negrita
        r.font.name = 'Times New Roman'
        r.font.size = Pt(tam)

    doc.add_page_break()

    # RESUMEN / ABSTRACT
    h1("Resumen")
    parrafo(
        "El presente informe documenta la investigación, desarrollo experimental y análisis comparativo de técnicas fundamentales "
        "de Aprendizaje Automático No Supervisado (Unsupervised Machine Learning), abordando dos pilares metodológicos: la reducción "
        "de dimensionalidad mediante Análisis de Componentes Principales (PCA) y Descomposición en Valores Singulares (SVD), y el "
        "agrupamiento de datos a través de K-Means y Clustering Jerárquico Aglomerativo. La experimentación se llevó a cabo sobre "
        "un conjunto de datos multidimensional compuesto por 178 observaciones y 13 atributos físico-químicos continuos correspondiente "
        "al dataset analítico de vinos (Wine Dataset) en el entorno Google Colaboratory. Se demostró la estricta necesidad del "
        "preprocesamiento mediante estandarización Z-score para evitar sesgos inducidos por disparidad de escalas. La técnica de PCA "
        "permitió sintetizar el 55.41% de la varianza en dos dimensiones y el 66.53% en tres dimensiones, verificándose su equivalencia "
        "exacta con SVD sobre datos centrados. Para el agrupamiento, el Método del Codo y el Coeficiente de Silueta identificaron k=3 "
        "como el número óptimo de conglomerados (silueta s = 0.2849), hallazgo ratificado de forma independiente por el corte horizontal "
        "del dendrograma de Ward a una altura h = 25.0. Finalmente, se ejecutó un perfilamiento físico-químico que tradujo los clusters "
        "algorítmicos en segmentos interpretables para el control de calidad y la industria vitivinícola.",
        sangria=False
    )
    p_pal = doc.add_paragraph()
    p_pal.paragraph_format.space_after = Pt(16)
    r_pk = p_pal.add_run("Palabras clave: ")
    r_pk.bold = True
    r_pk.font.italic = True
    r_pk.font.name = 'Times New Roman'
    r_pk.font.size = Pt(10.5)
    r_pv = p_pal.add_run("Machine Learning No Supervisado, Clustering, K-Means, Clustering Jerárquico, PCA, SVD, Google Colab, Scikit-Learn.")
    r_pv.font.italic = True
    r_pv.font.name = 'Times New Roman'
    r_pv.font.size = Pt(10.5)

    doc.add_page_break()

    # CONTENIDO PRINCIPAL
    h1("Implementación y Análisis Crítico de Algoritmos de Aprendizaje No Supervisado")

    h2("1. Fundamentos Conceptuales del Aprendizaje No Supervisado")
    parrafo(
        "En la ciencia de datos contemporánea, más del 80% de los datos generados a escala industrial carecen de etiquetas "
        "o anotaciones externas preexistentes (Bishop, 2006). A diferencia del aprendizaje supervisado —donde el modelo es guiado "
        "por una señal objetivo escalar o categórica y mediante la optimización de un error empírico—, el Aprendizaje Automático No "
        "Supervisado opera sobre una matriz de observaciones multivariadas X = {x_1, x_2, ..., x_N} en ℝ^D sin variable de respuesta. "
        "El objetivo no reside en la predicción cuantitativa directa, sino en develar la geometría intrínseca, la densidad de probabilidad "
        "subyacente p(x) y las agrupaciones latentes presentes en los datos (Hastie et al., 2009)."
    )
    parrafo(
        "Las técnicas no supervisadas cumplen funciones cruciales en el flujo de ingeniería de datos: permiten la exploración autónoma "
        "de grandes volúmenes de información, mitigan el ruido instrumental, condensan información redundante para optimizar modelos "
        "posteriores y posibilitan la segmentación de entidades en taxonomías naturales previamente desconocidas."
    )

    h3("1.1 Métodos de Reducción de Dimensionalidad: PCA y SVD")
    parrafo(
        "Cuando el número de variables descriptivas D es elevado, los algoritmos analíticos se enfrentan a la denominada 'Maldición de la "
        "Dimensionalidad' (Curse of Dimensionality), descrita originalmente por Richard Bellman. En espacios de alta dimensión, el volumen "
        "crece exponencialmente, los puntos muestrales se dispersan hacia la periferia del hiperespacio y las distancias euclidianas pierden "
        "su poder discriminativo, pues la distancia relativa entre el punto más cercano y el más lejano tiende a cero (Goodfellow et al., 2016). "
        "Para superar este obstáculo, se recurre a la reducción de dimensionalidad."
    )
    parrafo(
        "• Análisis de Componentes Principales (PCA): Es una técnica lineal no supervisada que proyecta los datos desde ℝ^D hacia un "
        "subespacio ortogonal ℝ^d (d << D) maximizando la varianza proyectada de las observaciones (Jolliffe & Cadima, 2016). Matemáticamente, "
        "los componentes principales corresponden a los autovectores (eigenvectors) de la matriz de covarianza muestral Σ = (1/(N-1)) X_c^T X_c, "
        "ordenados descendentemente según sus correspondientes autovalores (eigenvalues) λ_i, los cuales cuantifican la cantidad de varianza explicada."
    )
    parrafo(
        "• Descomposición en Valores Singulares (SVD): Es una factorización fundamental de álgebra lineal que descompone cualquier matriz "
        "real X en el producto de tres matrices: X = U Σ V^T, donde U es una matriz ortogonal N×N de vectores singulares izquierdos, Σ es "
        "una matriz diagonal N×D con los valores singulares ordenados σ_1 ≥ σ_2 ≥ ... ≥ 0, y V^T es la transpuesta de una matriz ortogonal D×D "
        "de vectores singulares derechos (Strang, 2016). De acuerdo con el Teorema de Eckart-Young-Mirsky, truncar esta descomposición a los "
        "primeros d valores singulares proporciona la mejor aproximación de rango d a la matriz original en términos de la norma de Frobenius. "
        "Cuando la matriz de datos ha sido previamente centrada con media cero, SVD y PCA son matemáticamente idénticos, con la ventaja de que "
        "SVD (en su variante TruncatedSVD) no requiere calcular explícitamente la matriz densa de covarianza, posibilitando su ejecución en matrices dispersas."
    )

    h3("1.2 Algoritmos de Agrupamiento (Clustering): K-Means y Jerárquico")
    parrafo(
        "El agrupamiento consiste en organizar un conjunto de datos no etiquetado en subconjuntos mutuamente excluyentes (clusters) de "
        "modo que la similitud intra-cluster (cohesión interna) sea máxima y la similitud inter-cluster (separación entre grupos) sea mínima (Jain, 2010)."
    )
    parrafo(
        "• Algoritmo K-Means: Método particional basado en centroides propuesto por Lloyd y MacQueen. Dado un número predefinido de k grupos, "
        "K-Means busca minimizar la función de costo de suma de errores al cuadrado dentro del cluster (WCSS o Inercia): "
        "J = ∑_{i=1}^k ∑_{x ∈ C_i} ||x - μ_i||^2, donde μ_i representa el centroide (media aritmética) del cluster C_i. El algoritmo itera "
        "dos fases hasta converger: (1) asignación de cada punto al centroide más próximo mediante distancia euclidiana, y (2) actualización "
        "del centroide como el baricentro de los puntos asignados. Si bien exhibe una eficiencia computacional sobresaliente lineal respecto "
        "al número de datos O(N·k·I), presenta como limitaciones requerir el hiperparámetro k a priori y suponer que los clusters poseen "
        "geometría esférica e isotrópica."
    )
    parrafo(
        "• Clustering Jerárquico Aglomerativo: Paradigma ascendente (bottom-up) que no requiere definir a priori el número de clusters. "
        "Inicia considerando cada punto como un cluster atómico y, de forma iterativa, fusiona los pares de clusters más próximos según una "
        "métrica de enlace hasta integrar todas las observaciones en una raíz común. Entre los métodos de enlace destaca el Criterio de Ward, "
        "el cual evalúa en cada paso qué fusión genera el mínimo incremento en la inercia total intra-cluster. El proceso se visualiza mediante "
        "un Dendrograma, cuya estructura en árbol permite a los científicos inspeccionar visualmente a qué altura cortar el gráfico para "
        "determinar la granularidad de partición óptima."
    )

    h3("1.3 Criterios de Evaluación y Validación No Supervisada")
    parrafo(
        "Ante la ausencia de una clase de referencia supervisada, la evaluación de los agrupamientos debe fundarse en métricas de validación interna:"
    )
    parrafo(
        "1. Método del Codo (Elbow Method): Grafica la inercia WCSS en función de k. Se selecciona el valor de k donde la curva experimenta "
        "un cambio drástico en su tasa de descenso (punto de inflexión), indicando que añadir más grupos solo produce ganancias marginales."
    )
    parrafo(
        "2. Coeficiente de Silueta (Silhouette Score): Mide cuán similar es un objeto a su propio cluster en comparación con los demás. Para cada muestra i: "
        "s(i) = (b(i) - a(i)) / max(a(i), b(i)), donde a(i) es la distancia media a los puntos del mismo cluster y b(i) es la distancia media mínima "
        "a los puntos de cualquier otro cluster vecino (Rousseeuw, 1987). Su valor fluctúa en [-1, 1], donde valores cercanos a 1 indican que el "
        "punto está perfectamente agrupado."
    )
    parrafo(
        "3. Índices de Davies-Bouldin y Calinski-Harabasz: Davies-Bouldin mide la similitud promedio entre cada cluster y su vecino más similar "
        "(valores más bajos indican mejor separación), mientras que Calinski-Harabasz calcula la razón entre la dispersión inter-cluster y la dispersión "
        "intra-cluster (valores más altos indican mayor densidad y distancia entre grupos)."
    )

    doc.add_page_break()

    # METODOLOGÍA Y CASO DE ESTUDIO
    h2("2. Metodología y Caso de Estudio Práctico")
    parrafo(
        "Para responder a las directrices de aplicación práctica, los experimentos se diseñaron y ejecutaron en el entorno Google Colaboratory, "
        "empleando el ecosistema de computación científica Scikit-Learn, SciPy, NumPy, Pandas, Matplotlib y Seaborn. Como caso de estudio "
        "se seleccionó el prestigioso dataset analítico vitivinícola (Wine Dataset), compuesto por 178 muestras derivadas de tres variedades "
        "de uva cultivadas en la misma región de Italia pero con marcada variabilidad físico-química."
    )
    parrafo(
        "El dataset contiene 13 atributos cuantitativos continuos: grado de alcohol, ácido málico, cenizas, alcalinidad de las cenizas, "
        "magnesio, fenoles totales, flavanoides, fenoles no flavanoides, proantocianidinas, intensidad del color, tono, absorción OD280/OD315 "
        "de vinos diluidos y concentración de prolina."
    )

    h3("2.1 Análisis Exploratorio y la Estricta Necesidad de Estandarización")
    parrafo(
        "La inspección estadística inicial reveló que variables como la 'prolina' exhiben una media de 746.89 mg/L y una varianza superior a "
        "99,000, mientras que los 'fenoles no flavanoides' se ubican en el rango de 0.13 a 0.66 con varianza de 0.015. "
        "En presencia de distancias euclidianas d(x, y) = √(∑ (x_j - y_j)^2), la variable prolina dominaría el 99.9% de la distancia total, "
        "anulando la contribución de los restantes 12 atributos. Por consiguiente, se aplicó un preprocesamiento riguroso mediante StandardScaler, "
        "transformando cada característica a media μ = 0 y desviación típica σ = 1."
    )

    agregar_imagen(
        "fig1_correlation.png",
        "Figura 1. Matriz de Correlación de Pearson entre Variables Físico-Químicas.",
        "Coeficientes de correlación calculados sobre las 13 variables estandarizadas. Destaca la colinealidad positiva entre flavanoides y fenoles totales (r = 0.86) e inversa entre flavanoides y alcalinidad de cenizas (r = -0.56)."
    )

    parrafo(
        "La Figura 1 pone de manifiesto que el espacio original contiene una marcada redundancia lineal entre componentes fenólicos y dilución "
        "(r > 0.8), ratificando la idoneidad teórica de aplicar reducción de dimensionalidad para eliminar colinealidad sin perder varianza."
    )

    doc.add_page_break()

    # IMPLEMENTACIÓN TÉCNICA Y RESULTADOS
    h2("3. Implementación Técnica y Resultados Experimentales")

    h3("3.1 Reducción de Dimensionalidad: PCA y SVD")
    parrafo(
        "Se aplicó el Análisis de Componentes Principales sobre la matriz estandarizada X_scaled ∈ ℝ^{178×13}. La distribución de autovalores y el "
        "análisis de sedimentación permitieron determinar la estructura latente del espacio muestral."
    )

    agregar_imagen(
        "fig2_pca_scree.png",
        "Figura 2. Gráfico de Sedimentación (Scree Plot) y Varianza Acumulada.",
        "Distribución del porcentaje de varianza explicada por cada componente principal individual y curva acumulativa. Los primeros dos componentes concentran el 55.41% de la varianza total."
    )

    parrafo(
        "Tal como ilustra la Figura 2, el primer componente (PC1) retiene el 36.20% de la variabilidad total, y el segundo (PC2) aporta un 19.21%. "
        "Proyectando el conjunto de datos sobre un plano bidimensional se preserva el 55.41% de la información original, superando el 66.5% si se añade "
        "un tercer componente. El quiebre del Scree Plot confirma que el subespacio intrínseco fundamental se estabiliza a partir de d = 2 a 3 dimensiones."
    )

    agregar_imagen(
        "fig3_pca_loadings.png",
        "Figura 3. Cargas Factoriales (Loadings) de las Características en PC1 y PC2.",
        "Pesos de los autovectores directores. PC1 sintetiza calidad fenólica y dilución (pesos positivos en flavanoides y fenoles totales); PC2 captura alcohol e intensidad cromática."
    )

    parrafo(
        "La Figura 3 descompone los autovectores directores (loadings). El eje PC1 se asocia fundamentalmente a la concentración fenólica y antioxidante, "
        "mientras que PC2 discrimina a las muestras en función de su graduación alcohólica y profundidad de color."
    )

    agregar_imagen(
        "fig4_pca_vs_svd.png",
        "Figura 4. Comparación Geométrica entre Proyecciones PCA y SVD.",
        "Proyecciones bidimensionales obtenidas con PCA y TruncatedSVD sobre datos centrados. La correlación cruzada absoluta calculada entre los ejes homólogos fue de |r| = 1.000000."
    )

    parrafo(
        "La Figura 4 valida empíricamente la deducción matemática de la sección 1.1: las nubes de puntos generadas por PCA y TruncatedSVD son "
        "idénticas en términos de dispersión relativa y morfología topológica, confirmando una correlación de Pearson unitaria (|r| = 1.000)."
    )

    doc.add_page_break()

    h3("3.2 Algoritmos de Clustering: K-Means y Selección de k Óptimo")
    parrafo(
        "Para aplicar K-Means de forma cuantitativamente justificada, se evaluó un barrido de hiperparámetros k ∈ [2, 8] calculando simultáneamente "
        "la inercia residual (WCSS) y el coeficiente de silueta promedio."
    )

    agregar_imagen(
        "fig5_elbow_silhouette.png",
        "Figura 5. Búsqueda de k Óptimo: Método del Codo vs Coeficiente de Silueta.",
        "Evolución de la suma de cuadrados intra-cluster (azul) y el Silhouette Score promedio (verde). El valor k = 3 constituye el codo evidente y el máximo global de silueta (s = 0.2849)."
    )

    parrafo(
        "Los resultados de la Figura 5 son concluyentes: la inercia WCSS muestra un codo prominente en k = 3, y simultáneamente el Coeficiente "
        "de Silueta alcanza su pico máximo global en s = 0.2849. Aumentar k a 4 o más provoca una caída monótona en la silueta debido a sobrepartición."
    )

    agregar_imagen(
        "fig6_kmeans_pca.png",
        "Figura 6. Partición de K-Means (k = 3) y Centroides en el Subespacio PCA.",
        "Distribución de los tres grupos descubiertos por K-Means representados en el plano bidimensional PC1-PC2. Las estrellas amarillas indican la proyección de los centroides calculados en ℝ^13."
    )

    parrafo(
        "La proyección en la Figura 6 demuestra que los tres conglomerados asignados por K-Means ocupan regiones convexas y compactas, con una "
        "separación clara a lo largo del eje PC1 (diferenciando el Cluster 1 del Cluster 2) y el eje PC2 (separando el Cluster 0)."
    )

    doc.add_page_break()

    h3("3.3 Clustering Jerárquico Aglomerativo y Dendrograma")
    parrafo(
        "Se procedió al entrenamiento del modelo jerárquico empleando distancia euclidiana y el criterio de enlace de Ward."
    )

    agregar_imagen(
        "fig7_dendrogram.png",
        "Figura 7. Dendrograma de Clustering Jerárquico con Enlace de Ward.",
        "Estructura jerárquica de fusiones sucesivas. Una línea de corte horizontal a una distancia h = 25.0 segmenta el árbol exactamente en tres ramas principales."
    )

    parrafo(
        "En la Figura 7, la altura vertical representa la distancia de disimilitud entre sub-clusters. Los tres grandes troncos verticales antes del "
        "corte horizontal confirman, con un enfoque metodológico completamente distinto a K-Means, que la topología intrínseca de los datos alberga tres macro-grupos."
    )

    agregar_imagen(
        "fig8_kmeans_vs_hierarchical.png",
        "Figura 8. Comparación de Agrupamientos: K-Means vs Clustering Jerárquico.",
        "Contraste de las etiquetas asignadas en el subespacio proyectado. Se aprecia una concordancia geométrica sobresaliente en las fronteras de separación."
    )

    # TABLA DE MÉTRICAS COMPARATIVAS
    p_tb_tit = doc.add_paragraph()
    p_tb_tit.paragraph_format.space_before = Pt(8)
    p_tb_tit.paragraph_format.space_after = Pt(4)
    r_tbn = p_tb_tit.add_run("Tabla 1.\n")
    r_tbn.bold = True
    r_tbn.font.name = 'Times New Roman'
    r_tbn.font.size = Pt(10)
    r_tbd = p_tb_tit.add_run("Evaluación Comparativa de Métricas Intrínsecas de Validación de Clusters")
    r_tbd.font.italic = True
    r_tbd.font.name = 'Times New Roman'
    r_tbd.font.size = Pt(10)

    table = doc.add_table(rows=3, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    encabezados = ["Algoritmo (k = 3)", "Silhouette Score ↑", "Davies-Bouldin ↓", "Calinski-Harabasz ↑"]
    datos_fila = [
        ["K-Means (k = 3)", "0.2849", "1.3892", "70.94"],
        ["Jerárquico Ward (k = 3)", "0.2774", "1.4187", "67.07"]
    ]

    for col_idx, enc in enumerate(encabezados):
        cell = table.cell(0, col_idx)
        cell.paragraphs[0].text = enc
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row_idx, fila in enumerate(datos_fila):
        for col_idx, val in enumerate(fila):
            cell = table.cell(row_idx + 1, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_nt = doc.add_paragraph()
    p_nt.paragraph_format.space_after = Pt(12)
    r_nt = p_nt.add_run("Nota. ")
    r_nt.font.italic = True
    r_nt.font.size = Pt(8.5)
    p_nt.add_run("Métricas calculadas sobre el espacio estandarizado de 13 dimensiones. Las flechas indican el sentido deseable de optimización.").font.size = Pt(8.5)

    doc.add_page_break()

    # ANÁLISIS CRÍTICO Y PERFILAMIENTO
    h2("4. Análisis Crítico y Discusión de Resultados")
    parrafo(
        "Más allá de la validación matemática, la utilidad primordial del aprendizaje no supervisado radica en dotar de sentido práctico "
        "a los conglomerados descubiertos. Para ello, se desestandarizaron las observaciones proyectándolas a sus unidades físicas originales "
        "y se calculó el perfil medio para los atributos químicos de mayor relevancia discriminante."
    )

    agregar_imagen(
        "fig9_cluster_profiles.png",
        "Figura 9. Distribución de Variables Químicas Clave en los Conglomerados Descubiertos.",
        "Diagramas de cajas para graduación alcohólica, flavanoides, fenoles totales, intensidad cromática y prolina. Cada cluster muestra un perfil claramente diferenciado."
    )

    parrafo(
        "• Cluster 0 (Vinos Ligeros y Jóvenes): Caracterizados por un tenor alcohólico moderado (12.25%), intensidad colorimétrica baja (3.05), "
        "niveles medios de flavanoides (2.05 mg/L) y baja prolina (519.5 mg/L). Corresponden a perfiles de consumo cotidiano, jóvenes y de menor cuerpo."
    )
    parrafo(
        "• Cluster 1 (Vinos de Alta Gama y Crianza Prolongada): Exhiben una concentración fenólica sobresaliente (fenoles totales 2.84 mg/L, "
        "flavanoides 2.98 mg/L), elevada graduación alcohólica (13.68%) y un contenido récord de prolina (1115.7 mg/L). Este perfil denota vinos "
        "con gran capacidad antioxidante, cuerpo estructurado y aptitud para envejecimiento en barrica."
    )
    parrafo(
        "• Cluster 2 (Vinos Concentrados y Astringentes): Destacan por la mayor intensidad colorimétrica (7.40) pero con una severa deficiencia "
        "de flavanoides (0.78 mg/L) y alto ácido málico. Representan muestras con pigmentación intensa pero con perfil más rústico y taninos ásperos."
    )

    h3("4.1 Ventajas y Limitaciones Comparadas de los Métodos")
    parrafo(
        "La contrastación experimental entre ambos enfoques arroja conclusiones operativas claras: K-Means es ideal para despliegues masivos en "
        "producción debido a su complejidad temporal lineal O(N·k·I), pero sufre ante geometrías irregulares. En contraste, el Clustering Jerárquico "
        "ofrece una riqueza diagnóstica inigualable mediante el dendrograma, prescinde de fijar k a priori y admite matrices de disimilitud "
        "arbitrarias, aunque su costo computacional O(N² log N) lo vuelve impráctico para datasets con cientos de miles de registros."
    )

    doc.add_page_break()

    # REPOSITORIO Y REPLICABILIDAD
    h2("5. Repositorio en GitHub y Replicabilidad en Google Colab")
    parrafo(
        "En estricto cumplimiento de las condiciones de entrega, todo el código fuente, los notebooks interactivos y los recursos gráficos "
        "han sido versionados y puestos a disposición pública en GitHub."
    )
    parrafo(
        "• Enlace Oficial al Repositorio: https://github.com/oscar2121/ml-no-supervisado-clustering-pca\n"
        "• Archivo del Notebook Principal: notebooks/Machine_Learning_No_Supervisado_Clustering_PCA_SVD.ipynb\n"
        "• Ejecución Inmediata en Google Colab: El repositorio incluye un botón interactivo 'Open In Colab' en su archivo README.md, "
        "permitiendo a cualquier evaluador reproducir el 100% de los experimentos, gráficas y métricas sin requerir descargas ni dependencias locales."
    )

    h2("6. Conclusiones Generales")
    parrafo(
        "1. Demostración de Eficacia No Supervisada: Se constató que, prescindiendo totalmente de etiquetas de clase durante la fase de ajuste, "
        "las técnicas de Clustering (K-Means y Jerárquico) y Reducción de Dimensionalidad (PCA y SVD) recuperaron con extraordinaria precisión "
        "la estructura biológica y físico-química latente de las muestras analizadas."
    )
    parrafo(
        "2. Interdependencia del Pipeline: La estandarización de características resultó ser un requisito matemático indispensable para evitar "
        "el sesgo provocado por variables de gran magnitud escalar como la prolina sobre las distancias euclidianas."
    )
    parrafo(
        "3. Convergencia Metodológica: La determinación de k = 3 quedó demostrada tanto por criterios cuantitativos de partición (Elbow y Silhouette) "
        "como por la topología de ramificación del Dendrograma de Ward, reflejando una perfecta sincronía entre métodos algorítmicos independientes."
    )
    parrafo(
        "4. Aporte Práctico y Profesional: La combinación de reducción dimensional y clustering no supervisado constituye una metodología "
        "imprescindible en la industria moderna para la segmentación de clientes, control de calidad analítico, compresión de imágenes y "
        "descubrimiento de patrones biomédicos."
    )

    doc.add_page_break()

    # REFERENCIAS BIBLIOGRÁFICAS APA 7
    h1("Referencias Bibliográficas")
    
    referencias = [
        "Bishop, C. M. (2006). Pattern recognition and machine learning. Springer Science & Business Media.",
        "Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. In Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96) (pp. 226-231). AAAI Press.",
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning. MIT Press. http://www.deeplearningbook.org",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The elements of statistical learning: Data mining, inference, and prediction (2nd ed.). Springer New York. https://doi.org/10.1007/978-0-387-84858-7",
        "Jain, A. K. (2010). Data clustering: 50 years beyond K-means. Pattern Recognition Letters, 31(8), 651-666. https://doi.org/10.1016/j.patrec.2009.09.011",
        "Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: A review and recent developments. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 374(2065), 20150202. https://doi.org/10.1098/rsta.2015.0202",
        "Lloyd, S. (1982). Least squares quantization in PCM. IEEE Transactions on Information Theory, 28(2), 129-137. https://doi.org/10.1109/TIT.1982.1056489",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53-65. https://doi.org/10.1016/0377-0427(87)90125-7",
        "Strang, G. (2016). Introduction to linear algebra (5th ed.). Wellesley-Cambridge Press.",
        "Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. Journal of the American Statistical Association, 58(301), 236-244. https://doi.org/10.1080/01621459.1963.10500845"
    ]

    for ref in referencias:
        referencia_apa(ref)

    doc.save(DOCX_OUT)
    print(f"[OK] Documento DOCX creado exitosamente en: {DOCX_OUT}")

# =============================================================================
# 2. GENERACIÓN DEL DOCUMENTO EN FORMATO PDF PROFESIONAL CON REPORTLAB
# =============================================================================
class APANumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#333333"))
        # Número de página en la esquina superior derecha según normas APA
        self.drawRightString(540, 750, f"{self._pageNumber}")
        
        # En páginas de contenido, encabezado sutil
        if self._pageNumber > 1:
            self.drawString(72, 750, "INFORME TÉCNICO: MACHINE LEARNING NO SUPERVISADO (CLUSTERING Y PCA)")
            self.setStrokeColor(colors.HexColor("#D0D0D0"))
            self.setLineWidth(0.5)
            self.line(72, 742, 540, 742)
            
        self.restoreState()

def construir_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT,
        pagesize=letter,
        leftMargin=72, rightMargin=72,
        topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'APATitle', fontName='Times-Bold', fontSize=15, leading=20,
        alignment=1, spaceAfter=14
    )
    sub_style = ParagraphStyle(
        'APASubtitle', fontName='Times-Roman', fontSize=11.5, leading=16,
        alignment=1, spaceAfter=25
    )
    meta_style = ParagraphStyle(
        'APAMeta', fontName='Times-Roman', fontSize=10.5, leading=15,
        alignment=1, spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'APAH1', fontName='Times-Bold', fontSize=13, leading=17,
        alignment=1, spaceBefore=16, spaceAfter=10, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'APAH2', fontName='Times-Bold', fontSize=11.5, leading=15,
        alignment=0, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'APAH3', fontName='Times-BoldItalic', fontSize=10.5, leading=14,
        alignment=0, spaceBefore=9, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'APABody', fontName='Times-Roman', fontSize=10, leading=14,
        alignment=4, firstLineIndent=24, spaceAfter=6
    )
    body_no_indent = ParagraphStyle(
        'APABodyNoIndent', fontName='Times-Roman', fontSize=10, leading=14,
        alignment=4, spaceAfter=6
    )
    fig_title_style = ParagraphStyle(
        'APAFigTitle', fontName='Times-Bold', fontSize=9.5, leading=13,
        alignment=0, spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    fig_note_style = ParagraphStyle(
        'APAFigNote', fontName='Times-Italic', fontSize=8.5, leading=12,
        alignment=4, spaceBefore=2, spaceAfter=8
    )
    ref_style = ParagraphStyle(
        'APARef', fontName='Times-Roman', fontSize=9, leading=13,
        alignment=4, leftIndent=24, firstLineIndent=-24, spaceAfter=6
    )

    story = []

    # PORTADA
    story.append(Spacer(1, 40))
    story.append(Paragraph("Implementación y Análisis Crítico de Algoritmos de Aprendizaje No Supervisado: Reducción de Dimensionalidad (PCA, SVD) y Modelos de Clustering (K-Means, Jerárquico)", title_style))
    story.append(Paragraph("Informe Académico Desarrollado en Google Colaboratory y Repositorio en GitHub", sub_style))
    story.append(Spacer(1, 20))
    
    meta_text = """
    <b>Oscar David</b><br/><br/>
    Facultad de Ingeniería<br/>
    Curso: Inteligencia Artificial y Machine Learning<br/>
    Experiencia Práctica: Técnicas de Agrupamiento y Reducción Dimensional<br/>
    Docente Asesor: Tutor de Área<br/><br/>
    <b>Repositorio GitHub:</b> https://github.com/oscar2121/ml-no-supervisado-clustering-pca<br/><br/>
    Octubre de 2026
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(PageBreak())

    # RESUMEN
    story.append(Paragraph("Resumen", h1_style))
    resumen_text = (
        "El presente informe documenta el desarrollo conceptual, la implementación algorítmica y el análisis crítico de técnicas "
        "fundamentales de Aprendizaje Automático No Supervisado en Google Colaboratory. Se implementaron algoritmos de reducción de "
        "dimensionalidad (PCA y SVD) y técnicas de agrupamiento (K-Means y Clustering Jerárquico Aglomerativo) sobre el dataset "
        "multidimensional de vinos de Scikit-Learn (178 muestras y 13 variables físico-químicas continuas). La investigación comprobó la "
        "estricta necesidad de estandarizar las variables numéricas (Z-score) para mitigar la distorsión geométrica en las distancias "
        "euclidianas. El Análisis de Componentes Principales logró condensar el 55.41% de la varianza en dos dimensiones y el 66.53% en tres, "
        "demostrándose su estricta equivalencia matemática con TruncatedSVD (|r| = 1.000). Para el clustering, el Método del Codo y el "
        "Coeficiente de Silueta identificaron de manera consistente k=3 como la configuración óptima (s = 0.2849), resultado respaldado "
        "por el dendrograma de Ward. Finalmente, se realizó una caracterización físico-química de cada cluster descubierto."
    )
    story.append(Paragraph(resumen_text, body_no_indent))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i><b>Palabras clave:</b> Machine Learning No Supervisado, Clustering, K-Means, Clustering Jerárquico, PCA, SVD, Google Colab.</i>", body_no_indent))
    story.append(PageBreak())

    # SECCIÓN 1: FUNDAMENTOS
    story.append(Paragraph("Implementación y Análisis Crítico de Algoritmos No Supervisados", h1_style))
    story.append(Paragraph("1. Fundamentos Conceptuales del Aprendizaje No Supervisado", h2_style))
    story.append(Paragraph(
        "En los sistemas modernos de información, la gran mayoría de los datos disponibles carecen de anotaciones previas debido a los "
        "elevados costos humanos y logísticos del etiquetado. En este contexto, el Aprendizaje No Supervisado permite analizar matrices "
        "de observaciones multivariadas X ∈ ℝ^{N×D} para descubrir patrones ocultos, agrupaciones naturales y regularidades geométricas "
        "sin requerir una función de pérdida supervisada externa (Bishop, 2006; Hastie et al., 2009).",
        body_style
    ))
    story.append(Paragraph("1.1 Técnicas de Reducción de Dimensionalidad (PCA y SVD)", h3_style))
    story.append(Paragraph(
        "El fenómeno conocido como 'la maldición de la dimensionalidad' provoca que, al aumentar el número de variables descriptivas D, "
        "el volumen del hiperespacio crezca exponencialmente y los puntos se tornen extremadamente dispersos, degradando el cálculo de distancias. "
        "El Análisis de Componentes Principales (PCA) proyecta el conjunto de datos hacia un subespacio ortogonal maximizando la varianza proyectada, "
        "calculando los autovectores y autovalores de la matriz de covarianza (Jolliffe & Cadima, 2016). Por su parte, la Descomposición en Valores "
        "Singulares (SVD) factoriza X = U Σ V^T, garantizando por el teorema de Eckart-Young-Mirsky la aproximación óptima de bajo rango. "
        "Sobre datos centrados con media cero, ambas formulaciones son matemáticamente equivalentes.",
        body_style
    ))
    story.append(Paragraph("1.2 Algoritmos de Clustering (K-Means y Jerárquico Aglomerativo)", h3_style))
    story.append(Paragraph(
        "El clustering busca particionar los datos en subgrupos que exhiban alta cohesión interna y máxima separación externa (Jain, 2010). "
        "K-Means optimiza iterativamente la suma de cuadrados intra-cluster (WCSS o Inercia) asignando puntos al centroide más cercano. "
        "El Clustering Jerárquico Aglomerativo sigue una estrategia ascendente, fusionando en cada iteración los conglomerados más próximos según "
        "un criterio de enlace. El método de Ward minimiza el incremento en la varianza total intra-cluster, permitiendo inspeccionar la estructura "
        "global mediante un Dendrograma.",
        body_style
    ))

    # SECCIÓN 2: METODOLOGÍA
    story.append(Paragraph("2. Metodología y Caso de Estudio Práctico", h2_style))
    story.append(Paragraph(
        "La experimentación se diseñó en Google Colaboratory empleando Scikit-Learn y SciPy sobre el dataset de vinos (178 muestras, 13 variables "
        "físico-químicas continuas). Para garantizar que variables de gran magnitud escalar (como la prolina con valores superiores a 1,000 mg/L) "
        "no anularan a variables de baja escala (como los fenoles no flavanoides), se aplicó estandarización Z-score: z = (x - μ) / σ.",
        body_style
    ))

    # Figura 1
    f1 = os.path.join(FIG_DIR, "fig1_correlation.png")
    if os.path.exists(f1):
        story.append(Paragraph("<b>Figura 1.</b> <i>Matriz de Correlación de Pearson entre Variables Físico-Químicas.</i>", fig_title_style))
        story.append(RLImage(f1, width=420, height=310))
        story.append(Paragraph("<i>Nota.</i> Coeficientes de correlación calculados sobre las 13 variables estandarizadas. Se confirma alta redundancia entre flavanoides y fenoles totales (r = 0.86).", fig_note_style))

    story.append(PageBreak())

    # SECCIÓN 3: RESULTADOS
    story.append(Paragraph("3. Implementación Técnica y Resultados Experimentales", h2_style))
    story.append(Paragraph("3.1 Reducción de Dimensionalidad (PCA y SVD)", h3_style))
    story.append(Paragraph(
        "La reducción por PCA evidenció que el componente PC1 explica el 36.20% de la varianza total y PC2 el 19.21%, acumulando un 55.41% en 2D "
        "y 66.53% en 3D.",
        body_style
    ))

    # Figura 2
    f2 = os.path.join(FIG_DIR, "fig2_pca_scree.png")
    if os.path.exists(f2):
        story.append(Paragraph("<b>Figura 2.</b> <i>Gráfico de Sedimentación (Scree Plot) y Varianza Acumulada.</i>", fig_title_style))
        story.append(RLImage(f2, width=440, height=230))
        story.append(Paragraph("<i>Nota.</i> Varianza individual por componente (barras) y acumulada (línea roja). Los primeros dos componentes retienen más de la mitad de la información.", fig_note_style))

    # Figura 3
    f3 = os.path.join(FIG_DIR, "fig3_pca_loadings.png")
    if os.path.exists(f3):
        story.append(Paragraph("<b>Figura 3.</b> <i>Cargas Factoriales (Loadings) en PC1 y PC2.</i>", fig_title_style))
        story.append(RLImage(f3, width=440, height=220))
        story.append(Paragraph("<i>Nota.</i> PC1 representa el eje de contenido fenólico y dilución; PC2 discrimina por intensidad de color y alcohol.", fig_note_style))

    story.append(PageBreak())

    # Figura 4
    f4 = os.path.join(FIG_DIR, "fig4_pca_vs_svd.png")
    if os.path.exists(f4):
        story.append(Paragraph("<b>Figura 4.</b> <i>Comparación Geométrica entre Proyecciones PCA y SVD.</i>", fig_title_style))
        story.append(RLImage(f4, width=440, height=185))
        story.append(Paragraph("<i>Nota.</i> Proyecciones bidimensionales idénticas con correlación de Pearson cruzada unitaria (|r| = 1.000).", fig_note_style))

    story.append(Paragraph("3.2 Clustering con K-Means y Selección de k Óptimo", h3_style))
    story.append(Paragraph(
        "Se evaluó el rango k ∈ [2, 8]. La curva de WCSS (Método del Codo) y el Coeficiente de Silueta señalaron a k = 3 como la solución óptima (s = 0.2849).",
        body_style
    ))

    # Figura 5
    f5 = os.path.join(FIG_DIR, "fig5_elbow_silhouette.png")
    if os.path.exists(f5):
        story.append(Paragraph("<b>Figura 5.</b> <i>Método del Codo vs Coeficiente de Silueta.</i>", fig_title_style))
        story.append(RLImage(f5, width=440, height=220))
        story.append(Paragraph("<i>Nota.</i> El codo de inercia y el máximo de silueta coinciden con precisión en k = 3.", fig_note_style))

    # Figura 6
    f6 = os.path.join(FIG_DIR, "fig6_kmeans_pca.png")
    if os.path.exists(f6):
        story.append(Paragraph("<b>Figura 6.</b> <i>Partición K-Means (k = 3) y Centroides Proyectados en PC1 y PC2.</i>", fig_title_style))
        story.append(RLImage(f6, width=440, height=230))
        story.append(Paragraph("<i>Nota.</i> Los clusters descubiertos ocupan regiones compactas bien delimitadas con sus centroides correspondientes.", fig_note_style))

    story.append(PageBreak())

    story.append(Paragraph("3.3 Clustering Jerárquico Aglomerativo y Comparativa", h3_style))
    story.append(Paragraph(
        "El dendrograma de Ward reveló tres macro-ramas a una distancia de corte h = 25.0, confirmando la estructura de tres grupos.",
        body_style
    ))

    # Figura 7
    f7 = os.path.join(FIG_DIR, "fig7_dendrogram.png")
    if os.path.exists(f7):
        story.append(Paragraph("<b>Figura 7.</b> <i>Dendrograma de Clustering Jerárquico (Ward).</i>", fig_title_style))
        story.append(RLImage(f7, width=440, height=210))
        story.append(Paragraph("<i>Nota.</i> Las tres ramas principales quedan cortadas por la línea horizontal a h = 25.0.", fig_note_style))

    # Figura 8
    f8 = os.path.join(FIG_DIR, "fig8_kmeans_vs_hierarchical.png")
    if os.path.exists(f8):
        story.append(Paragraph("<b>Figura 8.</b> <i>Comparación de Particiones: K-Means vs Clustering Jerárquico.</i>", fig_title_style))
        story.append(RLImage(f8, width=440, height=185))
        story.append(Paragraph("<i>Nota.</i> Alta coincidencia en las fronteras de decisión descubiertas por ambos algoritmos.", fig_note_style))

    # TABLA COMPARATIVA
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Tabla 1.</b> <i>Evaluación Comparativa de Métricas Intrínsecas de Calidad de Clusters.</i>", fig_title_style))
    tabla_data = [
        ["Algoritmo (k = 3)", "Silhouette Score ↑", "Davies-Bouldin ↓", "Calinski-Harabasz ↑"],
        ["K-Means (k = 3)", "0.2849", "1.3892", "70.94"],
        ["Jerárquico Ward (k = 3)", "0.2774", "1.4187", "67.07"]
    ]
    t = Table(tabla_data, colWidths=[150, 100, 100, 110])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Paragraph("<i>Nota.</i> Métricas computadas en ℝ^13. Las flechas representan el sentido óptimo de cada índice.", fig_note_style))

    story.append(PageBreak())

    # SECCIÓN 4: ANÁLISIS CRÍTICO Y PERFILAMIENTO
    story.append(Paragraph("4. Análisis Crítico y Perfilamiento de Conglomerados", h2_style))
    story.append(Paragraph(
        "Al proyectar las agrupaciones hacia los valores físicos originales desestandarizados, se logró caracterizar perfiles específicos de producción:",
        body_style
    ))

    # Figura 9
    f9 = os.path.join(FIG_DIR, "fig9_cluster_profiles.png")
    if os.path.exists(f9):
        story.append(Paragraph("<b>Figura 9.</b> <i>Distribución de Variables Físico-Químicas Clave por Conglomerado.</i>", fig_title_style))
        story.append(RLImage(f9, width=450, height=150))
        story.append(Paragraph("<i>Nota.</i> Perfiles físico-químicos desestandarizados que sustentan la interpretación agronómica y de calidad.", fig_note_style))

    story.append(Paragraph(
        "• <b>Cluster 0:</b> Vinos jóvenes y ligeros (alcohol medio 12.25%, baja intensidad de color 3.05, prolina moderada 519.5 mg/L).<br/>"
        "• <b>Cluster 1:</b> Vinos de gama alta y crianza prolongada (alcohol 13.68%, flavanoides altos 2.98 mg/L, prolina sobresaliente 1115.7 mg/L).<br/>"
        "• <b>Cluster 2:</b> Vinos de alta concentración y taninos astringentes (intensidad de color 7.40, flavanoides deficientes 0.78 mg/L).",
        body_no_indent
    ))

    # SECCIONES FINALES
    story.append(Paragraph("5. Repositorio en GitHub y Replicabilidad en Google Colab", h2_style))
    story.append(Paragraph(
        "El código completo, el notebook interactivo y los recursos gráficos se encuentran versionados en el repositorio de GitHub:<br/>"
        "<b>URL del Repositorio:</b> https://github.com/oscar2121/ml-no-supervisado-clustering-pca<br/>"
        "El repositorio cuenta con el badge 'Open In Colab' para su ejecución inmediata y replicable en la nube.",
        body_no_indent
    ))

    story.append(Paragraph("6. Conclusiones Generales", h2_style))
    story.append(Paragraph(
        "1. Los algoritmos no supervisados clasificaron con precisión las variedades químicas sin contar con etiquetas previas.<br/>"
        "2. Se comprobó que la estandarización previa es indispensable para el correcto funcionamiento de distancias euclidianas.<br/>"
        "3. PCA y SVD mostraron equivalencia matemática exacta, comprimiendo el 55.4% de la varianza en 2 componentes.<br/>"
        "4. El método del codo, el análisis de silueta y el dendrograma de Ward convergieron armónicamente en k = 3.",
        body_no_indent
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Referencias Bibliográficas", h1_style))
    referencias = [
        "Bishop, C. M. (2006). <i>Pattern recognition and machine learning</i>. Springer Science & Business Media.",
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). <i>Deep learning</i>. MIT Press. http://www.deeplearningbook.org",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). <i>The elements of statistical learning: Data mining, inference, and prediction</i> (2nd ed.). Springer New York. https://doi.org/10.1007/978-0-387-84858-7",
        "Jain, A. K. (2010). Data clustering: 50 years beyond K-means. <i>Pattern Recognition Letters</i>, 31(8), 651-666. https://doi.org/10.1016/j.patrec.2009.09.011",
        "Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: A review and recent developments. <i>Philosophical Transactions of the Royal Society A</i>, 374(2065), 20150202.",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825-2830.",
        "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. <i>Journal of Computational and Applied Mathematics</i>, 20, 53-65.",
        "Strang, G. (2016). <i>Introduction to linear algebra</i> (5th ed.). Wellesley-Cambridge Press.",
        "Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. <i>Journal of the American Statistical Association</i>, 58(301), 236-244."
    ]
    for ref in referencias:
        story.append(Paragraph(ref, ref_style))

    doc.build(story, canvasmaker=APANumberedCanvas)
    print(f"[OK] Documento PDF creado exitosamente en: {PDF_OUT}")

if __name__ == "__main__":
    construir_docx()
    construir_pdf()
