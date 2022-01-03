from urllib.parse import urlparse

def domain(url):
    return urlparse(url).netloc