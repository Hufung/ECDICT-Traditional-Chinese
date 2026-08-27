# ECDICT Traditional Chinese API Version

This is the API version of ECDICT Traditional Chinese, designed for easy integration with web and mobile applications.

## 📁 Directory Structure

```
api/
├── dict/                    # Dictionary JSON files
│   ├── index.json          # Metadata and file index
│   ├── 0001.json           # First 1000 words
│   ├── 0002.json           # Next 1000 words
│   └── ...                 # Up to 771 files (770,611 words)
├── vocabulary/             # Vocabulary lists
│   ├── cet4.json           # CET4 vocabulary
│   ├── cet6.json           # CET6 vocabulary
│   ├── gaokao.json         # Gaokao vocabulary
│   ├── zhongkao.json       # Zhongkao vocabulary
│   ├── collins_3star.json  # 3+ star Collins words
│   ├── collins_4star.json  # 4+ star Collins words
│   ├── collins_5star.json  # 5 star Collins words
│   └── oxford_3000.json    # Oxford 3000 core words
└── convert_to_json.py      # Conversion script
```

## 🚀 Quick Start

### 1. Generate API Files

```bash
cd api
python convert_to_json.py
```

This will create:
- `dict/` directory with 771 JSON files (1000 words each)
- `vocabulary/` directory with vocabulary lists
- `dict/index.json` with metadata

### 2. Use the API

#### Fetch a Word
```python
import requests
import json

def get_word(word_name):
    # Search through JSON files
    for i in range(1, 772):
        url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict/{i:04d}.json"
        response = requests.get(url)
        words = response.json()
        
        for word in words:
            if word['word'].lower() == word_name.lower():
                return word
    
    return None

# Example
word = get_word('hello')
print(json.dumps(word, ensure_ascii=False, indent=2))
```

#### Fetch Vocabulary List
```python
import requests

def get_vocabulary(vocab_type):
    url = f"https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/vocabulary/{vocab_type}.json"
    response = requests.get(url)
    return response.json()

# Example
cet4_vocab = get_vocabulary('cet4')
print(f"CET4 words: {cet4_vocab['count']}")
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

### Index File Format
```json
{
  "name": "ECDICT Traditional Chinese",
  "version": "1.0.0",
  "description": "English-Chinese Dictionary Database (Traditional Chinese)",
  "total_files": 771,
  "file_pattern": "{chunk_num:04d}.json",
  "base_url": "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict"
}
```

### Vocabulary List Format
```json
{
  "name": "cet4",
  "count": 4567,
  "words": ["hello", "world", "good", ...]
}
```

## 🔧 Integration Examples

### JavaScript/Node.js
```javascript
// Fetch a word
async function getWord(word) {
    for (let i = 1; i <= 771; i++) {
        const url = `https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict/${String(i).padStart(4, '0')}.json`;
        const response = await fetch(url);
        const words = await response.json();
        
        const found = words.find(w => w.word.toLowerCase() === word.toLowerCase());
        if (found) return found;
    }
    return null;
}

// Example usage
getWord('hello').then(word => console.log(word));
```

### Swift (iOS)
```swift
func getWord(_ word: String) async throws -> [String: Any]? {
    for i in 1...771 {
        let urlString = "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict/\(String(format: "%04d", i)).json"
        guard let url = URL(string: urlString) else { continue }
        
        let (data, _) = try await URLSession.shared.data(from: url)
        guard let words = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] else { continue }
        
        if let found = words.first(where: { ($0["word"] as? String)?.lowercased() == word.lowercased() }) {
            return found
        }
    }
    return nil
}
```

### Kotlin (Android)
```kotlin
suspend fun getWord(word: String): Map<String, Any>? {
    for (i in 1..771) {
        val url = "https://raw.githubusercontent.com/Hufung/ECDICT-Traditional-Chinese-API/main/dict/${String.format("%04d", i)}.json"
        val response = URL(url).readText()
        val words = Json.parseToJsonElement(response).jsonArray
        
        val found = words.firstOrNull { 
            it.jsonObject["word"]?.jsonPrimitive?.content?.lowercase() == word.lowercase() 
        }
        
        if (found != null) {
            return found.jsonObject.toMap()
        }
    }
    return null
}
```

## 📈 Performance Tips

1. **Cache locally**: Download JSON files and use local cache
2. **Use SQLite**: For better search performance, convert to SQLite
3. **Batch requests**: Fetch multiple words at once
4. **Index words**: Create a word-to-file mapping for faster lookup

## 🔄 Update Process

To update the dictionary:
1. Update `ecdict_traditional.csv`
2. Run `python convert_to_json.py`
3. Upload the new JSON files to GitHub

## 📚 Data Sources

- Original ECDICT: https://github.com/skywind3000/ECDICT
- Traditional Chinese conversion: OpenCC library
- Reference API structure: https://github.com/ismartcoding/endict

## 📄 License

MIT License - See LICENSE file for details