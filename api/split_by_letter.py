#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Split dictionary files by first letter
"""

import csv
import json
import os

def split_by_letter(csv_file, output_dir):
    """Split words by first letter"""
    letter_groups = {}
    
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
            
            if group not in letter_groups:
                letter_groups[group] = []
            letter_groups[group].append(row)
    
    for group in letter_groups:
        letter_groups[group].sort(key=lambda x: x['word'].lower())
    
    os.makedirs(output_dir, exist_ok=True)
    for group, words in letter_groups.items():
        filename = os.path.join(output_dir, f'{group}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        print(f"Created {filename} with {len(words)} words")
    
    return letter_groups

def main():
    csv_file = 'ecdict_traditional.csv'
    output_dir = 'api/dict'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    split_by_letter(csv_file, output_dir)

if __name__ == '__main__':
    main()
