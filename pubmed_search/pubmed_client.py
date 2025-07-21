"""
PubMed API client for fetching research papers.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import time
import requests


class PubMedPaper:
    """Represents a research paper from PubMed."""
    
    def __init__(self, pubmed_id: str, title: str, publication_date: str,
                 authors: List[Dict[str, str]], corresponding_email: Optional[str] = None):
        self.pubmed_id = pubmed_id
        self.title = title
        self.publication_date = publication_date
        self.authors = authors  # List of dicts with 'name', 'affiliation'
        self.corresponding_email = corresponding_email
        self.non_academic_authors: List[str] = []
        self.company_affiliations: List[str] = []


class PubMedClient:
    """Client for interacting with PubMed API."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    PHARMA_BIOTECH_KEYWORDS = {
        'pharmaceutical', 'pharmaceuticals', 'pharma', 'biotech', 'biotechnology',
        'biopharmaceutical', 'biopharmaceuticals', 'drug', 'medicines', 'therapeutics',
        'inc.', 'inc', 'corp.', 'corp', 'ltd.', 'ltd', 'company', 'co.',
        'gmbh', 'ag', 'sa', 'plc', 'llc', 'limited'
    }
    
    ACADEMIC_KEYWORDS = {
        'university', 'college', 'institute', 'school', 'hospital', 'medical center',
        'research center', 'laboratory', 'dept', 'department', 'faculty',
        'academic', 'clinic', 'medical school'
    }
    
    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize PubMed client."""
        self.email = email
        self.api_key = api_key
        self.session = requests.Session()
    
    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """Search PubMed for papers and return PMIDs."""
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'xml'
        }
        
        if self.email:
            params['email'] = self.email
        if self.api_key:
            params['api_key'] = self.api_key
            
        url = f"{self.BASE_URL}esearch.fcgi"
        
        try:
            # Add small delay to respect API rate limits
            time.sleep(0.34)  # NCBI recommends max 3 requests per second
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            id_list = root.find('.//IdList')
            
            if id_list is not None:
                return [id_elem.text for id_elem in id_list.findall('Id') if id_elem.text]
            return []
            
        except requests.RequestException as e:
            raise Exception(f"PubMed search failed: {e}")
        except ET.ParseError as e:
            raise Exception(f"Failed to parse PubMed search response: {e}")
    
    def fetch_paper_details(self, pmids: List[str]) -> List[PubMedPaper]:
        """Fetch detailed information for papers by PMID."""
        if not pmids:
            return []
            
        # PubMed API allows up to 200 IDs per request
        papers = []
        batch_size = 200
        
        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i + batch_size]
            papers.extend(self._fetch_batch_details(batch_pmids))
            # Add delay between batches to respect rate limits
            if i + batch_size < len(pmids):
                time.sleep(0.5)
            
        return papers
    
    def _fetch_batch_details(self, pmids: List[str]) -> List[PubMedPaper]:
        """Fetch details for a batch of PMIDs."""
        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml',
            'rettype': 'abstract'
        }
        
        if self.email:
            params['email'] = self.email
        if self.api_key:
            params['api_key'] = self.api_key
            
        url = f"{self.BASE_URL}efetch.fcgi"
        
        try:
            # Add small delay to respect API rate limits
            time.sleep(0.34)  # NCBI recommends max 3 requests per second
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            return self._parse_paper_details(response.content)
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch paper details: {e}")
        except ET.ParseError as e:
            raise Exception(f"Failed to parse paper details response: {e}")
    
    def _parse_paper_details(self, xml_content: bytes) -> List[PubMedPaper]:
        """Parse XML response to extract paper details."""
        papers = []
        
        try:
            root = ET.fromstring(xml_content)
            
            for article in root.findall('.//PubmedArticle'):
                paper = self._extract_paper_info(article)
                if paper:
                    papers.append(paper)
                    
        except ET.ParseError as e:
            raise Exception(f"Failed to parse XML content: {e}")
            
        return papers
    
    def _extract_paper_info(self, article_elem) -> Optional[PubMedPaper]:
        """Extract paper information from XML element."""
        try:
            # Extract PMID
            pmid_elem = article_elem.find('.//PMID')
            if pmid_elem is None or not pmid_elem.text:
                return None
            pmid = pmid_elem.text
            
            # Extract title
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "No title available"
            
            # Extract publication date
            pub_date = self._extract_publication_date(article_elem)
            
            # Extract authors and affiliations
            authors = self._extract_authors_and_affiliations(article_elem)
            
            # Extract corresponding author email
            corresponding_email = self._extract_corresponding_email(article_elem)
            
            return PubMedPaper(pmid, title, pub_date, authors, corresponding_email)
            
        except Exception as e:
            # Log error but continue processing other papers
            print(f"Error extracting paper info: {e}")
            return None
    
    def _extract_publication_date(self, article_elem) -> str:
        """Extract publication date from article element."""
        # Try different date fields in order of preference
        date_paths = [
            './/PubDate',
            './/ArticleDate',
            './/DateCompleted',
            './/DateRevised'
        ]
        
        for path in date_paths:
            date_elem = article_elem.find(path)
            if date_elem is not None:
                year = date_elem.find('Year')
                month = date_elem.find('Month')
                day = date_elem.find('Day')
                
                year_text = year.text if year is not None else ""
                month_text = month.text if month is not None else ""
                day_text = day.text if day is not None else ""
                
                if year_text:
                    date_parts = [year_text]
                    if month_text:
                        # Handle both numeric and text months
                        if month_text.isdigit():
                            date_parts.append(month_text.zfill(2))
                        else:
                            # Convert month names to numbers
                            month_map = {
                                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                                'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                                'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                            }
                            month_num = month_map.get(month_text.lower()[:3], month_text)
                            date_parts.append(month_num)
                    if day_text and day_text.isdigit():
                        date_parts.append(day_text.zfill(2))
                    return "-".join(date_parts)
                    
        return "Unknown"
    
    def _extract_authors_and_affiliations(self, article_elem) -> List[Dict[str, str]]:
        """Extract authors and their affiliations."""
        authors = []
        author_list = article_elem.find('.//AuthorList')
        
        if author_list is not None:
            for author in author_list.findall('Author'):
                # Extract author name
                last_name = author.find('LastName')
                first_name = author.find('ForeName')
                initials = author.find('Initials')
                
                name_parts = []
                if last_name is not None and last_name.text:
                    name_parts.append(last_name.text)
                if first_name is not None and first_name.text:
                    name_parts.append(first_name.text)
                elif initials is not None and initials.text:
                    name_parts.append(initials.text)
                
                if not name_parts:
                    continue
                    
                author_name = ", ".join(name_parts)
                
                # Extract affiliations
                affiliations = []
                affiliation_info = author.find('AffiliationInfo')
                if affiliation_info is not None:
                    for affiliation in affiliation_info.findall('Affiliation'):
                        if affiliation.text:
                            affiliations.append(affiliation.text)
                
                authors.append({
                    'name': author_name,
                    'affiliation': '; '.join(affiliations) if affiliations else ""
                })
                
        return authors
    
    def _extract_corresponding_email(self, article_elem) -> Optional[str]:
        """Extract corresponding author email if available."""
        # Look for email in various locations
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Check author affiliations for emails
        author_list = article_elem.find('.//AuthorList')
        if author_list is not None:
            for author in author_list.findall('Author'):
                affiliation_info = author.find('AffiliationInfo')
                if affiliation_info is not None:
                    for affiliation in affiliation_info.findall('Affiliation'):
                        if affiliation.text:
                            emails = re.findall(email_pattern, affiliation.text)
                            if emails:
                                return emails[0]
        
        # Check abstract for emails (some papers include contact info there)
        abstract = article_elem.find('.//AbstractText')
        if abstract is not None and abstract.text:
            emails = re.findall(email_pattern, abstract.text)
            if emails:
                return emails[0]
                
        return None
    
    def is_non_academic_affiliation(self, affiliation: str) -> bool:
        """Determine if an affiliation is non-academic (pharmaceutical/biotech)."""
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # Check if it contains academic keywords (likely academic)
        for keyword in self.ACADEMIC_KEYWORDS:
            if keyword in affiliation_lower:
                return False
                
        # Check if it contains pharmaceutical/biotech keywords
        for keyword in self.PHARMA_BIOTECH_KEYWORDS:
            if keyword in affiliation_lower:
                return True
                
        # Additional heuristics: look for corporate suffixes and patterns
        corporate_patterns = [
            r'\b(inc\.?|corp\.?|ltd\.?|llc|gmbh|ag|sa|plc)\b',
            r'\b\w+\s+(pharmaceuticals?|biotech|biotechnology)\b',
            r'\b(drug|pharmaceutical|biotech)\s+company\b'
        ]
        
        for pattern in corporate_patterns:
            if re.search(pattern, affiliation_lower):
                return True
                
        return False
    
    def filter_papers_with_non_academic_authors(self, papers: List[PubMedPaper]) -> List[PubMedPaper]:
        """Filter papers to include only those with at least one non-academic author."""
        filtered_papers = []
        
        for paper in papers:
            non_academic_authors = []
            company_affiliations = []
            
            for author in paper.authors:
                if self.is_non_academic_affiliation(author['affiliation']):
                    non_academic_authors.append(author['name'])
                    
                    # Extract company names from affiliation
                    companies = self._extract_company_names(author['affiliation'])
                    company_affiliations.extend(companies)
            
            if non_academic_authors:
                paper.non_academic_authors = non_academic_authors
                paper.company_affiliations = list(set(company_affiliations))  # Remove duplicates
                filtered_papers.append(paper)
                
        return filtered_papers
    
    def _extract_company_names(self, affiliation: str) -> List[str]:
        """Extract company names from affiliation string."""
        if not affiliation:
            return []
            
        companies = []
        
        # Split by common delimiters
        parts = re.split(r'[,;.]', affiliation)
        
        for part in parts:
            part = part.strip()
            part_lower = part.lower()
            
            # Skip if it looks academic
            if any(keyword in part_lower for keyword in self.ACADEMIC_KEYWORDS):
                continue
                
            # Check if this part contains pharmaceutical/biotech keywords
            if any(keyword in part_lower for keyword in self.PHARMA_BIOTECH_KEYWORDS):
                # Clean up the company name
                company = self._clean_company_name(part)
                if company:
                    companies.append(company)
                    
        return companies
    
    def _clean_company_name(self, company_text: str) -> str:
        """Clean and standardize company names."""
        # Remove common prefixes/suffixes that aren't part of the company name
        cleaned = company_text.strip()
        
        # Remove leading/trailing punctuation
        cleaned = re.sub(r'^[^\w]+|[^\w]+$', '', cleaned)
        
        # Remove department/division info that might precede company name
        cleaned = re.sub(r'^(department of|dept of|division of)\s+', '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip() if cleaned else company_text.strip()