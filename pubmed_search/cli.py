"""
Command-line interface for PubMed paper search tool.
"""

import sys
from typing import Optional, TextIO
import click
from .pubmed_client import PubMedClient
from .csv_writer import PubMedCSVWriter


@click.command()
@click.argument('query', required=True)
@click.option('-d', '--debug', is_flag=True, help='Print debug information during execution.')
@click.option('-f', '--file', 'output_file', type=str, help='Specify the filename to save the results.')
@click.option('--max-results', default=100, help='Maximum number of results to fetch (default: 100)')
@click.option('--email', help='Email address for PubMed API (recommended)')
@click.option('--api-key', help='API key for PubMed API (optional, for higher rate limits)')
def main(query: str, debug: bool, output_file: Optional[str], max_results: int, 
         email: Optional[str], api_key: Optional[str]):
    """
    Search PubMed for research papers with pharmaceutical/biotech company affiliations.
    
    This tool searches PubMed for papers matching your query and filters them to include
    only papers with at least one author affiliated with a pharmaceutical or biotech company.
    
    QUERY: Search query for PubMed (supports full PubMed query syntax)
    
    Examples:
        get-papers-list "cancer treatment 2023" --debug --file results.csv
        get-papers-list "diabetes AND drug therapy" --email your@email.com
    """
    # Validate parameters
    if max_results <= 0:
        click.echo("Error: max-results must be a positive integer", err=True)
        sys.exit(1)
    
    if max_results > 10000:
        click.echo("Warning: Large result sets may take significant time and may be rate-limited", err=True)
    
    if debug:
        click.echo(f"DEBUG: Searching PubMed for: {query}", err=True)
        click.echo(f"DEBUG: Maximum results: {max_results}", err=True)
        if email:
            click.echo(f"DEBUG: Using email: {email}", err=True)
        if api_key:
            click.echo("DEBUG: Using API key for enhanced rate limits", err=True)
        if output_file:
            click.echo(f"DEBUG: Output file: {output_file}", err=True)
        else:
            click.echo("DEBUG: Output to console", err=True)
        click.echo("", err=True)
    
    try:
        # Initialize PubMed client
        client = PubMedClient(email=email, api_key=api_key)
        
        # Search for papers
        if debug:
            click.echo("DEBUG: Searching PubMed...", err=True)
        pmids = client.search_papers(query, max_results)
        
        if not pmids:
            click.echo("No papers found for the given query.", err=True)
            sys.exit(1)
        
        if debug:
            click.echo(f"DEBUG: Found {len(pmids)} papers. Fetching details...", err=True)
        
        # Fetch paper details
        papers = client.fetch_paper_details(pmids)
        
        if debug:
            click.echo(f"DEBUG: Retrieved details for {len(papers)} papers.", err=True)
        
        # Filter for papers with non-academic authors
        filtered_papers = client.filter_papers_with_non_academic_authors(papers)
        
        if not filtered_papers:
            if debug:
                click.echo("DEBUG: No papers found with pharmaceutical/biotech company affiliations.", err=True)
            sys.exit(0)
        
        if debug:
            click.echo(f"DEBUG: Found {len(filtered_papers)} papers with non-academic authors.", err=True)
            click.echo("DEBUG: Writing results to CSV...", err=True)
        
        # Write results to CSV
        output_stream: TextIO
        if output_file:
            output_stream = open(output_file, 'w', newline='', encoding='utf-8')
        else:
            output_stream = sys.stdout
        
        try:
            writer = PubMedCSVWriter(output_stream)
            writer.write_papers(filtered_papers)
        finally:
            if output_file:
                output_stream.close()
        
        if debug:
            if output_file:
                click.echo(f"DEBUG: Results written to {output_file}", err=True)
            else:
                click.echo("DEBUG: Results written to stdout", err=True)
    
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(130)
    except Exception as e:
        if debug:
            import traceback
            click.echo(f"DEBUG: Exception details:\n{traceback.format_exc()}", err=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()