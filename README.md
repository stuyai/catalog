# StuyActivities Catalog Scraper

This project is a Python-based web scraper for the StuyActivities website. It extracts information about various clubs and activities, and formats the data for further use.

## Project Structure

The main scripts for the project are located in the `scraping/` directory:

- `club_names.py`: This script extracts the names of clubs from an HTML file and writes them to a text file.

- `get_charter_info.py`: This script reads the 'charter.txt' file from each club's directory, extracts specific sections such as the mission statement and meeting schedule using BeautifulSoup, and writes this information to a new 'charter_text.txt' file in the same directory.

- `get_club_info.py`: This script reads an HTML file containing club information, extracts details such as the club name, description, commitment level, categories, image URL, and link for each club using BeautifulSoup, and writes this information to a CSV file.

- `get_main_info.py`: This script reads the 'main.txt' file from each club's directory, extracts the mission, meeting schedule, leaders, and related clubs using BeautifulSoup, and writes this information to a new 'main_info.txt' file in the same directory.

- `get_members.py`: This script reads the 'members.txt' file from each club's directory, extracts the names of the members using BeautifulSoup, and writes these names to a new 'member_name_list.txt' file in the same directory.

- `get_related_clubs.py`: This script uses TF-IDF vectorization and cosine similarity to find and print the top three most related clubs for each club based on the combined text of their charter, main info, and member list.

- `main.py`: This script uses Selenium and BeautifulSoup to navigate to the StuyActivities website, waits for the page to load completely, and then prints the prettified HTML of the page.

- `scrape_all.py`: This script uses Selenium and BeautifulSoup to scrape club information from the StuyActivities website and saves the main page, charter, and members page HTML for each club into separate text files.

The `data/` directory contains the scraped data for each club.

## How to Run

1. Install the required Python packages; it's also recommended to create a venv:


```sh
python -m venv venv # Optional
source venv/bin/activate #Optional

pip install -r requirements.txt
```

2. Run the main script:

```sh
python main.py
```

## Data Format
The data for each club is stored in a separate directory under data/. Each directory contains the following files:

`main.txt`: The raw HTML of the club's main page

`main_info.txt`: Extracted information from the main page, including the club's mission, meeting schedule, leaders, and related clubs

`charter.txt`: The raw HTML of the club's charter page

`charter_info.txt`: Extracted information from the charter page, including the club's mission statement, meeting schedule, purpose, benefits to Stuyvesant, leadership appointment process, and unique qualities
