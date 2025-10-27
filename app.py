import streamlit as st
import wikipediaapi
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from queue import PriorityQueue
import math

st.set_page_config(page_title="Wikipedia Pathfinder", page_icon="🌐", layout="wide")

# Inicializa la API de Wikipedia (usuario neutro)
wiki = wikipediaapi.Wikipedia(language="en", user_agent="WikipediaPathfinder/1.0 (github)")

def obtener_texto(titulo):
    try:
        page = wiki.page(titulo)
        return page.text or ""
    except Exception:
        return ""

def get_links(pagina, visitados, costo, objetivo, resumen_objetivo):
    # Si el objetivo está directamente enlazado
    if objetivo in pagina.links:
        return [objetivo], [1.0]

    enlaces = [
        link for link in pagina.links.keys()
        if link not in visitados or visitados[link] > costo + 1
    ]
    if not enlaces:
        return None, None

    visitados.update({link: costo + 1 for link in enlaces})

    # TF-IDF sobre el texto objetivo y los títulos de enlaces
    corpus = [resumen_objetivo] + enlaces
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf = vectorizer.fit_transform(corpus)
    except Exception:
        # fallback simple: devolver primeros enlaces sin puntuación
        return enlaces[:min(5, len(enlaces))], [0.0]*min(5, len(enlaces))

    objetivo_vec = tfidf[0]
    enlaces_vecs = tfidf[1:]
    similitudes = cosine_similarity(objetivo_vec, enlaces_vecs).flatten()

    n_top = max(1, math.ceil(0.1 * len(enlaces)))
    indices_top = similitudes.argsort()[-n_top:][::-1]

    enlaces_filtrados = [enlaces[i] for i in indices_top]
    similitudes_filtradas = [similitudes[i] for i in indices_top]
    return enlaces_filtrados, similitudes_filtradas

class Nodo:
    def __init__(self, titulo, ruta):
        self.titulo = titulo
        self.ruta = ruta
    def __lt__(self, other):
        return self.titulo < other.titulo

def busqueda(inicio, objetivo, beta=1.0, max_depth=10, max_time=240, progress_bar=None, log_area=None):
    """
    Búsqueda heurística en Wikipedia.
    Se usa únicamente el parámetro beta para ponderar la similitud.
    """
    inicio_tiempo = time.perf_counter()
    visitados = {inicio: 0}
    cola = PriorityQueue()
    cola.put((0.0, Nodo(inicio, [inicio])))
    texto_objetivo = obtener_texto(objetivo)

    pasos = 0
    # Nota: prioridad = -sim * beta (mayor similitud -> menor prioridad numérica)
    while not cola.empty():
        if time.perf_counter() - inicio_tiempo > max_time:
            return None, time.perf_counter() - inicio_tiempo

        prioridad, nodo = cola.get()
        pasos += 1

        if log_area:
            log_area.text(f"Visitando: {nodo.titulo}")

        if nodo.titulo == objetivo:
            duracion = time.perf_counter() - inicio_tiempo
            return nodo.ruta, duracion

        pagina = wiki.page(nodo.titulo)
        enlaces, similitudes = get_links(pagina, visitados, len(nodo.ruta), objetivo, texto_objetivo)
        if not enlaces:
            continue

        for sim, enlace in zip(similitudes, enlaces):
            # ignorar similitudes no positivas
            if sim <= 0:
                continue
            nueva_ruta = nodo.ruta + [enlace]
            if len(nueva_ruta) > max_depth:
                continue

            hijo = Nodo(enlace, nueva_ruta)
            # Sólo usamos beta: prioridad numérica = -sim * beta
            prioridad_hijo = -sim * beta
            cola.put((prioridad_hijo, hijo))

        if progress_bar:
            # progreso aproximado: límite arbitrario para visual feedback
            progress_bar.progress(min(1.0, pasos / 1000))

    return None, time.perf_counter() - inicio_tiempo

# --- Interfaz ---
st.title("Wikipedia Pathfinder")
st.write("Encuentra rutas entre páginas de Wikipedia mediante una búsqueda guiada por similitud.")

with st.form("controls"):
    col1, col2 = st.columns(2)
    with col1:
        inicio = st.text_input("Página de inicio", "Napoleon")
        max_depth = st.slider("Profundidad máxima", 2, 30, 10, 1)
    with col2:
        objetivo = st.text_input("Página objetivo", "Apollo 11")
        max_time = st.slider("Tiempo máximo (segundos)", 10, 600, 60, 10)

    beta = 10

    submitted = st.form_submit_button("Iniciar búsqueda")

if submitted:
    spinner = st.empty()
    progress = st.progress(0)
    log = st.empty()

    spinner.info("Iniciando búsqueda...")
    ruta, duracion = busqueda(inicio.strip(), objetivo.strip(), beta=beta, max_depth=max_depth, max_time=max_time, progress_bar=progress, log_area=log)

    spinner.empty()
    if ruta:
        st.success(f"Ruta encontrada en {duracion:.2f} s")
        st.markdown("**Ruta:**")
        st.write(" → ".join(ruta))
        st.markdown(f"- Longitud: {len(ruta)}")
    else:
        st.error("No se encontró una ruta dentro de los límites indicados.")
        st.info("Prueba aumentar la profundidad o el tiempo máximo.")
