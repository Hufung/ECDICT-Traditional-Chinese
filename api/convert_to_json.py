#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert ECDICT Traditional Chinese CSV to JSON format for API usage
"""

import csv
import json
import os
import math

def csv_to_json(csv_file, output_dir, chunk_size=1000):
    """Convert CSV to multiple JSON files"""
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        chunk_num = 1
        chunk = []
        
        for row in reader:
            # Clean up the data
            clean_row = {}
            for key, value in row.items():
                clean_row[key] = value if value else ''
            
            chunk.append(clean_row)
            
            if len(chunk) >= chunk_size:
                # Write chunk to JSON file
                filename = os.path.join(output_dir, f'{chunk_num:04d}.json')
                with open(filename, 'w', encoding='utf-8') as jsonf:
                    json.dump(chunk, jsonf, ensure_ascii=False, indent=2)
                
                print(f"Created {filename} with {len(chunk)} words")
                chunk_num += 1
                chunk = []
        
        # Write remaining words
        if chunk:
            filename = os.path.join(output_dir, f'{chunk_num:04d}.json')
            with open(filename, 'w', encoding='utf-8') as jsonf:
                json.dump(chunk, jsonf, ensure_ascii=False, indent=2)
            print(f"Created {filename} with {len(chunk)} words")
    
    return chunk_num - 1

def create_index_file(output_dir, total_files):
    """Create index file with metadata"""
    index = {
        "name": "ECDICT Traditional Chinese",
        "version": "1.0.0",
        "description": "English-Chinese Dictionary Database (Traditional Chinese)",
        "total_files": total_files,
        "file_pattern": "{chunk_num:04d}.json",
        "base_url": "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict"
    }
    
    index_file = os.path.join(output_dir, "index.json")
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"Created index file with {total_files} chunks")

def create_vocabulary_lists(csv_file, output_dir):
    """Create vocabulary lists for different exam levels"""
    vocab_lists = {
        "cet4": [],
        "cet6": [],
        "gaokao": [],
        "zhongkao": [],
        "collins_3star": [],
        "collins_4star": [],
        "collins_5star": [],
        "oxford_3000": []
    }
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word']
            
            # CET4
            if 'cet4' in row['tag']:
                vocab_lists['cet4'].append(word)
            
            # CET6
            if 'cet6' in row['tag']:
                vocab_lists['cet6'].append(word)
            
            # Gaokao
            if 'gk' in row['tag']:
                vocab_lists['gaokao'].append(word)
            
            # Zhongkao
            if 'zk' in row['tag']:
                vocab_lists['zhongkao'].append(word)
            
            # Collins ratings
            if row['collins']:
                collins = int(row['collins'])
                if collins >= 3:
                    vocab_lists['collins_3star'].append(word)
                if collins >= 4:
                    vocab_lists['collins_4star'].append(word)
                if collins >= 5:
                    vocab_lists['collins_5star'].append(word)
            
            # Oxford 3000
            if row['oxford'] == '1':
                vocab_lists['oxford_3000'].append(word)
    
    # Save vocabulary lists
    os.makedirs(output_dir, exist_ok=True)
    for name, words in vocab_lists.items():
        filename = os.path.join(output_dir, f"{name}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "name": name,
                "count": len(words),
                "words": words
            }, f, ensure_ascii=False, indent=2)
        print(f"Created {filename} with {len(words)} words")

def main():
    # Directories
    api_dir = "api"
    dict_dir = os.path.join(api_dir, "dict")
    vocab_dir = os.path.join(api_dir, "vocabulary")
    
    # Convert CSV to JSON
    print("Converting CSV to JSON format...")
    csv_file = "ecdict_traditional.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    total_files = csv_to_json(csv_file, dict_dir, chunk_size=1000)
    create_index_file(dict_dir, total_files)
    
    # Create vocabulary lists
    print("\nCreating vocabulary lists...")
    create_vocabulary_lists(csv_file, vocab_dir)
    
    print("\nConversion completed!")
    print(f"Total JSON files: {total_files}")
    print(f"API directory structure created in: {api_dir}/")

if __name__ == "__main__":
    main()