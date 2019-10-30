import re
from multiprocessing import Pool
from grab import Grab, DataNotFound

from output import DataCtx


def get_h_scopus(author_id):
    g = Grab(transport="urllib3")
    url = "https://www.scopus.com/authid/detail.uri?authorId=%s"
    g.go(url % author_id, timeout=20)

    xpath = '//*[@id="authorDetailsHindex"]/div/div[2]/span'
    try:
        return g.doc.select(xpath).text()
    except DataNotFound:
        return "None"


def scrape_scopus(file=None):
    if not file:
        ctx = DataCtx()
        teachers_ids = ctx.select(
            'select author_id from teachers where author_id <> "None"'
        )
    else:
        with open(file) as f:
            rows = f.read()
        teachers_ids = re.findall(r"\d+", rows, flags=re.ASCII)

    pool = Pool(10)
    results = pool.map(get_h_scopus, teachers_ids)

    if not file:
        query = (
            "update teachers set h_index = ? where (h_index < ? "
            'or h_index = "None") and author_id = ?'
        )
        params = [(i, i, *j) for i, j in zip(results, teachers_ids)]
        ctx.execute_many(query, params)
    else:
        out = ["%s,%s\n" % (i, j) for i, j in zip(teachers_ids, results)]
        with open("scopus_results.txt", "w") as f:
            f.writelines(out)
