# ECDICT Traditional Chinese Version - Usage Guide

This guide explains how to use the Traditional Chinese version of ECDICT (English-Chinese Dictionary Database).

## 📁 File Structure

```
ECDICT/
├── README_traditional.md          # Documentation in Traditional Chinese
├── stardict_traditional.py        # Python module for dictionary operations
├── ecdict_traditional.csv         # Main dictionary database (770,611 entries)
├── ecdict.mini_traditional.csv    # Mini dictionary database (53 entries)
├── resemble_traditional.txt       # Word discrimination/explanation file
├── del_bfz_traditional.py         # Dictionary cleanup utility
├── dictutils_traditional.py       # Dictionary utility functions
├── linguist_traditional.py        # Linguistic processing utilities
└── CONVERSION_SUMMARY.md          # Conversion documentation
```

## 🔤 CSV Files Usage

### 1. Basic CSV Structure
The CSV files contain the following columns:
- `word` - English word
- `phonetic` - Phonetic transcription (IPA)
- `definition` - English definition
- `translation` - Chinese translation (Traditional Chinese)
- `pos` - Part of speech (e.g., n:46/v:54)
- `collins` - Collins star rating (1-5)
- `oxford` - Oxford 3000 core vocabulary (1=yes, 0=no)
- `tag` - Exam tags (zk/中考, gk/高考, cet4/四级, etc.)
- `bnc` - BNC corpus frequency rank
- `frq` - Contemporary corpus frequency rank
- `exchange` - Word forms (tenses, plurals, etc.)
- `detail` - JSON extension info (example sentences)
- `audio` - Audio URL (to be added)

### 2. Reading CSV Files

#### Using Python:
```python
import csv

# Read the Traditional Chinese dictionary
with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Word: {row['word']}")
        print(f"Phonetic: {row['phonetic']}")
        print(f"Definition: {row['definition']}")
        print(f"Translation: {row['translation']}")
        print(f"Collins: {row['collins']}")
        print("---")
```

#### Using Excel:
1. Open Excel
2. Go to Data → From Text/CSV
3. Select `ecdict_traditional.csv`
4. Choose "Delimited" and select "Comma"
5. Set encoding to "UTF-8"
6. Click "Load"

### 3. Searching for Words

#### Simple Search:
```python
import csv

def search_word(word):
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['word'].lower() == word.lower():
                return row
    return None

# Example usage
result = search_word('hello')
if result:
    print(f"Word: {result['word']}")
    print(f"Translation: {result['translation']}")
```

#### Advanced Search with Filters:
```python
import csv

def search_with_filters(exam_type=None, min_collins=None):
    results = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if exam_type and exam_type not in row['tag']:
                continue
            if min_collins and int(row['collins']) < min_collins:
                continue
            results.append(row)
    return results

# Example: Find CET4 words with 4+ Collins stars
cet4_words = search_with_filters(exam_type='cet4', min_collins=4)
```

## 🐍 Python Module Usage

### 1. Using DictCsv Class (CSV Files)

```python
from stardict_traditional import DictCsv

# Initialize dictionary
dict_csv = DictCsv('ecdict_traditional.csv')

# Query a word
word_data = dict_csv.query('hello')
if word_data:
    print(f"Word: {word_data['word']}")
    print(f"Translation: {word_data['translation']}")
    print(f"Definition: {word_data['definition']}")

# Get word count
total_words = dict_csv.count()
print(f"Total words: {total_words}")

# Match similar words
similar_words = dict_csv.match('helo', 5)  # Find 5 words similar to 'helo'
for word in similar_words:
    print(f"Similar: {word['word']}")
```

### 2. Using StarDict Class (SQLite Database)

First, convert CSV to SQLite:
```python
from stardict_traditional import StarDict, DictCsv

# Create SQLite database from CSV
csv_dict = DictCsv('ecdict_traditional.csv')
sqlite_dict = StarDict('ecdict_traditional.db')

# Copy data from CSV to SQLite
for word in csv_dict:
    data = csv_dict.query(word)
    sqlite_dict.register(word, data)

sqlite_dict.commit()
```

Then use SQLite database:
```python
from stardict_traditional import StarDict

# Initialize SQLite dictionary
dict_sqlite = StarDict('ecdict_traditional.db')

# Query words
word_data = dict_sqlite.query('hello')

# Batch query
words = ['hello', 'world', 'good']
results = dict_sqlite.query_batch(words)

# Iterate through all words
for word in dict_sqlite:
    print(word)
```

### 3. Using DictMySQL Class (MySQL Database)

```python
from stardict_traditional import DictMySQL

# Initialize MySQL dictionary
dict_mysql = DictMySQL(
    host='localhost',
    user='username',
    password='password',
    database='ecdict'
)

# Query words
word_data = dict_mysql.query('hello')
```

## 📊 Word Form Information (Exchange Field)

The `exchange` field contains word form variations:
- `p` - Past tense (e.g., walked)
- `d` - Past participle (e.g., walked)
- `i` - Present participle (e.g., walking)
- `3` - Third person singular (e.g., walks)
- `r` - Comparative (e.g., bigger)
- `t` - Superlative (e.g., biggest)
- `s` - Plural (e.g., cats)
- `0` - Lemma (base form)
- `1` - Lemma form type

Example for "perceive":
```
d:perceived/p:perceived/3:perceives/i:perceiving
```

## 🔍 Search Examples

