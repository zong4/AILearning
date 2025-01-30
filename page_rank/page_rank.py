import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # Create a dictionary to store the probability distribution
    probability_distribution = {}
    
    # If the page has no links, return a probability distribution that chooses randomly from all pages
    if len(corpus[page]) == 0:
        for page in corpus:
            probability_distribution[page] = 1 / len(corpus)
        return probability_distribution
    
    # Calculate the probability of choosing a link at random from all pages
    for page in corpus:
        probability_distribution[page] = (1 - damping_factor) / len(corpus)

    # Calculate the probability of choosing a link at random linked to the page
    for linked_page in corpus[page]:
        probability_distribution[linked_page] += damping_factor / len(corpus[page])
    
    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create a dictionary to store the number of times each page is visited
    page_visits = {page: 0 for page in corpus}
    
    # Choose a random page to start
    current_page = random.choice(list(corpus.keys()))
    
    # Visit n pages
    for i in range(n):
        page_visits[current_page] += 1
        
        # Get the probability distribution for the current page
        probability_distribution = transition_model(corpus, current_page, damping_factor)
        
        # Choose the next page based on the probability distribution
        current_page = random.choices(list(probability_distribution.keys()), weights=probability_distribution.values(), k=1)[0]
    
    # Calculate the PageRank values
    page_rank = {page: page_visits[page] / n for page in corpus}
    
    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Create a dictionary to store the PageRank values
    page_rank = {page: 1 / len(corpus) for page in corpus}
    
    # Create a dictionary to store the new PageRank values
    new_page_rank = {page: 0 for page in corpus}
    
    # Create a boolean variable to check if the PageRank values have converged
    converged = False
    
    # Iterate until the PageRank values converge
    while not converged:
        
        # Calculate the new PageRank values
        for page in corpus:
            new_page_rank[page] = (1 - damping_factor) / len(corpus)
            for linking_page in corpus:
                if page in corpus[linking_page]:
                    new_page_rank[page] += damping_factor * page_rank[linking_page] / len(corpus[linking_page])
        
        # Check if the PageRank values have converged
        if all(abs(new_page_rank[page] - page_rank[page]) < 0.001 for page in corpus):
            converged = True
        
        # Update the PageRank values
        page_rank = new_page_rank.copy()
    
    return page_rank

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (damping factor = {DAMPING}, samples = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

main()
