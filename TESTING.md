# 🧪 Manual Testing Guide

## Quick Setup & Test Commands

### Step 1: Install Dependencies
Choose one method:

**Method A: Poetry (Recommended)**
```bash
poetry install
poetry shell
```

**Method B: pip + virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Basic Tests

**Test 1: Check Help**
```bash
# With Poetry:
poetry run get-papers-list --help

# With pip:
python3 -m pubmed_search.cli --help
```
✅ Expected: Shows usage instructions and options

**Test 2: Test Parameter Validation**
```bash
# With Poetry:
poetry run get-papers-list "test" --max-results -1

# With pip:
python3 -m pubmed_search.cli "test" --max-results -1
```
✅ Expected: Shows error "max-results must be a positive integer"

**Test 3: Simple Query (Debug Mode)**
```bash
# With Poetry:
poetry run get-papers-list "aspirin" --debug --max-results 3

# With pip:
python3 -m pubmed_search.cli "aspirin" --debug --max-results 3
```
✅ Expected: Shows debug output, searches PubMed, displays results

**Test 4: File Output**
```bash
# With Poetry:
poetry run get-papers-list "cancer therapy" --file test_results.csv --debug --max-results 5

# With pip:
python3 -m pubmed_search.cli "cancer therapy" --file test_results.csv --debug --max-results 5
```
✅ Expected: Creates test_results.csv file with paper data

**Test 5: Check CSV Output**
```bash
cat test_results.csv
```
✅ Expected: Shows CSV with headers: PubmedID, Title, PublicationDate, etc.

## Troubleshooting

### Common Issues:

**1. Module not found errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or poetry shell

# Reinstall dependencies
pip install -r requirements.txt  # or poetry install
```

**2. No papers found**
Try different search terms:
- "aspirin" (very common drug)
- "diabetes" (common condition) 
- "covid vaccine" (recent topic)

**3. API timeouts**
- Check internet connection
- Use smaller --max-results (try 3-5)
- Add your email: --email your@email.com

**4. Permission errors**
- Make sure you can write to the current directory
- Try a different output path: --file /tmp/results.csv

## Success Indicators

✅ **Everything is working if you see:**
- Help command shows all options
- Debug mode shows "DEBUG: Searching PubMed..." messages
- Papers are found and filtered
- CSV file is created with proper headers
- Non-academic authors are identified

## Sample Successful Output

```
DEBUG: Searching PubMed for: aspirin
DEBUG: Maximum results: 3
DEBUG: Output to console

DEBUG: Searching PubMed...
DEBUG: Found 3 papers. Fetching details...
DEBUG: Retrieved details for 3 papers.
DEBUG: Found 1 papers with non-academic authors.
DEBUG: Writing results to CSV...

PubmedID,Title,PublicationDate,Non-academicAuthor(s),CompanyAffiliation(s),CorrespondingAuthorEmail
12345678,"Aspirin therapy in cardiovascular disease",2023-01-15,"Smith, John","Pharma Corp",john.smith@pharmacorp.com
```