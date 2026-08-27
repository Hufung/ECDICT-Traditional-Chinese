#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced usage examples for ECDICT Traditional Chinese Version
"""

import csv
import json
from collections import defaultdict

def analyze_dictionary_stats(csv_file='ecdict_traditional.csv'):
    """Analyze dictionary statistics"""
    stats = {
        'total_words': 0,
        'exam_words': defaultdict(int),
        'collins_ratings': defaultdict(int),
        'oxford_words': 0,
        'pos_distribution': defaultdict(int),
        'exchange_words': 0
    }
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats['total_words'] += 1
            
            # Exam tags
            if row['tag']:
                tags = row['tag'].split()
                for tag in tags:
                    stats['exam_words'][tag] += 1
            
            # Collins ratings
            if row['collins']:
                stats['collins_ratings'][row['collins']] += 1
            
            # Oxford words
            if row['oxford'] == '1':
                stats['oxford_words'] += 1
            
            # Part of speech
            if row['pos']:
                pos_list = row['pos'].split('/')
                for pos in pos_list:
                    if ':' in pos:
                        pos_type = pos.split(':')[0]
                        stats['pos_distribution'][pos_type] += 1
            
            # Word forms
            if row['exchange']:
                stats['exchange_words'] += 1
    
    return stats

def create_word_frequency_ranking(csv_file='ecdict_traditional.csv', top_n=100):
    """Create word frequency ranking based on BNC and contemporary corpus"""
    words_bnc = []
    words_contemporary = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['bnc'] and row['bnc'].isdigit():
                words_bnc.append({
                    'word': row['word'],
                    'rank': int(row['bnc']),
                    'translation': row['translation'][:50]
                })
            
            if row['frq'] and row['frq'].isdigit():
                words_contemporary.append({
                    'word': row['word'],
                    'rank': int(row['frq']),
                    'translation': row['translation'][:50]
                })
    
    # Sort by rank
    words_bnc.sort(key=lambda x: x['rank'])
    words_contemporary.sort(key=lambda x: x['rank'])
    
    return {
        'bnc_top': words_bnc[:top_n],
        'contemporary_top': words_contemporary[:top_n]
    }

def find_words_by_pattern(pattern, csv_file='ecdict_traditional.csv'):
    """Find words matching a pattern (simple regex)"""
    import re
    
    matching_words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if re.search(pattern, row['word'], re.IGNORECASE):
                matching_words.append(row)
    
    return matching_words

def create_vocabulary_list(exam_type, min_collins=0, csv_file='ecdict_traditional.csv'):
    """Create a vocabulary list for a specific exam"""
    vocab_list = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if exam_type in row['tag']:
                if min_collins > 0 and row['collins']:
                    if int(row['collins']) < min_collins:
                        continue
                
                vocab_list.append({
                    'word': row['word'],
                    'phonetic': row['phonetic'],
                    'translation': row['translation'],
                    'collins': row['collins'],
                    'bnc': row['bnc']
                })
    
    return vocab_list

def export_to_json(data, filename):
    """Export data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data exported to {filename}")

def main():
    print("Advanced ECDICT Usage Examples")
    print("=" * 60)
    
    # Example 1: Dictionary Statistics
    print("\n1. Dictionary Statistics")
    print("-" * 40)
    
    stats = analyze_dictionary_stats()
    print(f"Total words: {stats['total_words']}")
    print(f"Words with word forms: {stats['exchange_words']}")
    print(f"Oxford 3000 words: {stats['oxford_words']}")
    
    print("\nExam word counts:")
    for exam, count in sorted(stats['exam_words'].items()):
        print(f"  {exam}: {count}")
    
    print("\nCollins rating distribution:")
    for rating, count in sorted(stats['collins_ratings'].items()):
        print(f"  {rating} stars: {count}")
    
    # Example 2: Word Frequency Ranking
    print("\n2. Word Frequency Ranking")
    print("-" * 40)
    
    ranking = create_word_frequency_ranking(top_n=20)
    
    print("Top 20 BNC words:")
    for i, word in enumerate(ranking['bnc_top'][:20], 1):
        print(f"{i:2d}. {word['word']} (BNC #{word['rank']}): {word['translation']}")
    
    print("\nTop 20 Contemporary words:")
    for i, word in enumerate(ranking['contemporary_top'][:20], 1):
        print(f"{i:2d}. {word['word']} (FRQ #{word['rank']}): {word['translation']}")
    
    # Example 3: Pattern Matching
    print("\n3. Pattern Matching")
    print("-" * 40)
    
    # Find words starting with "un"
    un_words = find_words_by_pattern(r'^un')
    print(f"Words starting with 'un': {len(un_words)}")
    print("First 10 examples:")
    for word in un_words[:10]:
        print(f"  {word['word']}: {word['translation'][:50]}")
    
    # Find words ending with "tion"
    tion_words = find_words_by_pattern(r'tion$')
    print(f"\nWords ending with 'tion': {len(tion_words)}")
    print("First 10 examples:")
    for word in tion_words[:10]:
        print(f"  {word['word']}: {word['translation'][:50]}")
    
    # Example 4: Vocabulary List
    print("\n4. Vocabulary List Creation")
    print("-" * 40)
    
    # Create CET4 vocabulary list with 4+ Collins stars
    cet4_vocab = create_vocabulary_list('cet4', min_collins=4)
    print(f"CET4 words with 4+ Collins stars: {len(cet4_vocab)}")
    print("First 10 examples:")
    for word in cet4_vocab[:10]:
        print(f"  {word['word']}: {word['translation'][:50]}")
    
    # Example 5: Export to JSON
    print("\n5. Export to JSON")
    print("-" * 40)
    
    # Export top 100 BNC words to JSON
    export_data = {
        'bnc_top_100': ranking['bnc_top'][:100],
        'contemporary_top_100': ranking['contemporary_top'][:100]
    }
    
    export_to_json(export_data, 'word_frequency_ranking.json')
    
    print("\n" + "=" * 60)
    print("All examples completed!")

if __name__ == "__main__":
    main()