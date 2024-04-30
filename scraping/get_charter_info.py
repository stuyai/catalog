import os
from bs4 import BeautifulSoup

def extract_charter_info(directory):
    input_file_path = os.path.join(directory, 'charter.txt')
    output_file_path = os.path.join(directory, 'charter_text.txt')

    # Read the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty string to store the extracted information
    charter_info = ""

    # Define sections to extract based on heading names
    sections = ["Mission Statement: ", "What days does this organization meet?", 
                "What is the meeting schedule?", "What is the purpose of this activity?", 
                "How does this activity benefit Stuyvesant?", "How does this activity appoint leaders?", 
                "What makes this activity unique?"]

    # Extract the information for each section
    for section in sections:
        heading = soup.find('h5', text=section)
        if heading:
            content = heading.find_next_sibling('p').get_text(strip=True)
            if section != sections[0]:
                charter_info += f"{section}:\n{content}\n\n"
            else:
                charter_info += f"Mission Statement:\n{content}\n\n"
        else:
            charter_info += f"{section}:\nInformation not available.\n\n"

    # Write the extracted information to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(charter_info)

    print(f"Charter info extracted to {output_file_path}")

# Specify the path to the data directory
data_directory = './data'

# Iterate over each subdirectory in the data directory
for subdir in os.listdir(data_directory):
    subdir_path = os.path.join(data_directory, subdir)
    if os.path.isdir(subdir_path):
        extract_charter_info(subdir_path)
