import matplotlib.pyplot as plt
from output import DataCtx


colors = [
    "purple",
    "gold",
    "deepskyblue",
    "darkorange",
    "red",
    "lightskyblue",
    "greenyellow",
    "brown",
    "black",
]


def hist_h(labels, values):
    """Plot a horizontal histogram."""
    fig, ax = plt.subplots()
    y_pos = [i for i in range(len(labels))]

    rects = ax.barh(y_pos, values, color=colors)
    ax.invert_yaxis()
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)

    plt.xlim(0, values[0] + 8)
    for rect in rects:
        h = rect.get_height()
        w = rect.get_width()
        ax.text(
            w + 5, rect.get_y() + h / 2.5, "{}".format(int(w)), ha="center",
            va="center"
        )

    plt.show()


def hist_v(labels, values, group=False):
    """Plot a vertical histogram."""
    width = 0.8
    align = "center"
    val = values
    if group:
        val = [0] * 5
        for i, j in zip(labels, values):
            val[i // 5] += j
        values = [round(i * 100 / sum(val), 2) for i in val]
        labels = ["%d" % (i * 5) for i in range(5)]
        width = 1
        align = "edge"

    fig, ax = plt.subplots()
    x_pos = [i for i in range(len(labels))]

    rects = ax.bar(x_pos, values, color=colors, width=width, align=align)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_xlabel("h-index")
    ax.set_ylabel("n")

    plt.ylim(0, max(values) + 5)
    for rect, j in zip(rects, val):
        h = rect.get_height()
        w = rect.get_width()
        text = "{}% ({})".format(h, j) if group else "%s" % h
        ax.text(rect.get_x() + w / 2, h + 2, text, ha="center", va="center")

    plt.show()


def diag_circle(x, y):
    """Plot a pie chart."""
    porcent = [100.0 * i / sum(y) for i in y]

    patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)
    labels = ["{0} - {1:1.2f} %".format(i, j) for i, j in zip(x, porcent)]

    patches, labels, dummy = zip(
        *sorted(zip(patches, labels, y), key=lambda x: x[2], reverse=True)
    )

    plt.legend(patches, labels, bbox_to_anchor=(-0.1, 1.0), fontsize=9)

    plt.show()


if __name__ == "__main__":
    labels = []
    values = []

    ctx = DataCtx()

    query1 = (
        "select institute, count(*) as num from teachers "
        "group by institute order by num desc"
    )
    query2 = (
        "select institute, count(*) as num from teachers "
        'where h_index <> "None" group by institute '
        "order by num desc"
    )
    query3 = (
        "select a.institute, b.num * 100.0 / count(*) as perc "
        "from teachers a, (%s) b where a.institute = b.institute "
        "group by a.institute order by perc desc" % query2
    )

    inst = "Институт вычислительной математики и информационных технологий"
    query4 = (
        'select unit, count(*) as num from teachers where institute = "%s" '
        "group by unit order by num desc" % inst
    )
    query5 = (
        'select unit, count(*) as num from teachers where institute = "%s" '
        'and h_index <> "None" group by unit order by num desc' % inst
    )
    query6 = (
        "select a.unit, b.num * 100.0 / count(*) as p from teachers a, (%s) b "
        'where a.unit = b.unit and institute = "%s" group by a.unit '
        "order by p desc" % (query5, inst)
    )

    query7 = (
        "select institute, round(max(h_index), 1) as max_h from teachers "
        'where h_index <> "None" group by institute order by max_h desc'
    )
    query8 = (
        "select h_index, count(*) as num from teachers "
        'where h_index <> "None" '
        "group by h_index order by h_index"
    )

    for i in ctx.select(query1):
        # Вместо query1 подставляются остальные запросы
        # Сокращение слов
        # labels.append(''.join([j[0] for j in i[0].split()]))
        labels.append(i[0])  # Если сокращение ненужно
        values.append(i[1])

    hist_h(labels, values)
    # hist_v(labels, values) # Вертикальная полосовая диаграмма
    # diag_circle(labels, values) # Круговая диаграмма
