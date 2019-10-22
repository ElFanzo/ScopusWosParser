from grab import Grab, DataNotFound
from multiprocessing import Pool
import re

from output import DataCtx


def get_teachers(page):
    g = Grab()
    url = (
        "https://kpfu.ru/main_page?p_sub=7860&p_order=1&p_id=0&p_period=on"
        "&p_rec_count=435&p_page=%d" % page
    )
    g.go(url, timeout=90)

    teachers = g.doc.select(
        '//*[@id="ss_content"]/div[2]/div/div[2]/table[2]/tr/td/span/a'
    )

    result = ""
    for man in teachers:
        g.go(man.select("@href").text())
        try:
            info = g.doc.select(
                '//*[@id="ss_content"]/div/div/div[2]/div[2]/div[1]/div/table'
            ).text()
        except DataNotFound:
            pass
        else:
            try:
                kfu = man.select("../following-sibling::*").text().split("/")
                inst = kfu[1].strip()
                unit = kfu[-1].strip() if len(kfu) > 2 else "None"
            except (DataNotFound, IndexError):
                inst = unit = "None"

            resid = re.search(r"rid/([A-Z]-\d{4}-\d{4})", info, flags=re.ASCII)
            authid = re.search(r"authorId=(\d+)", info, flags=re.ASCII)

            if resid or authid:
                authid = authid.group(1) if authid else "None"
                resid = resid.group(1) if resid else "None"
                result += "|".join([man.text(), inst, unit, authid, resid]) + "/"

    return result[:-1] if result else None


def scrape_kfu():
    ctx = DataCtx()
    pool = Pool(10)

    results = pool.map(get_teachers, [i for i in range(1, 11)])
    results = [tuple(j.split("|")) for i in results for j in i.split("/")]

    query = """ create table if not exists teachers
                    (name text, institute text, unit text,
                    author_id text, researcher_id text, h_index integer) """
    ctx.execute(query)
    query = "insert into teachers values (?, ?, ?, ?, ?, Null)"
    ctx.execute_many(query, results)
