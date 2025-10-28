==========================================
🌐 WIKIPEDIA PATHFINDER
==========================================

Wikipedia Pathfinder es una aplicación interactiva construida con Streamlit que permite encontrar una ruta entre dos páginas de Wikipedia, utilizando un algoritmo de búsqueda heurística basada en similitud semántica (TF-IDF + Cosine Similarity).

El objetivo es simular cómo una persona podría “navegar” de un tema a otro en Wikipedia siguiendo enlaces relevantes, pero de manera automatizada y eficiente.

------------------------------------------
🚀 CARACTERÍSTICAS
------------------------------------------
- 🔍 Búsqueda heurística en la red de Wikipedia.  
- 📊 Visualización de progreso y registros en tiempo real.  
- 🧠 Algoritmo optimizado usando TF-IDF y similitud coseno.  
- 🐳 Distribución lista para usar con Docker.  
- 💻 Interfaz moderna y simple construida con Streamlit.

------------------------------------------
🧠 CÓMO FUNCIONA EL ALGORITMO
------------------------------------------
El algoritmo busca conectar dos artículos de Wikipedia (inicio → objetivo) siguiendo enlaces internos, priorizando aquellos más semánticamente similares al objetivo.

1️⃣ **Obtención de enlaces**  
   Para una página dada, se obtienen todos los enlaces salientes (`pagina.links`).

2️⃣ **Cálculo de similitud**  
   Se usa TF-IDF (Term Frequency–Inverse Document Frequency) para representar los textos como vectores y se calcula la similitud coseno entre:
   - el texto del artículo objetivo  
   - los títulos de los enlaces salientes

   Esto permite estimar qué enlaces son “más cercanos” al objetivo en significado.

3️⃣ **Expansión heurística**  
   El algoritmo usa una cola de prioridad (PriorityQueue) donde cada nodo tiene un “costo” calculado así:
      prioridad = -similitud × β
      Donde **β** es el parámetro de peso que define cuánto influye la similitud en la búsqueda.

El nodo con mayor similitud (menor prioridad numérica) se explora primero, y así sucesivamente, hasta:
- alcanzar el objetivo, o  
- llegar al límite de profundidad (`max_depth`) o tiempo (`max_time`).

------------------------------------------
🧩 ESTRUCTURA DEL PROYECTO
------------------------------------------
wikipedia-pathfinder/
├── app.py                # Aplicación principal de Streamlit
├── Dockerfile            # Imagen lista para ejecutar la app
├── requirements.txt      # Dependencias del proyecto
└── README_FULL.txt       # Documentación (este archivo)

------------------------------------------
⚙️ INSTALACIÓN Y USO
------------------------------------------

🐳 OPCIÓN 1 — USAR DOCKER (RECOMENDADA)

1️⃣ Clona el repositorio:
git clone https://github.com/<tu_usuario>/wikipedia-pathfinder.git
cd wikipedia-pathfinder
2️⃣ Construye la imagen:
docker build -t wikipedia-pathfinder .
3️⃣ Ejecuta el contenedor:
docker run -p 8501:8501 wikipedia-pathfinder

💻 OPCIÓN 2 — EJECUTAR LOCALMENTE (SIN DOCKER)

1️⃣ Instala las dependencias:
pip install -r requirements.txt
2️⃣ Ejecuta la app:
streamlit run app.py

🧪 PARÁMETROS DISPONIBLES
------------------------------------------------------------------------------------------------
| Parámetro                 | Descripción                                  | Valor por defecto |
| ------------------------- | -------------------------------------------- | ----------------- |
| **Página de inicio**      | Artículo desde el que comienza la búsqueda   | "Napoleon"        |
| **Página objetivo**       | Artículo que se intenta alcanzar             | "Apollo 11"       |
| **Profundidad máxima**    | Máximo número de saltos entre artículos      | 10                |
| **Tiempo máximo (s)**     | Límite de ejecución de la búsqueda           | 60                |
------------------------------------------------------------------------------------------------

🧑‍💻 AUTOR

Creado por Alejandro Rodríguez
📧 alejandro.rodricoll@gmail.com

🪪 LICENCIA

Este proyecto se distribuye bajo la licencia MIT, por lo que puedes usarlo, modificarlo y distribuirlo libremente, siempre que se mantenga el reconocimiento al autor original.

“La curiosidad es el motor del conocimiento; Wikipedia Pathfinder es una forma de seguir ese impulso, paso a paso.”
