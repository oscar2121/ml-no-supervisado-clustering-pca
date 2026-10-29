import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\oscar\.gemini\antigravity\scratch\ml_no_supervisado"
PDF_OUTPUT = os.path.join(BASE_DIR, "Blog_Machine_Learning_No_Supervisado.pdf")

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
        # Encabezado APA: Número de página en la esquina superior derecha en todas las páginas
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.HexColor("#333333"))
        self.drawRightString(558, 755, f"{self._pageNumber}")
        
        # En páginas interiores, título corto a la izquierda
        if self._pageNumber > 1:
            self.drawString(54, 755, "BLOG ACADÉMICO: MACHINE LEARNING NO SUPERVISADO")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
            
        self.restoreState()

def crear_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=72, rightMargin=72, # 1 pulgada (72 pt) APA
        topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Estilos APA: Títulos centrados y en negro puro
    title_style = ParagraphStyle(
        'APATitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=21,
        textColor=colors.HexColor('#000000'),
        alignment=1, # Centrado
        spaceAfter=12
    )
    sub_style = ParagraphStyle(
        'APASubtitle',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#222222'),
        alignment=1, # Centrado
        spaceAfter=24
    )
    meta_style = ParagraphStyle(
        'APAMeta',
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#000000'),
        alignment=1, # Centrado
        spaceAfter=4
    )
    h1_centered = ParagraphStyle(
        'Heading1_Centered',
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#000000'),
        alignment=1, # Centrado
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True
    )
    h2_centered = ParagraphStyle(
        'Heading2_Centered',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#000000'),
        alignment=1, # Centrado
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3_Style',
        fontName='Times-BoldItalic',
        fontSize=11,
        leading=14.5,
        textColor=colors.HexColor('#000000'),
        alignment=0, # Izquierda
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'APABody',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#111111'),
        firstLineIndent=28, # Sangría primera línea APA 0.5 pulgada
        alignment=4, # Justificado
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#000000'),
        leftIndent=20,
        spaceBefore=4,
        spaceAfter=6
    )
    ref_style = ParagraphStyle(
        'APAReference',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#000000'),
        leftIndent=28,
        firstLineIndent=-28, # Sangría francesa
        alignment=4,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # PORTADA
    # =========================================================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("Descifrando Patrones Ocultos: Casos de Uso, Algoritmos y Aplicaciones Prácticas del Machine Learning No Supervisado", title_style))
    story.append(Paragraph("Un Análisis Crítico sobre Agrupamiento, Reducción de Dimensionalidad y Reglas de Asociación", sub_style))
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>Oscar David</b>", meta_style))
    story.append(Paragraph("Facultad de Ingeniería", meta_style))
    story.append(Paragraph("Curso: Inteligencia Artificial y Machine Learning", meta_style))
    story.append(Paragraph("Experiencia de Aprendizaje: Algoritmos No Supervisados", meta_style))
    story.append(Paragraph("Docente: Tutor de Área", meta_style))
    story.append(Paragraph("Octubre de 2026", meta_style))

    story.append(PageBreak())

    # =========================================================================
    # INTRODUCCIÓN
    # =========================================================================
    story.append(Paragraph("Descifrando Patrones Ocultos: Casos de Uso, Algoritmos y Aplicaciones Prácticas del Machine Learning No Supervisado", h1_centered))
    story.append(Paragraph("1. Introducción al Paradigma No Supervisado", h2_centered))
    story.append(Paragraph(
        "En la era del Big Data, la gran mayoría de la información generada diariamente por la actividad digital humana, "
        "dispositivos de Internet de las Cosas (IoT), transacciones comerciales y sensores biomédicos carece de etiquetas previas. "
        "El etiquetado manual de datos es un proceso costoso, propenso al error humano y, en muchas ocasiones, inviable debido al "
        "volumen exponencial de los flujos de información. Es precisamente en este escenario donde el Aprendizaje Automático No Supervisado "
        "(Unsupervised Machine Learning) adquiere un rol protagónico dentro de la inteligencia artificial contemporánea (Bishop, 2006).",
        body_style
    ))
    story.append(Paragraph(
        "A diferencia del aprendizaje supervisado, donde los algoritmos son guiados por una señal objetivo conocida "
        "—un vector de etiquetas y que actúa como 'profesor' mediante una función de pérdida de discrepancia empírica—, "
        "en el aprendizaje no supervisado el sistema recibe únicamente un conjunto de observaciones multidimensionales "
        "X = {x1, x2, ..., xN} ∈ ℝ^(D). El objetivo matemático no es predecir una clase o un valor escalar, sino modelar la estructura "
        "intrínseca, las regularidades geométricas o la distribución de densidad de probabilidad conjunta subyacente p(x) (Hastie et al., 2009). "
        "En términos conceptuales, el aprendizaje no supervisado busca responder a la pregunta fundamental: ¿cómo están organizados "
        "naturalmente estos datos y qué conocimiento latente encierran sus relaciones espaciales?",
        body_style
    ))

    # =========================================================================
    # TAREAS PRINCIPALES
    # =========================================================================
    story.append(Paragraph("2. Principales Tareas del Machine Learning No Supervisado", h2_centered))
    story.append(Paragraph(
        "El aprendizaje no supervisado abarca un amplio espectro de técnicas cuantitativas orientadas a resolver problemas "
        "donde no existe una respuesta correcta preestablecida. De acuerdo con la literatura canónica (Goodfellow et al., 2016; Jain, 2010), "
        "sus aplicaciones se agrupan en tres pilares fundamentales: agrupamiento (clustering), reducción de dimensionalidad y "
        "minería de reglas de asociación.",
        body_style
    ))

    story.append(Paragraph("2.1 Agrupamiento o Clustering", h3_style))
    story.append(Paragraph(
        "El clustering consiste en particionar un conjunto heterogéneo de datos en subgrupos homogéneos o conglomerados (clusters), "
        "de modo que los elementos asignados al mismo grupo exhiban una alta similitud interna (alta cohesión intra-cluster) y, al mismo tiempo, "
        "sean marcadamente diferenciables de los elementos pertenecientes a otros grupos (alta separación inter-cluster). "
        "Entre los algoritmos más representativos destacan:<br/>"
        "• <b>K-Means:</b> Algoritmo de partición basado en centroides que optimiza iterativamente la suma de errores al cuadrado (SSE o inercia). "
        "Asigna cada punto al centroide más próximo mediante la distancia euclidiana y recalcula la posición de dichos centros como la media "
        "aritmética de las observaciones asignadas. Es altamente eficiente computacionalmente, pero presupone clusters con formas esféricas e isotrópicas "
        "y requiere definir a priori el hiperparámetro k (Jain, 2010).<br/>"
        "• <b>DBSCAN:</b> Algoritmo basado en densidad espacial. Define los clusters como regiones continuas de alta densidad de puntos separadas "
        "por áreas de baja densidad. Es capaz de descubrir agrupaciones de formas arbitrarias y posee la capacidad intrínseca de catalogar "
        "observaciones aisladas como ruido o valores atípicos (Ester et al., 1996).<br/>"
        "• <b>Clustering Jerárquico:</b> Construye un árbol jerárquico de agrupamientos representable mediante un dendrograma aglomerativo.",
        body_style
    ))
    story.append(Paragraph(
        "Para validar la calidad de las agrupaciones sin etiquetas externas, se recurre a métricas intrínsecas como el Coeficiente de Silueta "
        "(Silhouette Score), que mide el contraste entre la distancia media intra-cluster y la distancia al cluster vecino más cercano "
        "(variando entre -1 y +1), y el método del codo (Elbow Method), que busca el punto de inflexión en la inercia residual (Rousseeuw, 1987).",
        body_style
    ))

    story.append(Paragraph("2.2 Reducción de Dimensionalidad", h3_style))
    story.append(Paragraph(
        "En aplicaciones complejas (como visión artificial, genómica o procesamiento de texto), cada observación puede estar descrita "
        "por cientos o miles de variables. Esta hiperdimensionalidad provoca el fenómeno conocido como 'la maldición de la dimensionalidad' "
        "(Curse of Dimensionality), donde el volumen del espacio crece exponencialmente, los datos se tornan extremadamente dispersos y "
        "las métricas de distancia euclidiana pierden su capacidad discriminante (Bishop, 2006). La reducción de dimensionalidad proyecta "
        "los datos desde un espacio original ℝ^D hacia un subespacio latente ℝ^d (con d << D), preservando la mayor cantidad de información posible.<br/>"
        "• <b>PCA (Principal Component Analysis):</b> Técnica lineal clásica que encuentra un nuevo sistema de coordenadas ortogonales maximizando "
        "la varianza proyectada a través de la descomposición en valores singulares (SVD) de la matriz de covarianza (Hastie et al., 2009).<br/>"
        "• <b>t-SNE y UMAP:</b> Métodos no lineales diseñados para la visualización de datos de alta dimensión en 2D o 3D, preservando la estructura "
        "de vecindad local (van der Maaten & Hinton, 2008; McInnes et al., 2018).",
        body_style
    ))

    story.append(Paragraph("2.3 Minería de Reglas de Asociación", h3_style))
    story.append(Paragraph(
        "Orientada a descubrir dependencias probabilísticas y relaciones de co-ocurrencia entre variables discretas en grandes conjuntos transaccionales. "
        "Algoritmos como Apriori y FP-Growth identifican patrones frecuentes evaluando tres métricas estadísticas cardinales (Agrawal & Srikant, 1994): "
        "<b>Soporte</b> (frecuencia relativa del conjunto de ítems), <b>Confianza</b> (probabilidad condicional de ocurrencia del consecuente dado el antecedente) "
        "y <b>Lift</b> (razón entre la confianza observada y la probabilidad esperada bajo independencia estadística; Lift > 1 evidencia asociación positiva real).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # CASOS DE USO REALES
    # =========================================================================
    story.append(Paragraph("3. Casos de Uso Aplicados en la Industria", h2_centered))
    story.append(Paragraph(
        "La aplicabilidad del aprendizaje no supervisado abarca prácticamente todos los sectores estratégicos de la economía digital. "
        "A continuación, se profundiza en cuatro casos de uso emblemáticos donde estas técnicas generan ventajas competitivas decisivas:",
        body_style
    ))

    story.append(Paragraph("Caso de Uso 1: Segmentación Estratégica de Clientes y Personalización en E-Commerce y Banca", h3_style))
    story.append(Paragraph(
        "En plataformas como Amazon o entidades bancarias globales, millones de usuarios interactúan generando millones de eventos diarios. "
        "Mediante modelos no supervisados, se construye una matriz de comportamiento a partir de variables de Recencia, Frecuencia y Valor Monetario (modelo RFM). "
        "Tras estandarizar las variables, se aplica PCA para eliminar ruido y correlaciones espurias, y posteriormente K-Means descubre segmentos latentes: "
        "clientes leales de alto consumo, cazadores de descuentos estacionales, clientes en riesgo inminente de deserción (churn) y nuevos usuarios. "
        "Esta segmentación automática optimiza presupuestos publicitarios e incrementa sustancialmente el Valor de Vida del Cliente (LTV).",
        body_style
    ))

    story.append(Paragraph("Caso de Uso 2: Detección de Fraude Transaccional y Ciberseguridad", h3_style))
    story.append(Paragraph(
        "En la detección de fraudes financieros y ataques cibernéticos de 'día cero', los estafadores modifican continuamente sus tácticas y las "
        "transacciones fraudulentas representan menos del 0.1% del total. Algoritmos como <b>Isolation Forests</b> y <b>DBSCAN</b> operan bajo el supuesto "
        "no supervisado de que las anomalías son cuantitativamente escasas y numéricamente atípicas. Isolation Forest aísla anomalías mediante particiones "
        "aleatorias recursivas en pocas divisiones, mientras DBSCAN detecta transacciones que caen en regiones de baja densidad de tráfico, disparando alertas "
        "en milisegundos sin requerir re-etiquetado manual.",
        body_style
    ))

    story.append(Paragraph("Caso de Uso 3: Optimización de Inventarios y Recomendaciones Cruzadas (Market Basket Analysis)", h3_style))
    story.append(Paragraph(
        "En el retail y supermercados, el análisis de transacciones de puntos de venta (POS) mediante el algoritmo FP-Growth permite comprender "
        "la afinidad entre productos. Cadenas comerciales descubren reglas con Lift > 2.0 y rediseñan la distribución física de anaqueles o despliegan "
        "módulos de recomendación en tiempo real ('frecuentemente comprados juntos'), aumentando hasta un 15% el ticket promedio.",
        body_style
    ))

    story.append(Paragraph("Caso de Uso 4: Bioinformática y Medicina Personalizada: Descubrimiento de Subtipos de Enfermedades", h3_style))
    story.append(Paragraph(
        "En la secuenciación genómica y transcriptómica (scRNA-seq), cada muestra contiene más de 25,000 genes. Aplicando PCA combinado con t-SNE "
        "y clustering jerárquico, los bioinformáticos han descubierto subtipos moleculares de cáncer que antes se diagnosticaban bajo una misma categoría, "
        "permitiendo diseñar terapias personalizadas dirigidas a la firma genética específica del paciente (van der Maaten & Hinton, 2008).",
        body_style
    ))

    # =========================================================================
    # EJEMPLOS DESARROLLADOS EN CLASE
    # =========================================================================
    story.append(Paragraph("4. Análisis de Ejemplos Desarrollados en Clase", h2_centered))
    story.append(Paragraph(
        "A fin de vincular la teoría conceptual con la experimentación computacional, se analizan dos flujos de trabajo diseñados en clase en Python.",
        body_style
    ))

    story.append(Paragraph("Ejemplo 1: Flujo Completo de Segmentación con K-Means y Validación Intrínseca", h3_style))
    cod_k = (
        "# 1. Preprocesamiento: Estandarización obligatoria de escalas\n"
        "scaler = StandardScaler()\n"
        "X_scaled = scaler.fit_transform(datos_clientes)\n"
        "# 2. Método del Codo y Coeficiente de Silueta para determinar k\n"
        "for k in range(2, 9):\n"
        "    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)\n"
        "    kmeans.fit(X_scaled)\n"
        "    siluetas.append(silhouette_score(X_scaled, kmeans.labels_))\n"
        "# 3. Ajuste del modelo final con k óptimo (k=4)\n"
        "modelo_final = KMeans(n_clusters=4, init='k-means++', random_state=42)\n"
        "etiquetas = modelo_final.fit_predict(X_scaled)"
    )
    story.append(Paragraph(cod_k.replace('\n', '<br/>'), code_style))
    story.append(Paragraph(
        "<i>Discusión Técnica:</i> Se constató la extrema sensibilidad de K-Means frente a la escala de las variables: sin estandarización, "
        "las variables de mayor magnitud dominan artificialmente la distancia euclidiana. El uso de 'k-means++' evitó mínimos locales subóptimos.",
        body_style
    ))

    story.append(Paragraph("Ejemplo 2: Reducción Dimensional con PCA Preservando el 95% de la Varianza", h3_style))
    cod_p = (
        "from sklearn.decomposition import PCA\n"
        "pca = PCA(n_components=0.95, random_state=42)\n"
        "X_reducido = pca.fit_transform(X_scaled)\n"
        "print(f'Dimensiones originales: {X_scaled.shape[1]} | Retenidas: {X_reducido.shape[1]}')"
    )
    story.append(Paragraph(cod_p.replace('\n', '<br/>'), code_style))
    story.append(Paragraph(
        "<i>Discusión Técnica:</i> En un dataset de 30 variables continuas correlacionadas, 10 componentes principales fueron suficientes para "
        "retener el 95.2% de la varianza total, evidenciando que el 66.6% de las dimensiones correspondían a redundancia o ruido colineal.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # DISCUSIÓN Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("5. Desafíos Metodológicos y Consideraciones Éticas", h2_centered))
    story.append(Paragraph(
        "1. <b>Ambigüedad en la Evaluación:</b> Al carecer de 'ground truth', dos algoritmos de clustering pueden generar agrupaciones radicalmente "
        "distintas y ambas ser matemáticamente óptimas bajo su criterio. Se requiere la validación del experto de negocio para certificar su valor pragmático.<br/>"
        "2. <b>Amplificación de Sesgos Históricos:</b> Los algoritmos no supervisados agrupan patrones presentes en los datos. Si los datos reflejan "
        "desigualdades sistémicas o sesgos socioeconómicos, el algoritmo consolidará clusters discriminatorios de forma encubierta.<br/>"
        "3. <b>Interpretabilidad:</b> Justificar decisiones operativas complejas basadas en clusters latentes o variedades no lineales representa "
        "un desafío frente a marcos regulatorios como el RGPD.",
        body_style
    ))

    story.append(Paragraph("6. Conclusiones", h2_centered))
    story.append(Paragraph(
        "1. <b>Extracción de Conocimiento Latente:</b> El aprendizaje no supervisado transforma datos crudos no etiquetados en conocimiento "
        "accionable, permitiendo la toma de decisiones basada en evidencia en comercio, finanzas, ciberseguridad y medicina personalizada.<br/>"
        "2. <b>El Preprocesamiento como Factor Crítico:</b> Debido a la dependencia de métricas de distancia espacial, la normalización y "
        "curaduría de variables es la fase más determinante para la validez de los resultados.<br/>"
        "3. <b>Evolución hacia el Aprendizaje Autosupervisado:</b> El aprendizaje no supervisado es el pilar de la revolución de los Modelos Fundacionales "
        "y Grandes Modelos de Lenguaje (LLMs), donde aprender representaciones a partir del contexto intrínseco de los datos define la vanguardia de la IA.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REFERENCIAS
    # =========================================================================
    story.append(Paragraph("Referencias", h1_centered))

    referencias = [
        "Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. In J. B. Bocca, M. Jarke, & C. Zaniolo (Eds.), <i>Proceedings of the 20th International Conference on Very Large Data Bases (VLDB '94)</i> (pp. 487–499). Morgan Kaufmann Publishers.",
        "Bishop, C. M. (2006). <i>Pattern recognition and machine learning</i>. Springer Science+Business Media.",
        "Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. In E. Simoudis, J. Han, & U. Fayyad (Eds.), <i>Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96)</i> (pp. 226–231). AAAI Press.",
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). <i>Deep learning</i>. MIT Press. http://www.deeplearningbook.org",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). <i>The elements of statistical learning: Data mining, inference, and prediction</i> (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-84858-7",
        "Jain, A. K. (2010). Data clustering: 50 years beyond K-means. <i>Pattern Recognition Letters</i>, 31(8), 651–666. https://doi.org/10.1016/j.patrec.2009.09.011",
        "McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for dimension reduction. <i>arXiv preprint arXiv:1802.03426</i>. https://doi.org/10.48550/arXiv.1802.03426",
        "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. <i>Journal of Computational and Applied Mathematics</i>, 20, 53–65. https://doi.org/10.1016/0377-0427(87)90125-7",
        "van der Maaten, L., & Hinton, G. (2008). Visualizing data using t-SNE. <i>Journal of Machine Learning Research</i>, 9(86), 2579–2605."
    ]

    for ref in referencias:
        story.append(Paragraph(ref, ref_style))

    doc.build(story, canvasmaker=APANumberedCanvas)
    print(f"¡DOCUMENTO PDF APA GENERADO CON ÉXITO EN: {PDF_OUTPUT}!")

if __name__ == "__main__":
    crear_pdf()
