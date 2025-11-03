from bs4 import BeautifulSoup

filename = 'molbase_benzidine.html'

with open(filename, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find all h3 elements and print their title attribute if present
for h3 in soup.find_all('h3'):
    title = h3.get('title')
    if title:
        print(title)