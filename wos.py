import re
from multiprocessing import Pool
from grab import Grab, DataNotFound

from output import DataCtx


def get_h_wos(id_):
    g = Grab()
    g.go("https://apps.webofknowledge.com/WOS_GeneralSearch_input.do")

    try:
        g.doc.set_input_by_id(_id="value(input1)", value=id_)
    except DataNotFound:
        print("Search is not available! It's necessary to login.")
        raise PermissionError
    g.doc.set_input_by_id(_id="select1", value="AI")
    g.submit()

    try:
        href = g.doc.select(
            '//*[@id="view_citation_report_image"]/div/div/a/@href'
        ).text()
    except DataNotFound:
        return "None"

    g.go("https://apps.webofknowledge.com%s" % href)

    return g.doc.select('//*[@id="H_INDEX"]').text()


def scrape_wos(file=None):
    if not file:
        ctx = DataCtx()
        teachers_ids = ctx.select(
            'select researcher_id from teachers where researcher_id <> "None"'
        )
    else:
        with open(file) as f:
            rows = f.read()
        teachers_ids = re.findall(r"[A-Z]-\d{4}-\d{4}", rows, flags=re.ASCII)

    pool = Pool(8)
    results = pool.map(get_h_wos, teachers_ids)

    if not file:
        params = [(i, *j) for i, j in zip(results, teachers_ids)]
        ctx.execute_many(
            "update teachers set h_index = ? where researcher_id = ?", params
        )
    else:
        out = ["%s,%s\n" % (i, j) for i, j in zip(teachers_ids, results)]
        with open("wos_results.txt", "w") as f:
            f.writelines(out)
