import json
import os
from bs4 import BeautifulSoup
import html
import uuid

# Read existing items.json
with open('items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Directory containing item pages
items_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'item-*.html')

# Process each item to add unique ID and extract images
for item in items:
    # Ensure every item has a unique ID
    if 'id' not in item or not item['id']:
        item['id'] = str(uuid.uuid4())
    
    if not item['item_url'] or item['item_url'] == '#':
        continue
    
    try:
        # Construct the full path to the item page
        item_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), item['item_url'])
        
        # Read and parse the item page
        with open(item_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # Find the description div
        description_div = soup.find('div', class_='item-description')
        if description_div:
            # Get the HTML content and encode it
            description_html = str(description_div)
            encoded_description = html.escape(description_html)
            item['description'] = encoded_description
            
        # Find all image links in the gallery
        gallery = soup.find('div', class_='item-gallery')
        if gallery:
            images = []
            for img_link in gallery.find_all('a'):
                img_url = img_link.get('href')
                if img_url:
                    images.append(img_url)
            item['images'] = images
            
    except Exception as e:
        print(f"Error processing {item['item_url']}: {str(e)}")

# Save the updated items.json
with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("Items have been updated with IDs and image URLs")
