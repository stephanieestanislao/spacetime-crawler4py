import re #was
from urllib.parse import urlparse #was
from bs4 import BeautifulSoup

def scraper(url : str, resp : utils.response.Response) -> list:
    '''Args:
    url  -  The URL that was added to the frontier, and downloaded from the cache.
            It's of type str and was a url that was previously added to the frontier.
    resp -  This is the response given by the caching server for the requested URL.
            The response is an object of type Response (see utils/response.py)
            
    returns a list of urls that are scraped from the response. (An empty list for responses
    that are empty) These urls will be added to the Frontier and retrieved from the cache.
    These urls have to be filtereed so that urls that do no have to be download '''
    
    links = extract_next_links(url, resp)
    links = [link for link in links if is_valid(link)]  # is_valid, 1st step in filtering the urls
    return link

def extract_next_links(url, resp):
    # open url
    try:
        html = urlopen(url)
    # page/server not found
    except (HTTPError, URLError):
        return list()
    
    cur_page = BeautifulSoup(html)
    return list()

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise