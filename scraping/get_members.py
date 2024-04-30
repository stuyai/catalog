import os
from bs4 import BeautifulSoup

def extract_member_names(directory):
    input_file_path = os.path.join(directory, 'members.txt')
    output_file_path = os.path.join(directory, 'member_name_list.txt')

    # Read the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <p> tags with the specific class for member names
    members = soup.find_all('p', class_='MuiTypography-root MuiTypography-body1 css-ekbb42')

    # Write member names to the output file, each on a new line
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for member in members:
            file.write(member.get_text().strip() + '\n')

    print(f"Member names extracted to {output_file_path}")

# Specify the path to the data directory
data_directory = './data'

# Iterate over each subdirectory in the data directory
for subdir in os.listdir(data_directory):
    subdir_path = os.path.join(data_directory, subdir)
    if os.path.isdir(subdir_path):
        extract_member_names(subdir_path)
