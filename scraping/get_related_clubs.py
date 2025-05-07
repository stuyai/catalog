#!/usr/bin/env python3
"""
related_clubs_top3.py

Three standout methods to find and debate "related" clubs at Stuyvesant:
 1. Content-Based (TF-IDF + Cosine)
 2. Semantic Embeddings (Sentence-BERT)
 3. Collaborative Filtering (Membership Overlap via SVD with Jaccard fallback)

Removes stop words for methods 1 & 2. Saves all results in JSON for later analysis.

Usage:
    python related_clubs_top3.py --data-dir ./data --top-k 3
"""
import os
import glob
import argparse
import json
import numpy as np

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from sklearn.decomposition import TruncatedSVD


def load_club_data(data_dir):
    club_names, club_texts, club_members = [], [], {}
    for path in glob.glob(os.path.join(data_dir, '*')):
        if not os.path.isdir(path): continue
        name = os.path.basename(path)
        club_names.append(name)
        # combine charter_text + main_info
        texts = []
        for fname in ('charter_text.txt','main_info.txt'):
            f = os.path.join(path, fname)
            if os.path.exists(f):
                texts.append(open(f, encoding='utf-8').read().strip())
        club_texts.append('\n'.join(texts))
        # load members
        members = set()
        member_file = os.path.join(path, 'member_name_list.txt')
        for line in open(member_file, encoding='utf-8') if os.path.exists(member_file) else []:
            nm=line.strip()
            if nm: members.add(nm)
        club_members[name]=members
    return club_names, club_texts, club_members


def content_similarity_tfidf(texts, names, top_k=3):
    """
    TF-IDF + Cosine Similarity
    - Removes English stop words.
    - Uses unigrams and bigrams.
    - Good for finding keyword-overlap relations.
    """
    # 1. Build TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9, ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform(texts)

    # 2. Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # 3. Gather top_k related clubs for each club
    results = {}
    for idx, club in enumerate(names):
        # List of (club_name, score) excluding itself
        club_scores = []
        for jdx, score in enumerate(similarity_matrix[idx]):
            if jdx == idx:
                continue
            club_scores.append((names[jdx], round(score, 4)))
        # Sort by descending score
        club_scores.sort(key=lambda x: x[1], reverse=True)
        # Keep only top_k
        results[club] = club_scores[:top_k]

    return results


def semantic_similarity_embeddings(texts, names, top_k=3, model_name='all-MPNet-base-v2'):
    cleaned=[' '.join([w for w in t.split() if w.lower() not in ENGLISH_STOP_WORDS]) for t in texts]
    model=SentenceTransformer(model_name)
    emb=model.encode(cleaned, convert_to_tensor=True)
    hits=util.semantic_search(emb, emb, top_k=top_k+1)
    out={}
    for i,club in enumerate(names):
        rel=[]
        for hit in hits[i]:
            j,score=hit['corpus_id'],hit['score']
            if j==i: continue
            rel.append((names[j],round(float(score),4)))
            if len(rel)>=top_k: break
        out[club]=rel
    return out

def collaborative_filtering_svd(members, names, top_k=3, n_components=5):
    """
    Collaborative Filtering via SVD with per-club Jaccard fallback.
    1. Build a binary student-by-club matrix.
    2. Perform truncated SVD to get latent club factors.
    3. Cosine similarity on factors.
    4. If SVD yields no signal for a club, compute Jaccard similarity instead.
    """
    # 1. Collect all unique students
    student_set = set()
    for member_list in members.values():
        for student in member_list:
            student_set.add(student)
    students = sorted(student_set)

    # 2. If not enough students, fallback for all clubs
    if len(students) < 2:
        print("Not enough students for SVD; returning empty results.")
        return {club: [] for club in names}

    # 3. Create index maps
    student_index = {student: i for i, student in enumerate(students)}
    club_index = {club: i for i, club in enumerate(names)}

    # 4. Build membership matrix R
    R = np.zeros((len(students), len(names)))
    for club, member_list in members.items():
        col = club_index[club]
        for student in member_list:
            row = student_index[student]
            R[row][col] = 1

    # 5. Determine number of SVD components
    components = min(n_components, len(students) - 1)
    if components < 1:
        return {club: [] for club in names}

    # 6. Compute latent factors for clubs
    svd = TruncatedSVD(n_components=components, random_state=0)
    club_factors = svd.fit_transform(R.T)

    # 7. Compute cosine similarity on latent factors
    similarity_matrix = cosine_similarity(club_factors)

    # 8. Gather results per club, no fallback
    results = {}
    for idx, club in enumerate(names):
        # Collect (club_name, score) excluding itself
        club_scores = []
        for jdx, score in enumerate(similarity_matrix[idx]):
            if jdx == idx:
                continue
            club_scores.append((names[jdx], round(score, 4)))
        # Sort and take top_k
        club_scores.sort(key=lambda x: x[1], reverse=True)
        top_related = club_scores[:top_k]

        results[club] = top_related

    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data-dir', default='./data')
    p.add_argument('--top-k', type=int, default=3)
    args=p.parse_args()

    names,texts,members=load_club_data(args.data_dir)
    m1=content_similarity_tfidf(texts,names,args.top_k)
    m2=semantic_similarity_embeddings(texts,names,args.top_k)
    m3=collaborative_filtering_svd(members,names,args.top_k)

    # print with scores
    print("\n1) Content-Based (TF-IDF):")
    for c in names:
        entries=[f"'{nm}' ({sc})" for nm,sc in m1.get(c,[])]
        print(f"  {c}: {', '.join(entries)}")

    print("\n2) Semantic Embeddings:")
    for c in names:
        entries=[f"'{nm}' ({sc})" for nm,sc in m2.get(c,[])]
        print(f"  {c}: {', '.join(entries)}")

    print("\n3) Collaborative Filtering (SVD):")
    for c in names:
        entries=[f"'{nm}' ({sc})" for nm,sc in m3.get(c,[])]
        print(f"  {c}: {', '.join(entries)}")

    # final comparison with scores
    print("\nComparison per club:")
    for c in names:
        tf_entries = [f"'{nm}' ({sc})" for nm, sc in m1.get(c, [])]
        sb_entries = [f"'{nm}' ({sc})" for nm, sc in m2.get(c, [])]
        sv_entries = [f"'{nm}' ({sc})" for nm, sc in m3.get(c, [])]
        print(f"\n{c}:\n  TF-IDF: {', '.join(tf_entries)}\n  Embeddings: {', '.join(sb_entries)}\n  SVD: {', '.join(sv_entries)}")

    # save results
    results={'tfidf':m1,'embeddings':m2,'svd':m3}
    with open('related_clubs_results.json','w',encoding='utf-8') as f:
        json.dump(results,f, indent=2)
    print("\nSaved all results to related_clubs_results.json")

if __name__=='__main__':
    main()
