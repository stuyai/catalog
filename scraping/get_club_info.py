import csv
from bs4 import BeautifulSoup

# Define paths to the input and output files
input_file_path = './data/catalog.txt'
output_file_path = './data/clubs.csv'

# Open and read the HTML file
with open(input_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all cards (assuming each club is encapsulated within a <div> with a specific class that includes a button)
club_cards = soup.find_all('div', class_='MuiCardContent-root css-1qw96cp')

# Open the CSV file for writing
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Club Name', 'Description', 'Commitment Level', 'Categories', 'Image URL', 'Link'])

    # Loop through each club card and extract information
    for card in club_cards:
        # Extract club name
        name = card.find('h5').get_text(strip=True)
        
        # Extract description
        description = card.find('p').get_text(strip=True)
        
        # Extract commitment level and categories from chips
        chips = card.find_all('div', class_='MuiChip-root')
        commitment_level = chips[0].get_text(strip=True) if chips else 'Unknown'
        categories = ', '.join(chip.get_text(strip=True) for chip in chips[1:])  # Assuming the first chip is always commitment level
        
        # Find parent anchor tag for the link
        link_tag = card.find_parent('a')
        link = link_tag['href'] if link_tag else 'No link'
        
        # Find preceding sibling img tag for the image URL
        img_tag = link_tag.find('img') if link_tag else None
        image_url = img_tag['src'] if img_tag else 'No image'

        # Write the extracted information to the CSV
        writer.writerow([name, description, commitment_level, categories, image_url, link])

print(f"Data extracted and written to {output_file_path}")

