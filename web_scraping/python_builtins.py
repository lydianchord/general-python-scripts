import bs4
import requests

r = requests.get('https://docs.python.org/3/library/functions.html')
soup = bs4.BeautifulSoup(r.text, 'lxml')

func_table = soup.find('table')
cells = func_table.select('td')
funcs = (cell.text.strip('()') for cell in cells if cell.text[-1] == ')')

func_string = ' '.join(funcs)
with open('output/python_builtins.txt', 'w') as file:
    file.write(func_string)

# In Notepad++: Settings > Style Configurator > Python > KEYWORDS
