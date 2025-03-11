from dateutil import parser
from database import Database

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService



def main():
    """
    Основная функция выполнения скрипта:
    1. Инициализирует браузер с помощью Selenium
    2. Производит парсинг данных с интерактивного графика
    3. Сохраняет данные в MySQL базу данных
    4. Обеспечивает корректное завершение работы драйвера
    """
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://www.tbank.ru/invest/indexes/TIPOUS/")

        chart = driver.find_element(By.XPATH, "//div[@data-qa-file='ChartLinear']")
        element = driver.find_element(By.XPATH, "//div[@data-qa-file='IndexOverview']")

        # Скролл до конца графика
        driver.execute_script("arguments[0].scrollIntoView(false);", element)
        chart_width = chart.size['width']

        actions = ActionChains(driver)

        data_points = []

        # Перемещаемся по графику в обратном направлении, до тех пор, пока не будет собрано 10 точек
        for i in range(chart_width, 0, -1): 
            try:
                # Наводимся на график, чтобы появилась точка
                actions.move_to_element_with_offset(chart, i, 50).perform() 
                try:
                    сhart__svg = driver.find_element(By.CLASS_NAME, "Chart__svgChartContainer__Wa5N") \
                                                                            .find_element(By.TAG_NAME, "g")
                    data = сhart__svg.find_elements(By.TAG_NAME, "text")
                    date = parser.parse(data[0].text, dayfirst=True).date()
                    value = float(data[1].text.replace(',', '.'))
                    tuple_data = (date, value)
                    
                    # Добавляем данные в список в виде кортежа (также проверяем на дубликаты)
                    if tuple_data not in data_points:
                        data_points.append(tuple_data)
                    if len(data_points) >= 10:
                        break
                except:
                    continue  
            except:
                continue 
        # Добавляем данные в бд 
        db = Database()
        db.insert_data(data_points)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()