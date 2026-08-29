#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create search optimization metadata
"""

import csv
import json
import os

def create_search_meta(csv_file, output_dir):
    """Create search metadata"""
    letter_counts = {}
    total_words = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word']
            first_char = word[0].lower() if word else ''
            
            if first_char.isalpha():
                group = first_char
            elif first_char.isdigit():
                group = '0-9'
            else:
                group = 'special'
            
            letter_counts[group] = letter_counts.get(group, 0) + 1
            total_words += 1
    
    meta = {
        'total_words': total_words,
        'letter_counts': letter_counts,
        'search_tips': {
            'exact_lookup': 'Use word-index.json for O(1) lookup',
            'prefix_search': 'Use letter-based files (a.json, b.json, etc.)',
            'fuzzy_search': 'Scan all letter-based files'
        }
    }
    
    os.makedirs(output_dir, exist_ok=True)
    meta_file = os.path.join(output_dir, 'search.json')
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"Created search.json with metadata for {total_words} words")
    return meta

def main():
    csv_file = 'ecdict_traditional.csv'
    output_dir = 'api/dict'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    create_search_meta(csv_file, output_dir)

if __name__ == '__main__':
    main()
