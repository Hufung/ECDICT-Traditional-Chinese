# ECDICT Traditional Chinese - Quick Start Guide

## 🚀 Quick Start

### 1. Basic Word Lookup

```python
import csv

# Search for a word
def lookup_word(word):
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['word'].lower() == word.lower():
                return row
    return None

# Example
word = lookup_word('hello')
print(f"Translation: {word['translation']}")
```

### 2. Using the Python Module

```python
from stardict_traditional import DictCsv

# Initialize dictionary
dict_csv = DictCsv('ecdict_traditional.csv')

# Query a word
word_data = dict_csv.query('hello')
print(word_data['translation'])
```

### 3. Find Exam Words

```python
import csv

def get_exam_words(exam_type):
    words = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if exam_type in row['tag']:
                words.append(row['word'])
    return words

# Get CET4 words
cet4_words = get_exam_words('cet4')
print(f"CET4 words: {len(cet4_words)}")
```

## 📊 Common Tasks

### Task 1: Create Flashcards
```python
import csv

def create_flashcards(exam_type, count=10):
    flashcards = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if exam_type in row['tag'] and len(flashcards) < count:
                flashcards.append({
                    'front': row['word'],
                    'back': row['translation'],
                    'phonetic': row['phonetic']
                })
    return flashcards

# Create 10 CET4 flashcards
flashcards = create_flashcards('cet4', 10)
for card in flashcards:
    print(f"{card['front']} ({card['phonetic']}): {card['back']}")
```

### Task 2: Word Frequency Analysis
```python
import csv

def analyze_frequency():
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        words = []
        for row in reader:
            if row['bnc'] and row['bnc'].isdigit():
                words.append({
                    'word': row['word'],
                    'bnc': int(row['bnc']),
                    'translation': row['translation'][:50]
                })
    
    # Sort by BNC rank
    words.sort(key=lambda x: x['bnc'])
    
    print("Top 10 most frequent words (BNC):")
    for i, word in enumerate(words[:10], 1):
        print(f"{i}. {word['word']} (#{word['bnc']}): {word['translation']}")

analyze_frequency()
```

### Task 3: Export to Anki
```python
import csv

def export_to_anki(exam_type, filename='anki_export.txt'):
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as infile, \
         open(filename, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            if exam_type in row['tag']:
                # Anki format: front<tab>back
                front = row['word']
                back = f"{row['phonetic']}<br>{row['translation']}"
                outfile.write(f"{front}\t{back}\n")
    
    print(f"Exported to {filename}")

export_to_anki('cet4')
```

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/Hufung/ECDICT-Traditional-Chinese.git
cd ECDICT-Traditional-Chinese
```

2. No additional dependencies required for basic CSV usage.

3. For advanced features (SQLite, MySQL):
```bash
pip install opencc-python-reimplemented  # For Traditional Chinese conversion
```

## 📁 File Usage

| File | Description | Use Case |
|------|-------------|----------|
| `ecdict_traditional.csv` | Main dictionary (770K words) | Full dictionary search |
| `ecdict.mini_traditional.csv` | Mini dictionary (53 words) | Testing/development |
| `stardict_traditional.py` | Python module | Programmatic access |
| `resemble_traditional.txt` | Word discrimination | Learning differences |

## 🎯 Common Patterns

### Pattern 1: Batch Processing
```python
import csv

def batch_process(words):
    results = {}
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['word'].lower() in [w.lower() for w in words]:
                results[row['word']] = row
    return results

# Process multiple words at once
words = ['hello', 'world', 'good', 'bad']
results = batch_process(words)
```

### Pattern 2: Filter and Sort
```python
import csv

def filter_words(min_collins=0, max_bnc=10000):
    filtered = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['collins'] and int(row['collins']) >= min_collins:
                if row['bnc'] and row['bnc'].isdigit():
                    if int(row['bnc']) <= max_bnc:
                        filtered.append(row)
    
    return sorted(filtered, key=lambda x: int(x['bnc']))

# Get high-quality words
high_quality = filter_words(min_collins=4, max_bnc=1000)
print(f"Found {len(high_quality)} words")
```

## 📈 Performance Tips

1. **For large datasets**: Convert CSV to SQLite
2. **Memory efficiency**: Process CSV in chunks
3. **Batch operations**: Use `query_batch()` for multiple lookups
4. **Caching**: Cache frequently accessed words

## 🆘 Troubleshooting

**Issue: File not found**
```python
import os
print(os.path.exists('ecdict_traditional.csv'))  # Should be True
```

**Issue: Encoding errors**
```python
# Always use UTF-8 encoding
with open('file.csv', 'r', encoding='utf-8') as f:
    # ...
```

**Issue: Memory errors**
```python
# Process in chunks
chunk_size = 10000
with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    chunk = []
    for i, row in enumerate(reader):
        chunk.append(row)
        if i % chunk_size == 0:
            # Process chunk
            process_chunk(chunk)
            chunk = []
```

## 📚 Learn More

- Read `USAGE_GUIDE.md` for comprehensive documentation
- Check `CONVERSION_SUMMARY.md` for conversion details
- See `README_traditional.md` for project overview