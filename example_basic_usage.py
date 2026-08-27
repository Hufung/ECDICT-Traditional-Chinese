#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic usage examples for ECDICT Traditional Chinese Version
"""

import csv
import sys
import os

def search_word_csv(word, csv_file='ecdict_traditional.csv'):
    """Search for a word in CSV file"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['word'].lower() == word.lower():
                return row
    return None

def search_word_module(word):
    """Search for a word using the stardict module"""
    try:
        from stardict_traditional import DictCsv
        dict_csv = DictCsv('ecdict_traditional.csv')
        return dict_csv.query(word)
    except ImportError:
        print("Error: stardict_traditional module not found")
        return None

def display_word_info(word_data):
    """Display word information in a formatted way"""
    if not word_data:
        print(f"Word not found")
        return
    
    print(f"=" * 60)
    print(f"Word: {word_data['word']}")
    print(f"Phonetic: {word_data['phonetic']}")
    print(f"Definition: {word_data['definition']}")
    print(f"Translation: {word_data['translation']}")
    print(f"Part of Speech: {word_data['pos']}")
    print(f"Collins Rating: {word_data['collins']} stars")
    print(f"Oxford 3000: {'Yes' if word_data['oxford'] == '1' else 'No'}")
    print(f"BNC Frequency: {word_data['bnc']}")
    print(f"Contemporary Frequency: {word_data['frq']}")
    
    if word_data['exchange']:
        print(f"Word Forms: {word_data['exchange']}")
    
    print(f"=" * 60)

def get_exam_words(exam_type, csv_file='ecdict_traditional.csv'):
    """Get words for a specific exam type"""
    words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if exam_type in row['tag']:
                words.append(row['word'])
    return words

def main():
    # Example 1: Search for a word
    print("Example 1: Search for a word")
    print("-" * 40)
    
    # Using CSV directly
    word_data = search_word_csv('hello')
    print("Using CSV directly:")
    display_word_info(word_data)
    
    print("\n" + "=" * 60 + "\n")
    
    # Using module (if available)
    word_data = search_word_module('hello')
    print("Using stardict module:")
    display_word_info(word_data)
    
    print("\n" + "=" * 60 + "\n")
    
    # Example 2: Get exam words
    print("Example 2: Get exam words")
    print("-" * 40)
    
    cet4_words = get_exam_words('cet4')
    print(f"CET4 words count: {len(cet4_words)}")
    print(f"First 10 CET4 words: {cet4_words[:10]}")
    
    cet6_words = get_exam_words('cet6')
    print(f"CET6 words count: {len(cet6_words)}")
    print(f"First 10 CET6 words: {cet6_words[:10]}")
    
    print("\n" + "=" * 60 + "\n")
    
    # Example 3: Search multiple words
    print("Example 3: Search multiple words")
    print("-" * 40)
    
    words_to_search = ['hello', 'world', 'good', 'bad', 'happy']
    for word in words_to_search:
        word_data = search_word_csv(word)
        if word_data:
            print(f"{word}: {word_data['translation'][:50]}...")
        else:
            print(f"{word}: Not found")

if __name__ == "__main__":
    main()