### 1. Find Words by Exam Type
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

### 2. Find High-Frequency Words
```python
import csv

def get_high_frequency_words(limit=100):
    words = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['bnc'] and int(row['bnc']) <= limit:
                words.append({
                    'word': row['word'],
                    'bnc_rank': row['bnc'],
                    'translation': row['translation']
                })
    return sorted(words, key=lambda x: int(x['bnc_rank']))

# Get top 100 BNC words
top_words = get_high_frequency_words(100)
for word in top_words[:10]:
    print(f"{word['word']} (BNC #{word['bnc_rank']}): {word['translation']}")
```

### 3. Find Words by Collins Rating
```python
import csv

def get_collins_words(min_stars=4):
    words = []
    with open('ecdict_traditional.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['collins'] and int(row['collins']) >= min_stars:
                words.append(row)
    return words

# Get 5-star Collins words
five_star_words = get_collins_words(5)
print(f"5-star Collins words: {len(five_star_words)}")
```

## 🛠️ Utility Functions

### 1. Word Stripping
```python
from stardict_traditional import stripword

# Remove non-alphanumeric characters and convert to lowercase
clean_word = stripword("hello-world!")
print(clean_word)  # Output: helloworld
```

### 2. Word Matching
```python
from stardict_traditional import DictCsv

dict_csv = DictCsv('ecdict_traditional.csv')

# Find similar words
similar = dict_csv.match('helo', 5, fuzzy=True)
for word in similar:
    print(f"Similar: {word['word']}")
```

## 📈 Performance Tips

1. **For large datasets**: Convert CSV to SQLite for better performance
2. **Batch queries**: Use `query_batch()` for multiple word lookups
3. **Indexing**: SQLite automatically creates indexes for faster queries
4. **Memory usage**: CSV loads entire file into memory; SQLite uses disk storage

## 🔧 Troubleshooting

### Common Issues:

1. **Encoding problems**: Always use UTF-8 encoding
   ```python
   with open('file.csv', 'r', encoding='utf-8') as f:
       # ...
   ```

2. **Large file handling**: Use SQLite for files > 10MB
   ```python
   # Convert CSV to SQLite first
   from stardict_traditional import DictCsv, StarDict
   csv_dict = DictCsv('ecdict_traditional.csv')
   sqlite_dict = StarDict('ecdict.db')
   # ... copy data
   ```

3. **Memory errors**: Process CSV in chunks
   ```python
   import pandas as pd
   
   # Read in chunks
   chunks = pd.read_csv('ecdict_traditional.csv', chunksize=10000)
   for chunk in chunks:
       # Process each chunk
       pass
   ```

## 📚 Additional Resources

- Original ECDICT repository: https://github.com/skywind3000/ECDICT
- Traditional Chinese version: https://github.com/Hufung/ECDICT-Traditional-Chinese
- API version with fast search: https://github.com/Hufung/ECDICT-Traditional-Chinese/tree/main/api
- Documentation: README_traditional.md
- Conversion notes: CONVERSION_SUMMARY.md

## 🚀 API Version (Fast Search)

The API version provides fast search capabilities with O(1) lookup time.

### Fast Exact Lookup

```javascript
// JavaScript - Fast exact lookup
async function getWordFast(word) {
    // Step 1: Fetch index (cache this!)
    const indexRes = await fetch('https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/word-index.json');
    const wordIndex = await indexRes.json();
    
    // Step 2: Get file number from index
    const fileNum = wordIndex[word.toLowerCase()];
    if (!fileNum) return null;
    
    // Step 3: Fetch only that file
    const fileRes = await fetch(`https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/${String(fileNum).padStart(4, '0')}.json`);
    const words = await fileRes.json();
    
    // Step 4: Find word in file
    return words.find(w => w.word.toLowerCase() === word.toLowerCase());
}

// Example
const word = await getWordFast('hello');
console.log(word);
```

### Prefix Search

```javascript
// JavaScript - Prefix search
async function searchByPrefix(prefix) {
    const firstLetter = prefix[0].toLowerCase();
    
    // Fetch letter-based file
    const res = await fetch(`https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/${firstLetter}.json`);
    const words = await res.json();
    
    // Filter by prefix
    return words.filter(w => w.word.toLowerCase().startsWith(prefix.toLowerCase()));
}

// Example
const results = await searchByPrefix('hel');
console.log(results);
```

### Performance Comparison

| Metric | v1.0 (Original) | v2.0 (Fast Search) |
|--------|-----------------|-------------------|
| **Exact Lookup Time** | 30-60 sec | 0.5-1 sec |
| **Network Requests** | Up to 770 | 2 (index + file) |
| **Data Transfer** | ~500 MB | ~50 KB |
| **Prefix Search** | Not supported | 0.5-1 sec |

### API Directory Structure

```
api/
├── dict/
│   ├── index.json          # Metadata
│   ├── word-index.json     # Word-to-file mapping
│   ├── search.json         # Search optimization metadata
│   ├── 0001.json - 0771.json  # Dictionary files
│   ├── a.json - z.json     # Letter-based files
│   ├── 0-9.json            # Numbers
│   └── special.json        # Special characters
├── vocabulary/              # Vocabulary lists
├── convert_to_json.py      # Original conversion script
├── build_index.py          # Build word-to-file index
├── split_by_letter.py      # Split files by first letter
└── create_search_meta.py   # Create search metadata
```