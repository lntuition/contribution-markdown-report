import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from textwrap import dedent
from typing import Tuple

from base.type import ConfigType


class GraphGenerator():
    def _config_graph(self) -> ConfigType:
        raise NotImplementedError()

    def _get_graph_path(self, config: ConfigType, filename: str) -> Tuple[str, str]:
        return (
            f"{config['root_path']}/{config['asset_dir']}/{filename}",
            f"{config['asset_dir']}/{filename}"
        )

    def _save_count_based_graph(self, config: ConfigType, data: pd.DataFrame) -> str:
        save_path, src_path = self._get_graph_path(
            config=config, filename="count_based_graph.png")

        daily_count = pd.cut(
            data["count"],
            bins=[-1, 0, 2, 4, 6, np.inf],
            labels=["0", "1-2", "3-4", "5-6", "7+"]
        )
        total_count = len(daily_count.index)

        ax = sns.countplot(x=daily_count, palette="pastel")
        ax.set(title=config["count_based_title"],
               xlabel=config["count_based_x"],
               ylabel=config["count_based_y"])
        for p in ax.patches:
            count = p.get_height()
            ax.annotate(
                f"{count:.0f} ({100 * count / total_count:.1f}%)",
                (p.get_x() + p.get_width() / 2, count + 0.3),
                ha="center"
            )
        sns.set_style("whitegrid")
        sns.despine(top=True, right=True)

        plt.savefig(save_path, dpi=200, bbox_inches="tight")
        return src_path

    def generate_graph(self, data: pd.DataFrame, root_path: str, asset_dir: str) -> str:
        config = {
            "root_path": root_path,
            "asset_dir": asset_dir,
            **self._config_graph()
        }

        return dedent(f"""
            ## {config["section_name"]}
            <img src="{self._save_count_based_graph(config, data)}" width="45%">
        """)
