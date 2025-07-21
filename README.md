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

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   This will set up all required dependencies including:
   - `requests` - for API calls to PubMed E-utilities
   - `click` - for command-line interface framework

3. The installation will create an executable command `get-papers-list` via Poetry.

## Usage

### Basic Usage

```bash
# Search and output to console
get-papers-list "cancer treatment 2023"

# Save results to a CSV file
get-papers-list "diabetes drug therapy" --file results.csv

# Enable debug mode for detailed information
get-papers-list "alzheimer AND pharmaceutical" --debug --file alzheimer_papers.csv
```

### Command-line Options

- **Query** (required): Search query using PubMed syntax
- `-h, --help`: Display usage instructions (built-in Click help)
- `-d, --debug`: Print debug information during execution
- `-f, --file FILENAME`: Specify filename to save results (default: output to console)
- `--max-results N`: Maximum number of results to fetch (default: 100)
- `--email EMAIL`: Email address for PubMed API (recommended for better rate limits)
- `--api-key KEY`: API key for PubMed API (optional, for higher rate limits)

### Advanced Query Examples

```bash
# Search with date range
get-papers-list "cancer[MeSH] AND 2023:2024[pdat]" --file cancer_2023_2024.csv

# Search specific journal
get-papers-list "diabetes AND Nature[journal]" --debug

# Complex query with multiple terms
get-papers-list "(alzheimer OR dementia) AND drug therapy AND clinical trial" --file alzheimer_trials.csv
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
├── README.md               # This file
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

### Using Poetry (Recommended)

After running `poetry install`, you can test with Poetry:

```bash
# Test basic functionality
poetry run get-papers-list "aspirin" --debug --max-results 5

# Test file output
poetry run get-papers-list "covid vaccine" --file test_output.csv --debug --max-results 10
```

### Direct Python Module Execution

Alternatively, if Poetry isn't available, you can run directly:

```bash
# Basic functionality test (requires dependencies installed)
python3 -m pubmed_search.cli "aspirin" --debug --max-results 5

# Test file output
python3 -m pubmed_search.cli "covid vaccine" --file test_output.csv --debug --max-results 10
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

1. **No papers found**: Try broader search terms or check PubMed query syntax
2. **API timeouts**: Check internet connection and try with smaller result sets
3. **Permission errors**: Ensure write permissions for output file location
4. **Import errors**: Verify virtual environment activation and dependency installation

### Getting Help

For issues or questions:
1. Check the debug output using the `-d` flag
2. Verify your search query works on the PubMed website
3. Ensure all dependencies are properly installed via Poetry