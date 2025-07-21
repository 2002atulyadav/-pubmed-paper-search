# PubMed Paper Search Tool

A Python command-line tool to fetch research papers from PubMed and identify papers with authors affiliated with pharmaceutical or biotech companies.

## Features

- **PubMed Integration**: Fetches papers using the official PubMed E-utilities API
- **Smart Filtering**: Identifies papers with non-academic (pharmaceutical/biotech) author affiliations
- **Flexible Queries**: Supports full PubMed query syntax for complex searches
- **CSV Output**: Results exported in structured CSV format with detailed information
- **Command-line Interface**: Simple and intuitive CLI with debug mode

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry for dependency management

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pubmed-paper-search
   ```

2. Install dependencies (choose one method):

   **Method A: Using Poetry (Recommended)**
   ```bash
   poetry install
   ```
   
   **Method B: Using pip with virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   # OR venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

   This will set up all required dependencies including:
   - `requests` - for API calls to PubMed E-utilities
   - `click` - for command-line interface framework

3. **Poetry users**: The installation creates an executable command `get-papers-list`
   **Pip users**: Use `python3 -m pubmed_search.cli` to run the tool

## Usage

### Basic Usage

**With Poetry:**
```bash
# Search and output to console
poetry run get-papers-list "cancer treatment 2023"

# Save results to a CSV file
poetry run get-papers-list "diabetes drug therapy" --file results.csv

# Enable debug mode for detailed information
poetry run get-papers-list "alzheimer AND pharmaceutical" --debug --file alzheimer_papers.csv
```

**With pip (virtual environment activated):**
```bash
# Search and output to console
python3 -m pubmed_search.cli "cancer treatment 2023"

# Save results to a CSV file
python3 -m pubmed_search.cli "diabetes drug therapy" --file results.csv

# Enable debug mode for detailed information
python3 -m pubmed_search.cli "alzheimer AND pharmaceutical" --debug --file alzheimer_papers.csv
```

### Command-line Options

- **QUERY** (required): Search query using PubMed syntax (positional argument)
- `-h, --help`: Display usage instructions (built-in Click help)
- `-d, --debug`: Print debug information during execution
- `-f, --file FILENAME`: Specify filename to save results (default: output to console)
- `--max-results N`: Maximum number of results to fetch (default: 100)
- `--email EMAIL`: Email address for PubMed API (recommended for better rate limits)
- `--api-key KEY`: API key for PubMed API (optional, for higher rate limits)

### Advanced Query Examples

**With Poetry:**
```bash
# Search with date range
poetry run get-papers-list "cancer[MeSH] AND 2023:2024[pdat]" --file cancer_2023_2024.csv

# Search specific journal
poetry run get-papers-list "diabetes AND Nature[journal]" --debug

# Complex query with multiple terms
poetry run get-papers-list "(alzheimer OR dementia) AND drug therapy AND clinical trial" --file alzheimer_trials.csv
```

**With pip:**
```bash
# Search with date range
python3 -m pubmed_search.cli "cancer[MeSH] AND 2023:2024[pdat]" --file cancer_2023_2024.csv

# Search specific journal
python3 -m pubmed_search.cli "diabetes AND Nature[journal]" --debug

