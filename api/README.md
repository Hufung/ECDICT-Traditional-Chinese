# ECDICT Traditional Chinese API Version

This is the API version of ECDICT Traditional Chinese, designed for easy integration with web and mobile applications.

## 🚀 Fast Search (NEW in v2.0)

The API now supports **fast search** with O(1) lookup time:

### Exact Word Lookup

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
    
    // Step 4: Find word in file (binary search)
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

### Swift (iOS)

```swift
// Swift - Fast exact lookup
func getWordFast(_ word: String) async throws -> [String: Any]? {
    // Step 1: Fetch index (cache this!)
    let indexUrl = URL(string: "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/word-index.json")!
    let (indexData, _) = try await URLSession.shared.data(from: indexUrl)
    guard let wordIndex = try JSONSerialization.jsonObject(with: indexData) as? [String: Int] else { return nil }
    
    // Step 2: Get file number from index
    guard let fileNum = wordIndex[word.lowercased()] else { return nil }
    
    // Step 3: Fetch only that file
    let fileUrl = URL(string: "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/\(String(format: "%04d", fileNum)).json")!
    let (fileData, _) = try await URLSession.shared.data(from: fileUrl)
    guard let words = try JSONSerialization.jsonObject(with: fileData) as? [[String: Any]] else { return nil }
    
    // Step 4: Find word in file
    return words.first { ($0["word"] as? String)?.lowercased() == word.lowercased() }
}
```

### Kotlin (Android)

```kotlin
// Kotlin - Fast exact lookup
suspend fun getWordFast(word: String): Map<String, Any>? {
    // Step 1: Fetch index (cache this!)
    val indexUrl = URL("https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/word-index.json")
    val indexResponse = indexUrl.readText()
    val wordIndex = Json.parseToJsonElement(indexResponse).jsonObject.mapValues { it.value.jsonPrimitive.int }
    
    // Step 2: Get file number from index
    val fileNum = wordIndex[word.lowercase()] ?: return null
    
    // Step 3: Fetch only that file
    val fileUrl = URL("https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/${String.format("%04d", fileNum)}.json")
    val fileResponse = fileUrl.readText()
    val words = Json.parseToJsonElement(fileResponse).jsonArray
    
    // Step 4: Find word in file
    return words.firstOrNull { 
        it.jsonObject["word"]?.jsonPrimitive?.content?.lowercase() == word.lowercase() 
    }?.jsonObject?.toMap()
}
```

## 📁 Directory Structure

```
api/
├── dict/                    # Dictionary JSON files
│   ├── index.json          # Metadata and file index
│   ├── word-index.json     # Word-to-file mapping (for fast lookup)
│   ├── search.json         # Search optimization metadata
│   ├── 0001.json           # First 1000 words (sorted)
│   ├── 0002.json           # Next 1000 words (sorted)
│   ├── ...                 # Up to 770 files (770,611 words)
│   ├── a.json              # All words starting with 'a'
│   ├── b.json              # All words starting with 'b'
│   ├── ...                 # All letters
│   ├── z.json              # All words starting with 'z'
│   ├── 0-9.json            # Words starting with numbers
│   └── special.json        # Words starting with special characters
├── vocabulary/             # Vocabulary lists
│   ├── cet4.json           # CET4 vocabulary
│   ├── cet6.json           # CET6 vocabulary
│   ├── gaokao.json         # Gaokao vocabulary
│   ├── zhongkao.json       # Zhongkao vocabulary
│   ├── collins_3star.json  # 3+ star Collins words
│   ├── collins_4star.json  # 4+ star Collins words
│   ├── collins_5star.json  # 5 star Collins words
│   └── oxford_3000.json    # Oxford 3000 core words
├── convert_to_json.py      # Conversion script (original)
├── build_index.py          # Build word-to-file index
├── split_by_letter.py      # Split files by first letter
└── create_search_meta.py   # Create search metadata
```

## 🚀 Quick Start

### 1. Generate API Files (with fast search)

```bash
cd api
python convert_to_json.py
python build_index.py
python split_by_letter.py
python create_search_meta.py
```

### 2. Use the API

