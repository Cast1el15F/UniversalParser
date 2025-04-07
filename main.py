import UniversalPasrser.pars as pars
def start():
    print("1. Парсинг по url и xpath без входа в аккаунт (Используется Requests)",
    "2. Парсинг по url и xpath без входа в аккаунт (Используется Selenium)",
    sep="\n")

    type_parsing = int(input("Выберите тип парсинга: "))

    print("1. Получить весь html код элемента(ов)",
    "2. Получить результат по регулярному выражению",
    "3. Получить только текст",
    "4. Получить только названия выбранных атрибутов",
    sep="\n")

    type_elements = int(input("Выберите что вы хотите получить: "))

    if type_elements == 2:
        pattern = str(input("Введите паттерн для регулярного выражения: "))
    elif type_elements == 4:
        attribute_name = str(input("Введите какой атрибут вам нужен (например class или href)"))
    else:
        pattern = ""
        attribute_name = ""
    if type_parsing == 1:
        url = str(input("URL: "))
        xpath = str(input("Xpath: "))
        # print(url, xpath, sep="\n")
        print("Загрузка...")
        print(pars.parser_no_account_requests(url, xpath, type_elements, pattern, attribute_name))
    elif type_parsing == 2:
        url = str(input("URL: "))
        xpath = str(input("Xpath: "))
        # print(url, xpath, sep="\n")
        print("Загрузка...")
        print(pars.parser_no_account_selenium(url, xpath, type_elements, pattern, attribute_name))

if __name__ == "__main__":
    while True:
        start()

# https://www.forbes.ru/milliardery/533585-20-bogatejsih-ludej-mira-2025-rejting-forbes?image=513246
# //h2