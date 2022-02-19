from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# driver = webdriver.Edge(EdgeChromiumDriverManager().install())
driver = webdriver.Edge()

search_url = "https://www.elmenus.com/cairo/search-burger?query={q}"

driver.get(search_url.format(q='burger'))

elements = driver.find_elements_by_xpath("//*[@class='card-title']")

data = [element.text for element in elements]
print(data)