import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def combine_texts_from_files(directory, filenames):
    combined_text = ''
    for filename in filenames:
        try:
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                combined_text += file.read() + ' '
        except FileNotFoundError:
            print(f"File not found: {os.path.join(directory, filename)}")
    return combined_text.strip()

def get_club_texts(data_directory):
    club_texts = []
    club_names = []
    filenames = ['charter_text.txt', 'main_info.txt', 'member_name_list.txt']

    for subdir in os.listdir(data_directory):
        subdir_path = os.path.join(data_directory, subdir)
        if os.path.isdir(subdir_path):
            combined_text = combine_texts_from_files(subdir_path, filenames)
            club_texts.append(combined_text)
            club_names.append(subdir)

    return club_texts, club_names

def find_top_related_clubs(club_texts, club_names):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(club_texts)
    cosine_sim = cosine_similarity(tfidf_matrix)

    related_clubs = {}

    for idx, name in enumerate(club_names):
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_clubs = []
        count = 0
        for i, score in sim_scores:
            if i != idx and count < 3:
                top_clubs.append((club_names[i], score))
                count += 1
        related_clubs[name] = top_clubs

    return related_clubs

# Path to the data directory
data_directory = './data'
club_texts, club_names = get_club_texts(data_directory)

# Get the top related clubs for each club
related_clubs = find_top_related_clubs(club_texts, club_names)

# Display the results
for club, relations in related_clubs.items():
    print(f"Top related clubs for {club}:")
    for related_club, score in relations:
        print(f"  {related_club} with similarity score: {score:.4f}")
    print("")
