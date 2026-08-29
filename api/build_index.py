#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build word-to-file index for fast lookup
"""

import csv
import json
import os

def build_word_index(csv_file, output_dir, chunk_size=1000):
    """Build word-to-file index"""
    words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append(row['word'])
    
    words.sort(key=lambda w: w.lower())
    
    word_index = {}
    for i, word in enumerate(words):
        file_num = (i // chunk_size) + 1
        word_index[word.lower()] = file_num
    
    os.makedirs(output_dir, exist_ok=True)
    index_file = os.path.join(output_dir, 'word-index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(word_index, f, ensure_ascii=False)
    
    print(f"Created word-index.json with {len(word_index)} entries")
    return word_index

def main():
    csv_file = 'ecdict_traditional.csv'
    output_dir = 'api/dict'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    build_word_index(csv_file, output_dir)

if __name__ == '__main__':
    main()
