import re
from urllib.parse import urlparse 
from bs4 import BeautifulSoup

# domains we are allowed to crawl 
domains = [".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/", \
           ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences/"]

def scraper(url, resp):
    '''Args:
    url  -  The URL that was added to the frontier, and downloaded from the cache.
            It's of type str and was a url that was previously added to the frontier.
    resp -  This is the response given by the caching server for the requested URL.
            The response is an object of type Response (see utils/response.py)
            
    returns a list of urls that are scraped from the response. (An empty list for responses
    that are empty) These urls will be added to the Frontier and retrieved from the cache.
    These urls have to be filtered so that urls that do no have to be download '''
    
    links = extract_next_links(url, resp)
    links = [link for link in links if is_valid(link)]  # is_valid, 1st step in filtering the urls
    return link

def get_internal_links(cur_page, domain):
    internal_links = []
    
    # internal links begin with '/'
    for link in cur_page.findAll('a', href=re.compile(r"^(/|.*)")):
        if link.attrs["href"] != None and link.attrs["href"] not in internal_links:
            if link.attrs["href"][0] == '/':
                # only add websites we can crawl!
                if link.attrs["href"][1] == '/' and re.search(link.attrs["href"], r"^(.*("+domains[0]+"|"+\
                                                              domains[1]+"|"+domains[2]+"|"+domains[3]+"|"+\
                                                              domains[4]+").*)"):
                    internal_links.append(link.attrs['href'])   # may be //www.
                else:
                    internal_links.append(domain + link.attrs['href'])  # internal link
    return internal_links        

def get_external_links(cur_page, domain):
    external_links = []
    # external links begin with "http"
    for link in cur_page.findAll('a', href=re.compile("r^(http://|www.|https://)(.*)$")):
        if link.attr["href"] != None and link.attrs["href"] not in external_links:
            if re.search(link.attrs["href"], r"^(.*("+domains[0]+"|"+domains[1]+"|"+domains[2]+"|"+domains[3]+\
                         "|"+domains[4]+").*)"):
                external_links.append(link.attrs["href"])
    return extrernal_links
        
def extract_next_links(url, resp):
    # 200 ok status means success
    if response.status_code != 200:
        return list();
    
    # prof said to use this encoding in lecture
    #response.encoding = "utf-32"   
     
    # with sets, we can avoid duplicate links
    all_links = set()
    
    # build a domain name
    domain = "https://" + urlparse(url).netlock
    cur_page = BeautifulSoup(html)
    internal_links = get_internal_links(cur_page, domain)
    external_links = get_external_links(cur_page, domain)
    
    # add the links
    for link in external_links:   # 'a' defines a hyperlink
        all_links.add(link)
    for link in internal_links:
        all_links.add(link)

    return list(all_links)

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