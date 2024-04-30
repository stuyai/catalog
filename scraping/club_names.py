from bs4 import BeautifulSoup

# Path to the HTML file
input_file_path = './data/catalog.txt'
# Path to the output text file
output_file_path = './data/club_names.txt'

# Read the HTML file
with open(input_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <h5> tags with the specific class
h5_tags = soup.find_all('h5', class_='MuiTypography-root MuiTypography-h5 MuiTypography-alignCenter MuiTypography-gutterBottom css-1qsk5k0')

# Open the output file and write each item on a new line
with open(output_file_path, 'w', encoding='utf-8') as file:
    for tag in h5_tags:
        file.write(tag.get_text() + '\n')

print(f"Data extracted and written to {output_file_path}")

