import os
from bs4 import BeautifulSoup

def extract_main_info(directory):
    input_file_path = os.path.join(directory, 'main.txt')
    output_file_path = os.path.join(directory, 'main_info.txt')

    # Read the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract mission
    mission_tag = soup.find('h5', text='Mission:')
    mission = mission_tag.find_next('p').get_text(strip=True) if mission_tag else "Mission information not available"

    # Extract meeting schedule
    meeting_schedule_tag = soup.find('h5', text='Meeting Schedule:')
    meeting_schedule = meeting_schedule_tag.find_next('p').get_text(strip=True) if meeting_schedule_tag else "Meeting schedule not available"

    # Extract leaders
    leaders_tag = soup.find('h5', text='Leaders')
    if leaders_tag:
        leaders_list = leaders_tag.find_next('ul')
        leaders = [leader.find('p').get_text(strip=True) for leader in leaders_list.find_all('div', role='button')]
    else:
        leaders = ["No leaders listed"]

    # Extract related clubs
    related_clubs_tag = soup.find('h5', text='Related Clubs')
    if related_clubs_tag:
        related_clubs_list = related_clubs_tag.find_next('ul')
        related_clubs = [club.find('p').get_text(strip=True) for club in related_clubs_list.find_all('a')]
    else:
        related_clubs = ["No related clubs listed"]

    # Write extracted information to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("Mission:\n" + mission + "\n\n")
        file.write("Meeting Schedule:\n" + meeting_schedule + "\n\n")
        file.write("Leaders:\n" + "\n".join(leaders) + "\n\n")
        file.write("Related Clubs:\n" + "\n".join(related_clubs) + "\n")

    print(f"Info extracted to {output_file_path}")

# Specify the path to the data directory
data_directory = './data'

# Iterate over each subdirectory in the data directory
for subdir in os.listdir(data_directory):
    subdir_path = os.path.join(data_directory, subdir)
    if os.path.isdir(subdir_path):
        extract_main_info(subdir_path)
