"""
PubMed Paper Search Tool

A Python package for searching PubMed papers and filtering by pharmaceutical/biotech company affiliations.
"""

from .pubmed_client import PubMedClient, PubMedPaper
from .csv_writer import PubMedCSVWriter

__version__ = "0.1.0"
__all__ = ["PubMedClient", "PubMedPaper", "PubMedCSVWriter"]