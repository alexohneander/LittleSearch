# LittleSearch

LittleSearch is a Python-based search indexing and retrieval library. It provides tools to tokenize, index, and search through documents efficiently. The project is modular, making it easy to extend and customize.

## Features

- **Tokenization**: Supports multiple tokenization strategies (ngrams, prefixes, words).
- **Indexing**: Efficiently indexes documents for fast retrieval.
- **Search**: Provides search capabilities over indexed documents.
- **Interfaces**: Abstract interfaces for extensibility.
- **Utilities**: Logging and helper functions for better development experience.

## Project Structure

```text
githooks/
    pre-commit          # Git hooks for pre-commit checks
src/
    main.py             # Entry point for the application
    interfaces/
        indexable_document_interface.py  # Interface for indexable documents
        tokenizer_interface.py           # Interface for tokenizers
    models/
        index_entry.py   # Model for index entries
        index_token.py   # Model for tokens in the index
    services/
        search_indexing_service.py  # Service for indexing documents
        search_service.py           # Service for searching documents
    utils/
        logger.py         # Logging utility
        ngrams_tokenizer.py  # N-grams tokenizer implementation
        prefix_tokenizer.py # Prefix tokenizer implementation
        word_tokenizer.py   # Word tokenizer implementation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/alexohneander/LittleSearch.git
   ```

2. Navigate to the project directory:

   ```bash
   cd LittleSearch
   ```

3. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the main application:

   ```bash
   python src/main.py
   ```

2. Customize tokenizers or services by modifying the respective files in the `src/` directory.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature-name
   ```

3. Commit your changes:

   ```bash
   git commit -m "Description of changes"
   ```

4. Push to your branch:

   ```bash
   git push origin feature-name
   ```

5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various search indexing techniques and libraries.
- Special thanks to contributors and the open-source community.