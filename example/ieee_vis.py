from ieee_search.core.xploreapi import XPLORE
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize with your IEEE API key
api_key = os.getenv('IEEE_API_KEY')
xplore = XPLORE(api_key)

# Search for papers from IEEE Visualization conference
xplore.publicationTitle("IEEE Visualization")

# Optional: Set additional search parameters
xplore.maximumResults(100)  # Get up to 100 results (max is 200)
xplore.publicationYear("2023")  # Limit to specific year
# xplore.authorText("John Doe")  # Search by author
# xplore.queryText("visual analytics")  # Search by keywords

# Optional: Configure result format
xplore.setDataFormat("object")  # Returns JSON as Python object instead of raw string

# Execute the search
results = xplore.callAPI()

# If you used "object" data format, you can access the results directly
if xplore.outputDataFormat == "object":
    # Access the articles
    if "articles" in results:
        for article in results["articles"]:
            print(f"Title: {article.get('title', 'N/A')}")
            print(f"Authors: {', '.join(author.get('full_name', 'N/A') for author in article.get('authors', {}).get('authors', []))}")
            print(f"DOI: {article.get('doi', 'N/A')}")
            print("---")