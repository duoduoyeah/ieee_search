import json


class Paper:
    """A class representing a scientific paper from IEEE Xplore."""

    def __init__(
        self,
        title="N/A",
        publication_title="N/A",
        publication_year="N/A",
        doi="N/A",
        abstract="N/A",
        keywords="N/A",
        authors=None,
    ):
        self.title = title
        self.publication_title = publication_title
        self.publication_year = publication_year
        self.doi = doi
        self.abstract = abstract
        self.keywords = keywords
        self.authors = authors or []

    def to_dict(self):
        """Convert Paper object to dictionary representation."""
        return {
            "title": self.title,
            "publication_title": self.publication_title,
            "publication_year": self.publication_year,
            "doi": self.doi,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "authors": self.authors,
        }

    @classmethod
    def from_dict(cls, paper_dict):
        """Create a Paper object from a dictionary."""
        return cls(
            title=paper_dict.get("title", "N/A"),
            publication_title=paper_dict.get("publication_title", "N/A"),
            publication_year=paper_dict.get("publication_year", "N/A"),
            doi=paper_dict.get("doi", "N/A"),
            abstract=paper_dict.get("abstract", "N/A"),
            keywords=paper_dict.get("keywords", "N/A"),
            authors=paper_dict.get("authors", []),
        )


def extract_paper_metadata(articles):
    """Extract paper metadata from IEEE Xplore API results and return Paper objects."""
    papers = []
    for article in articles:
        author_list = []

        # Extract authors
        if "authors" in article and "authors" in article["authors"]:
            for author in article["authors"]["authors"]:
                author_list.append(
                    {
                        "name": author.get("full_name", "N/A"),
                        "affiliation": author.get("affiliation", "N/A"),
                    }
                )

        # Create a Paper object
        paper = Paper(
            title=article.get("title", "N/A"),
            publication_title=article.get("publication_title", "N/A"),
            publication_year=article.get("publication_year", "N/A"),
            doi=article.get("doi", "N/A"),
            abstract=article.get("abstract", "N/A"),
            keywords=article.get("author_terms", "N/A"),
            authors=author_list,
        )

        papers.append(paper)
    return papers


def save_papers_to_json(papers, filename):
    """Save a list of Paper objects to a JSON file."""
    papers_dict = [paper.to_dict() for paper in papers]
    with open(filename, "w") as f:
        json.dump(papers_dict, f, indent=2)


def load_papers_from_json(filename):
    """Load a list of Paper objects from a JSON file."""
    with open(filename, "r") as f:
        papers_dict = json.load(f)

    return [Paper.from_dict(paper_dict) for paper_dict in papers_dict]
