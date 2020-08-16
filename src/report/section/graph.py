import matplotlib.pyplot as plt

from textwrap import dedent

from base.crawler import CrawledData


class GraphGenerator():
    def _config_graph(self, **kwargs) -> str:
        raise NotImplementedError()

    def generate_graph(self, data: CrawledData) -> str:
        config = self._config_graph()
        
        _, ax = plt.subplots(figsize=(8, 4), subplot_kw={"aspect": "equal"})
        pie_legend = ["0", "1-2", "3-4", "5-6", "7+"]
        pie_cnt = [0, 0, 0, 0, 0]

        cnt_list = [value for value in data.values()]
        for cnt in cnt_list:
            if cnt < 1:
                pie_cnt[0] += 1
            elif cnt < 3:
                pie_cnt[1] += 1
            elif cnt < 5:
                pie_cnt[2] += 1
            elif cnt < 7:
                pie_cnt[3] += 1
            else:
                pie_cnt[4] += 1
        pie_cnt_sum = sum(pie_cnt)

        wedges, _, autotexts = ax.pie(
            pie_cnt, startangle=90, counterclock=False, autopct="", textprops={"color": "w"})
        for i, a in enumerate(autotexts):
            pct = pie_cnt[i]*100/pie_cnt_sum
            if pct > 10:
                a.set_text(f"{pie_cnt[i]}\n({pct:.1f}%)")
        ax.legend(wedges, pie_legend, title=config["box_title"],
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=10, weight="roman")
        ax.set_title(config["title"])
        plt.savefig(f"result/asset/pie_graph.png", dpi=400, bbox_inches="tight")

        return dedent(f"""
            ## Graph
            <img src="asset/pie_graph.png" alt="pie" width="60%">
        """)
