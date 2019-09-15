from teachers import scrape_kfu
from wos import scrape_wos
from scopus import scrape_scopus


if __name__ == "__main__":
    scrape_kfu()
    scrape_wos()
    scrape_scopus()
