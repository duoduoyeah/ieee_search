from ieee_search.core.xploreapi import XPLORE
from dotenv import load_dotenv
import os
import json
import time

# Function to extract paper metadata
def extract_paper_metadata(articles):
    papers = []
    for article in articles:
        paper = {
            "publication_title": article.get("publication_title", "N/A"),
            "title": article.get("title", "N/A"),
            "publication_year": article.get("publication_year", "N/A"),
            "doi": article.get("doi", "N/A"),
            "authors": [],
            "abstract": article.get("abstract", "N/A"),
            "keywords": article.get("author_terms", "N/A"),
        }
        
        # Extract authors
        if "authors" in article and "authors" in article["authors"]:
            for author in article["authors"]["authors"]:
                paper["authors"].append({
                    "name": author.get("full_name", "N/A"),
                    "affiliation": author.get("affiliation", "N/A")
                })
                
        papers.append(paper)
    return papers

def fetch_papers(start_year, end_year, api_key, conference_name):
    """Fetch papers from IEEE Visualization conference within the specified year range"""
    xplore = XPLORE(api_key)
    
    # Set up the search parameters
    xplore.publicationTitle(conference_name)
    xplore.resultsFilter("start_year", str(start_year))
    xplore.resultsFilter("end_year", str(end_year))
    xplore.resultsFilter("content_type", "Conferences")

    # Request all the metadata we need
    xplore.setDataFormat("object")
    xplore.maximumResults(200)
    
    # Collect all papers (handling pagination if needed)
    all_papers = []
    current_start = 1
    has_more_results = True
    
    while has_more_results:
        # Set the starting position for pagination
        xplore.startingResult(current_start)
        
        # Make API request
        results = xplore.callAPI()
        
        if "articles" in results and results["articles"]:
            # Extract metadata from current batch
            batch_papers = extract_paper_metadata(results["articles"])
            all_papers.extend(batch_papers)
            
            # Prepare for next page if needed
            total_results = int(results.get("total_records", 0))
            current_start += len(results["articles"])
            
            # Check if we've retrieved all available results
            if current_start > total_results:
                has_more_results = False
                
            # Add a short delay to avoid hitting API rate limits
            if has_more_results:
                time.sleep(1)
        else:
            # No results or error in response
            has_more_results = False
    
    return all_papers

def save_papers_to_json(papers, filename):
    """Save papers to a JSON file"""
    with open(filename, "w") as f:
        json.dump(papers, f, indent=2)

def display_paper_summary(papers, num_papers=3):
    """Print a summary of the first few papers"""
    for i, paper in enumerate(papers[:num_papers]):
        print(f"\nPaper {i+1}:")
        print(f"Title: {paper['title']}")
        print(f"Year: {paper['publication_year']}")

if __name__ == "__main__":
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv('IEEE_API_KEY')
    
    # Fetch papers from IEEE Visualization conference (2023-2024)
    all_papers = fetch_papers(2023, 2024, api_key, "IEEE Visualization and Visual Analytics")
    
    output_file = "output/ieee_vis_papers_2023_2024.json"
    # Print summary
    print(f"Retrieved {len(all_papers)} papers from IEEE Visualization and Visual Analytics (2023-2024)")
    
    # Save to JSON file
    save_papers_to_json(all_papers, output_file)
    
    # Display the first few papers
    display_paper_summary(all_papers, 1)