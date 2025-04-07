from selenium import webdriver
import requests
from lxml import html
import re
# import time

def parser_no_account_selenium(url: str, xpath: str, type_elements: int, pattern: str, attribute_name: str) -> str:
    # устанавливаем параметры веб драйвера
    chrome_options = webdriver.ChromeOptions()
    """
    Создается объект chrome_options, который 
    позволяет задавать параметры (опции) для браузера Chrome. 
    Эти параметры помогут изменить поведение браузера, например, 
    отключить загрузку изображений, запустить его в безголовом режиме 
    и т. д.
    """
    chrome_options.add_argument("--blink-settings=imagesEnabled=False")
    """
    Этот аргумент отключает загрузку изображений на страницах.
    --blink-settings=imagesEnabled=false — это внутренняя настройка движка Blink (рендеринг-движок Chrome), которая предотвращает загрузку изображений.
    Это помогает ускорить работу браузера и уменьшить потребление трафика.
    """
    chrome_options.add_argument("headless") # ("--incognito") # 
    """
    Запускает браузер в безголовом режиме (headless). Используем ("--incognito") чтобы видеть что происходит в браузере
    Это значит, что Chrome будет работать в фоновом режиме, без отображения окна.
    Полезно для автоматизированного тестирования, парсинга сайтов и других задач, где не нужен видимый браузер.
    """
    chrome_options.add_argument("no-sandbox")
    """
    Отключает песочницу (sandbox) Chrome.
    Это иногда требуется при запуске браузера в среде, где могут возникнуть проблемы с правами доступа (например, на серверах).
    Песочница — это механизм безопасности, который ограничивает доступ браузера к системе, но иногда может вызывать ошибки в автоматизации.
    """
    chrome_options.add_argument("disable-dev-shm-usage")
    """
    Отключает использование /dev/shm (общей памяти между процессами).
    По умолчанию Chrome использует /dev/shm для хранения временных файлов, но на некоторых системах (например, в Docker-контейнерах) размер этой памяти ограничен.
    Этот параметр предотвращает возможные ошибки из-за нехватки памяти.
    """
    driver = webdriver.Chrome(options=chrome_options)
    """
    Создается объект driver, который управляет браузером Chrome с заданными параметрами.
    webdriver.Chrome(options=chrome_options) передает ранее настроенные параметры в браузер.
    driver можно использовать для навигации, парсинга, кликов по элементам и других действий на веб-страницах.
    """

    driver.get(url) # Заходим на сайт

    # page_sourse = driver.page_source # Получаем html страницы, это не надо

    elements = driver.find_elements("xpath", xpath)

    # Вывод HTML кода всех найденных элементов

    result = ""

    if type_elements == 1:
        for element in elements:
            result += element.get_attribute("outerHTML").strip() + "\n"
        return result.strip()
    if type_elements == 2:
        # Собираем HTML всех элементов
        for element in elements:
            result += element.get_attribute("outerHTML") + "\n"
        # Применяем регулярное выражение
        matches = re.findall(pattern, result)
        # Объединяем найденное в строку
        return "\n".join(matches).strip()
    if type_elements == 3:
        for element in elements:
            result += element.text.strip() + "\n"
        return result.strip()
    if type_elements == 4:
        # получаем имя классов
        for element in elements:
            en = element.get_attribute(attribute_name) # создаем переменную для удобства
            if en:  # Проверим, что класс вообще есть
                result += en.strip() + "\n"
        return result.strip()
    driver.quit()

def parser_no_account_requests(url: str, xpath: str, type_elements: int, pattern: str, attribute_name: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"} # отправляем запрос от браузера
    response = requests.get(url, headers=headers) # отправляем запрос на сайт
    tree = html.fromstring(response.text) # получаем все элементы сайта
    elements = tree.xpath(xpath) # ищем по xpath нужные элементы
    # Соберём HTML-код всех найденных элементов
    result = "" # создаем переменную в которую будем складывать результаты
    if type_elements == 1: 
        for element in elements: # просматриваем все элементы
            result += html.tostring(element, encoding='unicode') + "\n" # расшифровываем и записываем в result
        return result.strip()
    if type_elements == 2:
        for element in elements:
            result += html.tostring(element, encoding='unicode') + "\n"
        # Применяем регулярное выражение
        matches = re.findall(pattern, result)
        # Возвращаем результат
        return "\n".join(matches).strip()
    elif type_elements == 3:
        # Соберём только текст из найденных элементов
        for element in elements:
            result += element.text_content().strip() + "\n"
        return result.strip()
    elif type_elements == 4:
        # получаем имя классов
        for element in elements:
            result += element.get(attribute_name, "").strip() + "\n"
        return result.strip()

if __name__ == "__main__": # для быстрых тестов
    url = 'https://www.forbes.ru/milliardery/533585-20-bogatejsih-ludej-mira-2025-rejting-forbes?image=513246' #str(input("URL: "))
    xpath = '//h2' # str(input("Xpath: "))
    type_elements = 4
    pattern = r'[1-9]'
    attribute_name = 'class'
    # print(url, xpath, sep="\n")
    print(parser_no_account_selenium(url, xpath, type_elements, pattern, attribute_name))