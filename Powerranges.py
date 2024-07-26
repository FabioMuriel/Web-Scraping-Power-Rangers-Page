import requests
from bs4 import BeautifulSoup as b
from PIL import Image
import io
import os

base_url = "http://www.rangercentral.com"
url = "http://www.rangercentral.com/database/index.htm"

generaciones = []
generacion_esp = []
nombre_generaciones = []

# Carpeta donde se guardaran las imagenes
carpeta_fotos = r"C:\Users\RYZEN\Desktop\Web-Scraping-Power-Rangers-Page\images"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
}

html = requests.get(url, headers=headers)
content = html.content
soup = b(content, "lxml")

for gen in soup.findAll("li", {"class": "leaf"}):
    link = gen.find("a")
    if link is not None:
        link_url = link.get("href")
        if "/database/" in link_url and "/database/index.htm" not in link_url:
            generaciones.append(base_url + link_url)
            nombre_generaciones.append(link_url)

x = 0
y = 0
for generacion in generaciones:
    html = requests.get(generacion, headers=headers)
    content = html.content
    soup = b(content, "lxml")
    post = soup.find("div", {"class": "menu-block-wrapper"})
    nombre_gen = nombre_generaciones[x].split("/")
    nombre_gen = nombre_gen[2]
    for enlace_individual in post.findAll("li", {"class": "leaf"}):
        if enlace_individual.find("a") is None or nombre_gen == "2023_cosmicfury" or nombre_gen == "2021_dinofury" or nombre_gen == "movies":
            break
        else:
            # print("Enlace individual: ", enlace_individual)
            url_pr = enlace_individual.find("a").get("href")
            if enlace_individual.find("a") is None:
                print("Enlace individual: ", enlace_individual)

            # print(url_pr)
            
            if url_pr is not None and not ("rangers.htm" in url_pr):

                if enlace_individual.find("a") is None:
                    print("Enlace individual: ", enlace_individual)
                    break

                pr_ur_completa = ("http://www.rangercentral.com/database/" + nombre_gen + "/" + url_pr)
                pagina_pr = requests.get(pr_ur_completa, headers=headers).content
                contenido = b(pagina_pr, "lxml")

                ##Obtencion de la informacion completa
                informacion = contenido.find("div", {"class": "post-outer post"})
                url_image = contenido.find("img")["src"]

                ##Obtener informacin del ranger
                informacion_ranger = informacion.find("table", {"class": "profile-page"})
                # print(informacion_ranger)
                
                if informacion_ranger is not None:
                    nombre_ranger = informacion_ranger.find("td", {"class": "profile"}).text
                    
                print(nombre_ranger.split(":")[1])
                
                if "Full Name" in nombre_ranger:
                    nombre_ranger = nombre_ranger.split(":")[1]
                else:
                    nombre_ranger = nombre_ranger[1]
                
                # Obtencion de la imagen
                pr_content_img = informacion.find("div", {"class": "profile_img"})
                pr_image_link = pr_content_img.find("img")["src"]
                pr_image_url_dowload = ("http://www.rangercentral.com/database/" + nombre_gen + "/" + pr_image_link)
                # print(pr_image_url_dowload)

                ##Descarga de la imagen
                r = requests.get(pr_image_url_dowload)
                file = io.BytesIO(r.content)
                img = Image.open(file)

                # Crear carpeta de generacion
                nombre_carpeta = nombre_gen  # Puedes cambiar esto según tu necesidad
                ruta_carpeta = os.path.join(carpeta_fotos, nombre_carpeta)
                os.makedirs(ruta_carpeta, exist_ok=True)
                
                nombre_ranger = nombre_ranger.replace('"', "")
                
                # Guardar la imagen
                img.save(os.path.join(ruta_carpeta, f"{nombre_ranger}.jpg"))

    x += 1
