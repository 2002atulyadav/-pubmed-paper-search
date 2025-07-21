#!/usr/bin/env python3
"""
Test script for actual PubMed API functionality.
Run this only after dependencies are installed.
"""

import sys
import time
from pubmed_search import PubMedClient, PubMedCSVWriter
from io import StringIO

def test_pubmed_client():
    """Test PubMed client with a simple query."""
    print("🧪 Testing PubMed API client...")
    
    try:
        # Initialize client
        client = PubMedClient(email="test@example.com")  # Use your email for better results
        print("✅ PubMed client initialized successfully")
        
        # Test search with a very simple, common query
        print("🔍 Testing search functionality with 'aspirin' (max 3 results)...")
        pmids = client.search_papers("aspirin", max_results=3)
        
        if pmids:
            print(f"✅ Search successful! Found {len(pmids)} papers")
            print(f"📄 Sample PMIDs: {pmids[:3]}")
            
            # Test fetching details for first paper only
            print("📊 Testing paper details fetch for first paper...")
            papers = client.fetch_paper_details([pmids[0]])
            
            if papers:
                paper = papers[0]
                print("✅ Paper details fetched successfully")
                print(f"📝 Title: {paper.title[:100]}...")
                print(f"📅 Date: {paper.publication_date}")
                print(f"👥 Authors: {len(paper.authors)}")
                
                # Test filtering
                print("🔍 Testing non-academic filtering...")
                filtered = client.filter_papers_with_non_academic_authors(papers)
                print(f"✅ Filtering complete: {len(filtered)} papers with non-academic authors")
                
                return True
            else:
                print("❌ No paper details could be fetched")
                return False
        else:
            print("❌ No papers found for 'aspirin' - this might indicate an API issue")
            return False
            
    except Exception as e:
        print(f"❌ Error during API testing: {e}")
        print("💡 This might be due to:")
        print("   - Missing internet connection")
        print("   - PubMed API temporarily unavailable")
        print("   - Missing dependencies")
        return False

def test_csv_output():
    """Test CSV output functionality with dummy data."""
    print("\n🧪 Testing CSV output functionality...")
    
    try:
        from pubmed_search.pubmed_client import PubMedPaper
        
        # Create dummy paper data
        dummy_paper = PubMedPaper(
            pubmed_id="12345678",
            title="Test Paper Title",
            publication_date="2023-01-15",
            authors=[
                {"name": "Smith, John", "affiliation": "Pharma Corp Inc."},
                {"name": "Doe, Jane", "affiliation": "University of Science"}
            ],
            corresponding_email="john.smith@pharmacorp.com"
        )
        
        # Simulate non-academic filtering
        dummy_paper.non_academic_authors = ["Smith, John"]
        dummy_paper.company_affiliations = ["Pharma Corp Inc."]
        
        # Test CSV writing to string
        output = StringIO()
        writer = PubMedCSVWriter(output)
        writer.write_papers([dummy_paper])
        
        csv_content = output.getvalue()
        if csv_content and "PubmedID" in csv_content and "12345678" in csv_content:
            print("✅ CSV output functionality works correctly")
            print("📄 Sample CSV output:")
            print(csv_content)
            return True
        else:
            print("❌ CSV output seems incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Error during CSV testing: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting API functionality tests...")
    print("⚠️  Make sure you have internet connection and dependencies installed!\n")
    
    # Test API functionality
    api_success = test_pubmed_client()
    
    # Test CSV functionality  
    csv_success = test_csv_output()
    
    print(f"\n📊 Test Results:")
    print(f"   API Functionality: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"   CSV Output: {'✅ PASS' if csv_success else '❌ FAIL'}")
    
    if api_success and csv_success:
        print("\n🎉 All tests passed! Your code is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")