#### Fast Exact Lookup
```python
import requests

def get_word_fast(word_name):
    # Step 1: Fetch index (cache this!)
    index_url = "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/word-index.json"
    word_index = requests.get(index_url).json()
    
    # Step 2: Get file number from index
    file_num = word_index.get(word_name.lower())
    if not file_num:
        return None
    
    # Step 3: Fetch only that file
    file_url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/{file_num:04d}.json"
    words = requests.get(file_url).json()
    
    # Step 4: Find word in file (binary search)
    for w in words:
        if w['word'].lower() == word_name.lower():
            return w
    
    return None

# Example
word = get_word_fast('hello')
print(json.dumps(word, ensure_ascii=False, indent=2))
```

#### Prefix Search
```python
import requests

def search_by_prefix(prefix):
    first_letter = prefix[0].lower()
    
    # Fetch letter-based file
    url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/{first_letter}.json"
    words = requests.get(url).json()
    
    # Filter by prefix
    return [w for w in words if w['word'].lower().startswith(prefix.lower())]

# Example
results = search_by_prefix('hel')
print(f"Found {len(results)} words starting with 'hel'")
```

## 📊 JSON Format

### Word Entry Format
```json
{
  "word": "hello",
  "phonetic": "heˈləʊ",
  "definition": "used as a greeting",
  "translation": "你好",
  "pos": "excl:77/n:23",
  "collins": "5",
  "oxford": "1",
  "tag": "cet4 cet6 zk gk",
  "bnc": "186",
  "frq": "193",
  "exchange": "",
  "detail": "",
  "audio": ""
}
```

### Word Index Format
```json
{
  "hello": 123,
  "world": 456,
  "test": 789
}
```

### Letter File Format
```json
[
  {
    "word": "hello",
    "phonetic": "heˈləʊ",
    "definition": "used as a greeting",
    "translation": "你好",
    ...
  },
  {
    "word": "help",
    "phonetic": "help",
    "definition": "to assist",
    "translation": "幫助",
    ...
  }
]
```

## 📈 Performance Comparison

| Metric | v1.0 (Original) | v2.0 (Fast Search) |
|--------|-----------------|-------------------|
| **Exact Lookup Time** | 30-60 sec | 0.5-1 sec |
| **Network Requests** | Up to 770 | 2 (index + file) |
| **Data Transfer** | ~500 MB | ~50 KB |
| **Prefix Search** | Not supported | 0.5-1 sec |

## 🔧 Additional Examples

### Fetch Vocabulary List
```python
import requests

def get_vocabulary(vocab_type):
    url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/vocabulary/{vocab_type}.json"
    return requests.get(url).json()

# Example
cet4_vocab = get_vocabulary('cet4')
print(f"CET4 words: {cet4_vocab['count']}")
```

### Batch Lookup
```python
import requests
import asyncio
import aiohttp

async def get_word_batch(words):
    # Fetch index once
    index_url = "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/word-index.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(index_url) as resp:
            word_index = await resp.json()
    
    # Fetch files in parallel
    tasks = []
    for word in words:
        file_num = word_index.get(word.lower())
        if file_num:
            file_url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese/main/api/dict/{file_num:04d}.json"
            tasks.append(fetch_word_from_file(word, file_url))
    
    results = await asyncio.gather(*tasks)
    return {word: result for word, result in zip(words, results)}

async def fetch_word_from_file(word, file_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            words = await resp.json()
            for w in words:
                if w['word'].lower() == word.lower():
                    return w
    return None

# Example
results = asyncio.run(get_word_batch(['hello', 'world', 'test']))
print(results)
```

## 📈 Performance Tips

1. **Cache word-index.json**: This file is ~5 MB but enables O(1) lookup
2. **Cache letter files**: Reuse letter-based files for multiple prefix searches
3. **Use batch requests**: Fetch multiple words at once
4. **Local storage**: Download index files for offline use

## 🔄 Update Process

To update the dictionary:
1. Update `ecdict_traditional.csv`
2. Run:
   ```bash
   python convert_to_json.py
   python build_index.py
   python split_by_letter.py
   python create_search_meta.py
   ```
3. Upload the new files to GitHub

## 📚 Data Sources

- Original ECDICT: https://github.com/skywind3000/ECDICT
- Traditional Chinese conversion: OpenCC library
- Reference API structure: https://github.com/ismartcoding/endict

## 📄 License

MIT License - See LICENSE file for details
