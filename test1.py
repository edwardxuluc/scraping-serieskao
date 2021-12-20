from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json

def create_file(nombre, data):
    print('generando archivo ', nombre)
    with open(nombre + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_enlaces_episodio(url):
    print('obteniendo enlaces: ', url)

    resultado = {
        'opcion_1': '',
        'opcion_2': '',
        'opcion_3': '',
        'opcion_4': '',
        'opcion_5': '',
    }

    browser2 = webdriver.Chrome()
    browser2.get(url)

    # links_container = browser2.find_element_by_xpath('//*[@id="PlayerDisplay"]/div[3]/div/div')
    links = browser2.find_elements_by_xpath('//*[@id="PlayerDisplay"]/div[3]/div/div/li')

    for link in links:
        # obtener el texto del li
        link_title = link.find_element_by_xpath('.//span').text
        # obtener el id del enlace
        link_id = link.get_attribute('onclick')
        # reemplazar strings no validos
        link_id = link_id.replace('go_to_player(\'', '').replace('\', 2, 1);', '')
        # agregar el path inicial
        link_id = 'https://kaocentro.net/player/?id=' + link_id

        if link_title == 'FEMBED':
            resultado['opcion_1'] = link_id
        elif link_title == 'AMAZON':
            resultado['opcion_2'] = link_id
        elif link_title == 'NETU':
            resultado['opcion_3'] = link_id
        elif link_title == 'HYDRAX':
            resultado['opcion_4'] = link_id
        elif link_title == 'ZPLAYER':
            resultado['opcion_5'] = link_id

    browser2.quit()

    return resultado

def get_info_episodio(url):
    print('obteniendo informacion: ', url)
    browser = webdriver.Chrome()
    browser.get(url)

    titulo = browser.find_element_by_xpath('//*[@id="info"]/h1').text
    descripcion = browser.find_element_by_xpath('//*[@id="info"]/div/p').text
    url_opciones = browser.find_element_by_xpath('//*[@id="dooplay_player_response"]/div/iframe').get_attribute('src')

    browser.quit()

    return {
        'titulo': titulo,
        'descripcion': descripcion,
        'url_opciones': url_opciones,
    }

    return res

def get_enlaces_temporada(browser, temporada_requerida):

    resultado = {
        'numero': '',
        'episodios': []
    }

    # buscar las temporadas
    temporadas = browser.find_element_by_xpath('//*[@id="seasons"]')
    temporadas = temporadas.find_elements_by_xpath('//*[@class="se-c"]')

    for temporada in temporadas:
        numero_temporada = temporada.get_attribute('data-season')
        if numero_temporada == temporada_requerida:
            print('Temporada encontrada')

            resultado['numero'] = numero_temporada
            episodios = temporada.find_elements_by_xpath('.//li')

            for episodio in episodios:
                resultado['episodios'].append({
                    'url': episodio.find_element_by_xpath('.//a').get_attribute('href'),
                    'portada': episodio.find_element_by_xpath('.//img').get_attribute('src')
                })

    return resultado




temporada_requerida = '4'
count = 1
max_count = 100

browser = webdriver.Chrome()
browser.get('https://serieskao.tv/animes/coraje-el-perro-cobarde/')

resultado = get_enlaces_temporada(browser, temporada_requerida)

for episodio in resultado['episodios']:
    if count <= max_count:
        informacion = get_info_episodio(episodio['url'])
        enlaces = get_enlaces_episodio(informacion['url_opciones'])

        episodio['titulo'] = informacion['titulo']
        episodio['descripcion'] = informacion['descripcion']
        episodio['opcion_1'] = enlaces['opcion_1']
        episodio['opcion_2'] = enlaces['opcion_2']
        episodio['opcion_3'] = enlaces['opcion_3']
        episodio['opcion_4'] = enlaces['opcion_4']
        episodio['opcion_5'] = enlaces['opcion_5']
        count = count + 1

nombre_archivo = 'temporada_' + str(temporada_requerida)
create_file(nombre_archivo, resultado['episodios'])

print(resultado)

browser.quit()