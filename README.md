# Rank Retrieval Model

**Document Retrieval · Inverted Index · TF-IDF · Boolean Search**

[نسخه فارسی](README.fa.md)

This project implements a small document retrieval system in Python. It searches a collection of **41 English text documents** and supports two ways of finding relevant files: Boolean queries and ranked retrieval.

## Features

- Text preprocessing with tokenization, stopword filtering and lemmatization
- Inverted index for locating documents that contain a term
- TF-IDF-based term weighting
- Boolean queries with `AND`, `OR`, `+` and `NOT`
- Parentheses for grouping Boolean conditions
- Ranked retrieval of up to 10 documents for regular text queries

## Query examples

Run `main.py` and enter a query in the terminal.

| Query | Meaning |
| --- | --- |
| `sport + line` | Documents containing **sport OR line** |
| `sport OR line` | Same as `+` |
| `sport AND line` | Documents containing **both** terms |
| `sport NOT line` | Documents containing sport but not line |
| `sport AND NOT line` | Same as above |
| `NOT sport` | Documents not containing sport |
| `(sport + line) AND NOT technology` | Grouped conditions |
| `online retail markets` | Ranked search without Boolean operators |

**Operator precedence:** `NOT` first, then `AND`, then `OR` / `+`. Boolean queries return the names of all matching documents; regular queries return up to 10 documents ordered by the project's similarity score.

Example:

```text
Enter your query: sport AND line
QUERY 1 :  sport AND line
['nike.txt', 'yahoo.txt']
```

![Example of ranked search output](Output/output_for_3_queries.png)

More examples are available in [`examples/sample_queries.txt`](examples/sample_queries.txt).

## Project structure

```text
Rank-Retrieval-Model/
├── main.py                  # Query input and output
├── PreprocessQuery.py       # Query processing
├── CosineSimilarity.py      # Document matching and scoring
├── PostingList.py           # Index and posting lists
├── Lemmatizer.py            # Lemmatization
├── Stopwords.py             # Stopword handling
├── tfidf.py                 # Term weighting
├── Dataset/                 # 41 text documents
├── Indexes/                 # Saved index files
├── tfidf_weights/           # Saved term weights
├── Output/                  # Example output
├── examples/                # Sample queries
├── tests/                   # Boolean query tests
├── docs/                    # Additional notes
├── requirements.txt
├── README.md
└── README.fa.md
```

## Setup

Python 3.10–3.12 is recommended. Install the required libraries:

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader stopwords punkt punkt_tab wordnet omw-1.4 averaged_perceptron_tagger averaged_perceptron_tagger_eng
```

A virtual environment may be used to keep the dependencies separate from other Python projects. On Windows, `py` can be used instead of `python`.

Start the search program from the project directory:

```bash
python main.py
```

Run the Boolean query tests:

```bash
python -m unittest discover -s tests -v
```

The library installation and language-model downloads require an internet connection. The document collection and index files are included in the repository.

## Notes

The ranking method uses the term weights and scoring rules implemented in the source code; it has not been evaluated on a standard retrieval benchmark. Boolean search is based on term matching rather than exact phrase matching. The stored index files should only be loaded from trusted sources.

The redistribution rights for the text documents are not confirmed. See [`docs/DATASET_AND_PUBLICATION.md`](docs/DATASET_AND_PUBLICATION.md) before sharing the dataset publicly.
