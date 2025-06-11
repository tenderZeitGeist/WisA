import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
import pandas as pd
import seaborn as sns
sns.set_theme(style="whitegrid")

output_dir = "py/plots/one_million"
os.makedirs(output_dir, exist_ok=True)

file_path = Path(__file__).resolve().parent.parent.parent / "results" / "sorting_info_linux_one_million.csv"
df = pd.read_csv(file_path)

df["datatype"] = df["file_name"].apply(
    lambda name: next((t for t in ("int", "float", "string") if t in name), "unknown")
)

####
# runtime / language / algorithm
####

grouped = (
    df.groupby(["algorithm", "implementation", "datatype"])["time_in_milliseconds"]
    .mean()
    .reset_index()
)

grouped["label"] = grouped["implementation"] + " | " + grouped["datatype"]

plt.figure(figsize=(12, 6))
sns.barplot(
    data=grouped,
    x="algorithm",
    y="time_in_milliseconds",
    hue="label",
    palette="Paired"
)

plt.ylabel("Average Runtime (ms)")
plt.title("Runtime á Algorithm, Language & Datatype", fontsize=14, fontweight='bold')
plt.legend(title="Language | Datatype", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()

plt.savefig(os.path.join(output_dir, "cpu_energy_grouped_bar_chart_detailed.jpg"), format="jpg", dpi=300)
plt.close()


####
# energy / language / algorithm
####

grouped = (
    df.groupby(["algorithm", "implementation", "datatype"])["cpu_energy"]
    .mean()
    .reset_index()
)

grouped["label"] = grouped["implementation"] + " | " + grouped["datatype"]

plt.figure(figsize=(12, 6))
sns.barplot(
    data=grouped,
    x="algorithm",
    y="cpu_energy",
    hue="label",
    palette="Paired"
)

plt.ylabel("Average CPU-Energy (kWh)")
plt.title("CPU-Energy á Algorithm, Language & Datatype", fontsize=14, fontweight='bold')
plt.legend(title="Language | Datatype", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()

plt.savefig(os.path.join(output_dir, "cpu_energy_grouped_bar_chart_detailed.jpg"), format="jpg", dpi=300)
plt.close()


###
#  bubble cpu_emissions/runtime
###

color_map = {"Python": "orange", "C++": "blue"}
marker_map = {"string": "o", "float": "X", "int": "D"}

df["time_s"] = (df["time_in_milliseconds"] / 1000)
df["efficiency_score"] = df["cpu_emissions"] / df["time_s"]
grouped = (
    df.groupby(["algorithm", "implementation", "datatype"])[
        ["time_in_milliseconds", "efficiency_score", "cpu_emissions"]
    ]
    .mean()
    .reset_index()
)
grouped["time_s"] = grouped["time_in_milliseconds"] / 1000

grouped["bubble_size"] = grouped["cpu_emissions"] * 1e9 # one million scale = 1e9, ten million 1e8

color_map = {"Python": "orange", "C++": "blue"}

for algo in grouped["algorithm"].unique():
    subset = grouped[grouped["algorithm"] == algo]

    fig, ax = plt.subplots(figsize=(10, 7))
    for _, row in subset.iterrows():
        ax.scatter(
            row["time_s"],
            row["efficiency_score"],
            s=row["bubble_size"],
            color=color_map.get(row["implementation"], "gray"),
            alpha=0.6,
            edgecolor="black",
            linewidth=0.5
        )
        ax.text(
            row["time_s"],
            row["efficiency_score"],
            row["datatype"],
            ha="center",
            va="center",
            fontsize=9,
            color="black",
            weight="bold"
        )

    ax.set_title(f"{algo} - CPU Efficiency by Datatype", fontsize=15, fontweight='bold')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CPU Emission Rate (kg CO$_2$eq/s)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.2e}"))
    ax.grid(True, linestyle='--', alpha=0.7)

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', label=impl,
                   markerfacecolor=color, markersize=10)
        for impl, color in color_map.items()
    ]
    ax.legend(handles=handles, title="Implementation", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"bubble_{algo.replace(' ', '_').lower()}.jpg"), dpi=300)
    plt.close()

###
#  Bar chart cpu emission/algorithm
###

grouped = df.groupby(["algorithm", "implementation"])["cpu_emissions"].mean().unstack()

fig, ax = plt.subplots(figsize=(8, 5))
grouped.plot(kind="bar", ax=ax, color=["tab:blue", "tab:orange"])

ax.set_title("CPU CO$_2$ Emissions per Algorithm", fontsize=14, fontweight='bold')
ax.set_ylabel("Emissions (kg CO$_2$eq)")
ax.set_xlabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Implementation")
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bar_chart.jpg"), format="jpg", dpi=300)
plt.close()

####
# Energy per ms
####

df["efficiency_score"] =  df["cpu_energy"] / df["time_in_milliseconds"]

grouped = df.groupby(["algorithm", "datatype"])["efficiency_score"].mean().unstack()

plt.figure(figsize=(10, 6))

grouped.plot(kind="bar", figsize=(10, 6), colormap="viridis")
plt.ylabel("Energy per ms (kWh/ms)")
plt.xlabel("")
plt.title("Energy-Efficiency by Algorithm and Datatype", fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(output_dir, "energy-efficiency_bar_chart.jpg"), format="jpg", dpi=300)
plt.close()

####
# CPU Emission per algorithm
####

cpp_df = df[df["implementation"] == "C++"]
cpp_grouped = (
    cpp_df.groupby(["algorithm", "datatype"])["cpu_emissions"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=cpp_grouped,
    x="algorithm",
    y="cpu_emissions",
    hue="datatype",
    palette="Set1"
)
plt.title("CPU-Emissions (C++) by Algorithm and Datatype", fontsize=14, fontweight='bold')
plt.xlabel("")
plt.ylabel("CPU-Emissions (kg CO$_2$eq)")
plt.legend(title="Datatype", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "emissions-cpp_bar_chart.jpg"), format="jpg", dpi=300)
plt.close()

py_df = df[df["implementation"] == "Python"]
py_grouped = (
    py_df.groupby(["algorithm", "datatype"])["cpu_emissions"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=py_grouped,
    x="algorithm",
    y="cpu_emissions",
    hue="datatype",
    palette="Set2"
)
plt.title("CPU-Emissions (Python) by Algorithm and Datatype", fontsize=14, fontweight='bold')
plt.xlabel("")
plt.ylabel("CPU-Emissionen (kg CO$_2$eq)")
plt.legend(title="Datentyp", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "emissions-python_bar_chart.jpg"), format="jpg", dpi=300)
plt.close()