# Complex query with multiple terms
python3 -m pubmed_search.cli "(alzheimer OR dementia) AND drug therapy AND clinical trial" --file alzheimer_trials.csv
```

## Output Format

The tool generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| **PubmedID** | Unique identifier for the paper |
| **Title** | Title of the research paper |
| **PublicationDate** | Date the paper was published |
| **Non-academicAuthor(s)** | Names of authors affiliated with pharmaceutical/biotech companies |
| **CompanyAffiliation(s)** | Names of pharmaceutical/biotech companies |
| **CorrespondingAuthorEmail** | Email address of the corresponding author |

### Sample Output

```csv
PubmedID,Title,PublicationDate,Non-academicAuthor(s),CompanyAffiliation(s),CorrespondingAuthorEmail
12345678,"Novel Cancer Treatment Approach",2023-06-15,"Smith, John; Doe, Jane","Pharma Corp; BioTech Inc","john.smith@pharmacorp.com"
```

## Code Organization

The project is structured as follows:

```
pubmed-paper-search/
├── pubmed_search/           # Main package
│   ├── __init__.py         # Package initialization and exports
│   ├── cli.py              # Command-line interface implementation
│   ├── pubmed_client.py    # PubMed API client and data models
│   └── csv_writer.py       # CSV output functionality
├── pyproject.toml          # Poetry configuration and dependencies
├── requirements.txt        # Pip dependencies file
├── README.md               # This file
├── TESTING.md              # Detailed testing guide
├── test_import.py          # Import validation test
├── test_api.py             # API functionality test
├── test_e2e.py             # End-to-end CLI test
└── Backendtakehomeproblem.pdf  # Original requirements
```

### Key Components

1. **PubMedClient**: Handles all interactions with the PubMed API
   - Searches for papers using E-utilities API
   - Fetches detailed paper information
   - Filters papers by author affiliations
   - Implements smart heuristics to identify non-academic affiliations

2. **PubMedPaper**: Data model representing a research paper
   - Stores paper metadata (ID, title, publication date)
   - Contains author information and affiliations
   - Tracks identified company affiliations and corresponding author email

3. **PubMedCSVWriter**: Handles CSV output formatting
   - Converts paper data to CSV format
   - Handles text cleaning for CSV compatibility
   - Supports both file and console output

4. **CLI Module**: Command-line interface implementation
   - Argument parsing and validation
   - Debug mode with detailed logging
   - Error handling and user feedback

## Non-Academic Institution Detection

The tool uses several heuristics to identify pharmaceutical and biotech company affiliations:

### Company Keywords
- Pharmaceutical terms: `pharmaceutical`, `pharma`, `drug`, `medicines`, `therapeutics`
- Biotech terms: `biotech`, `biotechnology`, `biopharmaceutical`
- Corporate suffixes: `Inc.`, `Corp.`, `Ltd.`, `LLC`, `GmbH`, `AG`, `SA`, `PLC`

### Academic Institution Exclusion
Authors affiliated with the following are considered academic:
- Universities and colleges
- Hospitals and medical centers
- Research institutes and laboratories
- Government research facilities

### Pattern Matching
- Regular expressions to identify corporate naming patterns
- Company name extraction and cleaning
- Email domain analysis for institutional identification

## Error Handling and Robustness

The tool includes comprehensive error handling for:

- **API Failures**: Network timeouts, rate limiting, invalid responses
- **Invalid Queries**: Malformed search queries, no results found
- **Data Issues**: Missing paper data, corrupted XML responses
- **File Operations**: Permission errors, disk space issues
- **Graceful Interruption**: Proper handling of Ctrl+C (SIGINT)
- **Parameter Validation**: Validates max-results parameter and warns about large datasets
- **Rate Limiting**: Built-in delays to respect PubMed API rate limits (max 3 requests/second)
- **Date Parsing**: Handles both numeric and text-based publication dates

## Development Tools Used

This project was developed with assistance from the following tools and resources:

- **Claude AI (Anthropic)**: Code generation, debugging, and documentation assistance
- **PubMed E-utilities API**: Official NCBI API for accessing PubMed database
  - Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- **Click Framework**: Python package for creating command-line interfaces
  - Documentation: https://click.palletsprojects.com/
- **Poetry**: Modern dependency management and packaging tool
  - Website: https://python-poetry.org/

## API Rate Limits and Best Practices

To ensure reliable operation and respect PubMed's usage policies:

1. **Email Registration**: Always provide an email address when making API calls
2. **Rate Limiting**: The tool implements appropriate delays between API calls
3. **Batch Processing**: Fetches paper details in batches to minimize API calls
4. **Timeout Management**: Handles network timeouts gracefully
5. **Error Retry**: Implements basic retry logic for transient failures

For production use or high-volume searches, consider:
- Registering for a PubMed API key
- Implementing more sophisticated caching
- Adding database storage for results

## Testing

### Quick Test Commands

After installing dependencies, test the tool with these commands:

**With Poetry:**
```bash
# Test help
poetry run get-papers-list --help

# Test basic functionality
poetry run get-papers-list "aspirin" --debug --max-results 5

# Test file output
poetry run get-papers-list "covid vaccine" --file test_output.csv --debug --max-results 10
```

**With pip (virtual environment activated):**
```bash
# Test help
python3 -m pubmed_search.cli --help

# Test basic functionality  
python3 -m pubmed_search.cli "aspirin" --debug --max-results 5

# Test file output
python3 -m pubmed_search.cli "covid vaccine" --file test_output.csv --debug --max-results 10
```

### Using Test Scripts

The project includes several test scripts:
- `test_import.py` - Verify imports work correctly
- `test_api.py` - Test PubMed API functionality 
- `test_e2e.py` - End-to-end CLI testing

Run them after installing dependencies:
```bash
python3 test_import.py
python3 test_api.py
python3 test_e2e.py
```

## Contributing

1. Ensure all code includes proper type hints
2. Follow PEP 8 style guidelines
3. Add docstrings to all public functions and classes
4. Test with various query types and edge cases
5. Update documentation for any new features

## License

This project is developed for educational and research purposes.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: 
   - Activate virtual environment: `source venv/bin/activate` or `poetry shell`
   - Install dependencies: `pip install -r requirements.txt` or `poetry install`

2. **No papers found**: 
   - Try common search terms: "aspirin", "diabetes", "covid vaccine"
   - Check PubMed query syntax on pubmed.ncbi.nlm.nih.gov
   - Use smaller result sets: `--max-results 5`

3. **API timeouts**: 
   - Check internet connection
   - Try smaller `--max-results` (3-10)
   - Add your email: `--email your@email.com`

4. **Permission errors**: 
   - Ensure write permissions for output file location
   - Try different path: `--file /tmp/results.csv`

5. **Command not found**:
   - Poetry users: Use `poetry run get-papers-list`
   - Pip users: Use `python3 -m pubmed_search.cli`

### Getting Help

For issues or questions:
1. Check the debug output using the `-d` or `--debug` flag
2. Verify your search query works on the PubMed website
3. Run the test scripts to identify specific issues
4. Check the TESTING.md file for detailed troubleshooting