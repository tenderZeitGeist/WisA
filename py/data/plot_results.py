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

###
#  scatter cpu_emissions/runtime
###

df["datatype"] = df["file_name"].apply(
    lambda name: next((t for t in ("int", "float", "string") if t in name), "unknown")
)

color_map = {"Python": "orange", "C++": "blue"}
marker_map = {"string": "o", "float": "X", "int": "D"}

df["efficiency_score"] =  df["cpu_emissions"] / df["time_in_milliseconds"]
grouped_df = (
    df.groupby(["algorithm", "implementation", "datatype"])[["time_in_milliseconds", "efficiency_score"]]
    .mean()
    .reset_index()
)

algorithms = grouped_df["algorithm"].unique()

for algorithm in algorithms:
    subset = grouped_df[grouped_df["algorithm"] == algorithm]
    
    fig, ax = plt.subplots(figsize=(7, 5))
    
    for _, row in subset.iterrows():
        ax.scatter(
            row["time_in_milliseconds"],
            row["efficiency_score"],
            color=color_map.get(row["implementation"], "gray"),
            marker=marker_map.get(row["datatype"], "x"),
            s=100,
            alpha=0.8
        )

    ax.set_title(f"{algorithm} - Time vs CPU Emissions Rate", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("CPU Emission rate (kg CO$_2$eq/ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2e}'))

    impl_legend = [Line2D([0], [0], color=color, lw=4, label=impl) for impl, color in color_map.items()]
    type_legend = [Line2D([0], [0], marker=marker, color='black', linestyle='None',
                        markersize=10, label=dtype) for dtype, marker in marker_map.items()]

    ax.legend(
        handles=impl_legend + type_legend,
        title="Legend",
        loc="lower left",
        bbox_to_anchor=(1.02, 0),
        borderaxespad=0
    )

    plt.tight_layout(rect=[0, 0, 1, 1])

    safe_name = algorithm.replace(" ", "_").lower()
    plt.savefig(os.path.join(output_dir, f"{safe_name}.jpg"), format="jpg", dpi=300)

    plt.show()



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
plt.show()

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

plt.show()

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
plt.show()

# Python
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
plt.show()

####
# Emissions per ms
####

#df["efficiency_score"] =  df["cpu_emissions"] / df["time_in_milliseconds"]

#grouped = df.groupby(["algorithm", "datatype"])["efficiency_score"].mean().unstack()

#plt.figure(figsize=(10, 6))

#grouped.plot(kind="bar", figsize=(10, 6), colormap="viridis")
#plt.ylabel("Emission per ms (kg CO$_2$eq/ms)")
#plt.xlabel("")
#plt.title("Emission-Efficiency by Algorithm and Datatype", fontsize=14, fontweight='bold')
#plt.xticks(rotation=45)
#plt.tight_layout()

#plt.savefig(os.path.join(output_dir, "emission-efficiency_bar_chart.jpg"), format="jpg", dpi=300)

#plt.show()