import json
from bs4 import BeautifulSoup

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all item cards
item_cards = soup.find_all('div', class_='item-card')

# Create list to store item data
items = []

# Process each item card
for card in item_cards:
    # Extract title and item page URL
    title_link = card.find('h3').find('a')
    if title_link:
        title = title_link.text.strip()
        item_url = title_link.get('href', '')
    else:
        title = card.find('h3').text.strip()
        item_url = ''
    
    # Extract image URL
    image_container = card.find('div', class_='image-container')
    if image_container:
        image_link = image_container.find('a')
        if image_link:
            img = image_link.find('img')
            image_url = img.get('src', '') if img else ''
        else:
            image_url = ''
    else:
        image_url = ''
    
    # Extract prices
    price_section = card.find('div', class_='price-section')
    price_old = price_section.find('span', class_='price-old')
    price = price_section.find('span', class_='price')
    
    # Extract status
    status = price_section.find('span', class_='status-text')
    
    # Create item dictionary
    item = {
        'title': title,
        'item_url': item_url,
        'image_url': image_url,
        'price_old': price_old.text.strip() if price_old else None,
        'price': price.text.strip() if price else None,
        'status': status.text.strip() if status else None
    }
    
    items.append(item)

# Save to JSON file
with open('items.json', 'w', encoding='utf-8') as json_file:
    json.dump(items, json_file, ensure_ascii=False, indent=2)

print(f"Extracted {len(items)} items and saved to items.json")
