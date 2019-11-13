from scopus import scrape_scopus
from teachers import scrape_kfu
from wos import scrape_wos


if __name__ == "__main__":
    scrape_kfu()
    scrape_wos()
    scrape_scopus()
