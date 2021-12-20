from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json

def console_log(value):
    print('-----------------------------------------------')
    print(value)
    print('-----------------------------------------------')


def create_file(nombre, data):
    print('generando archivo ', nombre)
    with open(nombre + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_enlaces_episodio(browser, url):
    print('obteniendo enlaces: ', url)

    resultado = {
        'opcion_1': '',
        'opcion_2': '',
        'opcion_3': '',
        'opcion_4': '',
        'opcion_5': '',
    }

    # browser = webdriver.Chrome()
    browser.get(url)

    # links_container = browser.find_element_by_xpath('//*[@id="PlayerDisplay"]/div[3]/div/div')
    links = browser.find_elements_by_xpath('//*[@id="PlayerDisplay"]/div[3]/div/div/li')

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

    # browser.quit()
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


browser = webdriver.Chrome()
browser.get('https://serieskao.tv/animes/coraje-el-perro-cobarde/')


# buscar las temporadas
temporadas = browser.find_element_by_xpath('//*[@id="seasons"]')
temporadas = temporadas.find_elements_by_xpath('//*[@class="se-c"]')
# print('temporadas: ', len(temporadas) )

resultado = {
    'numero': '',
    'episodios': []
}

for temporada in temporadas:
    numero_temporada = temporada.get_attribute('data-season')
    if numero_temporada == '1':

        resultado['numero'] = numero_temporada
        episodios = temporada.find_elements_by_xpath('.//li')

        for episodio in episodios:
            resultado['episodios'].append({
                'url': episodio.find_element_by_xpath('.//a').get_attribute('href'),
                'portada': episodio.find_element_by_xpath('.//img').get_attribute('src')
            })

count = 1
for episodio in resultado['episodios']:
    if count == 1:
        informacion = get_info_episodio(browser, episodio['url'])
        enlaces = get_enlaces_episodio(browser, informacion['url_opciones'])

        episodio['titulo'] = informacion['titulo']
        episodio['descripcion'] = informacion['descripcion']
        episodio['opcion_1'] = enlaces['opcion_1']
        episodio['opcion_2'] = enlaces['opcion_2']
        episodio['opcion_3'] = enlaces['opcion_3']
        episodio['opcion_4'] = enlaces['opcion_4']
        episodio['opcion_5'] = enlaces['opcion_5']
        count = count + 1

browser.quit()
print(resultado)
create_file('resultado', resultado)