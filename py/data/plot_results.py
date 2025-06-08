import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
import pandas as pd

file_path = Path(__file__).resolve().parent.parent.parent / "results" / "sorting_info.csv"
df = pd.read_csv(file_path)

df["datatype"] = df["file_name"].apply(lambda name: Path(name).stem.split('.')[0])

color_map = {"Python": "orange", "C++": "blue"}
marker_map = {"strings": "o", "floats": "s", "ints": "D"}

algorithms = df["algorithm"].unique()
n_algorithms = len(algorithms)

fig, axes = plt.subplots(1, n_algorithms, figsize=(6 * n_algorithms, 5), sharey=True)

if n_algorithms == 1:
    axes = [axes]

for ax, algorithm in zip(axes, algorithms):
    subset = df[df["algorithm"] == algorithm]

    for (impl, dtype), group in subset.groupby(["implementation", "datatype"]):
        ax.scatter(
            group["time_in_milliseconds"],
            group["emissions"],
            color=color_map.get(impl, "gray"),
            marker=marker_map.get(dtype, "x"),
            s=100,
            alpha=0.8
        )

    ax.set_title(algorithm)
    ax.set_xlabel("Time (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)

axes[0].set_ylabel("Emissions (kg CO₂eq)")
fig.suptitle("Comparison: Time vs Emissions per Algorithm", fontsize=16)

impl_legend = [Line2D([0], [0], color=color, lw=4, label=impl) for impl, color in color_map.items()]
type_legend = [Line2D([0], [0], marker=marker, color='black', linestyle='None',
                      markersize=10, label=dtype) for dtype, marker in marker_map.items()]

fig.legend(handles=impl_legend, title="Implementation", loc="lower center", bbox_to_anchor=(0.115, -0.0), ncol=1)
fig.legend(handles=type_legend, title="Data Type", loc="lower center", bbox_to_anchor=(0.05, -0.0), ncol=1)

plt.tight_layout(rect=[0, 0.2, 1, 1]) 

plt.show()
