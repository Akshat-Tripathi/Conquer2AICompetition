from selenium import webdriver
import os

cwd = os.path.dirname(os.path.abspath(__file__))

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(cwd + "/chromedriver.exe", chrome_options=options)

driver.get(f"file://{cwd}/map.html")
driver.fullscreen_window()

def set_country(country_code, number, colour):
    driver.execute_script(f"""
        var country = document.getElementsByName("{country_code}")[0];
        country.innerHTML = "{number}";
    """)
    if country_code != "PO":
        driver.execute_script(f"document.getElementById(\"{country_code}\").children[0].children[0].style.fill = \"{colour}\";")
