"""
CSV output functionality for PubMed paper search results.
"""

import csv
import sys
from typing import List, TextIO, Optional
from .pubmed_client import PubMedPaper


class PubMedCSVWriter:
    """Handles writing PubMed paper data to CSV format."""
    
    CSV_HEADERS = [
        'PubmedID',
        'Title',
        'PublicationDate',
        'Non-academicAuthor(s)',
        'CompanyAffiliation(s)',
        'CorrespondingAuthorEmail'
    ]
    
    def __init__(self, output_file: Optional[TextIO] = None):
        """Initialize CSV writer with optional output file."""
        self.output_file = output_file or sys.stdout
    
    def write_papers(self, papers: List[PubMedPaper]) -> None:
        """Write papers to CSV format."""
        writer = csv.writer(self.output_file)
        
        # Write headers
        writer.writerow(self.CSV_HEADERS)
        
        # Write paper data
        for paper in papers:
            row = self._paper_to_row(paper)
            writer.writerow(row)
    
    def _paper_to_row(self, paper: PubMedPaper) -> List[str]:
        """Convert a PubMedPaper to CSV row format."""
        return [
            paper.pubmed_id,
            self._clean_text_for_csv(paper.title),
            paper.publication_date,
            '; '.join(paper.non_academic_authors),
            '; '.join(paper.company_affiliations),
            paper.corresponding_email or ''
        ]
    
    def _clean_text_for_csv(self, text: Optional[str]) -> str:
        """Clean text for CSV output by removing problematic characters."""
        if not text:
            return ''
        
        # Remove newlines and excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove any null bytes that might cause issues
        cleaned = cleaned.replace('\x00', '')
        
        return cleaned