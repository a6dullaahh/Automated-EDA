import matplotlib.pyplot as plt


def correlation_matrix(df):
    return df.select_dtypes(include="number").corr()


def plot_correlation_heatmap(df):
    corr = correlation_matrix(df)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    ax.set_title("Correlation Heatmap")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    return fig


def plot_histogram(df, column, bins=30):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df[column].dropna(), bins=bins, color="#4C72B0", edgecolor="white")
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig


def plot_box(df, column):
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.boxplot(df[column].dropna(), vert=True)
    ax.set_title(f"Boxplot of {column}")
    ax.set_ylabel(column)
    fig.tight_layout()
    return fig


def plot_bar_categorical(df, column, top_n=20):
    counts = df[column].value_counts().nlargest(top_n)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(counts.index.astype(str), counts.values, color="#55A868")
    ax.set_title(f"Top values in {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_scatter(df, x, y, color=None):
    fig, ax = plt.subplots(figsize=(7, 5))
    if color:
        categories = df[color].astype("category")
        codes = categories.cat.codes
        scatter = ax.scatter(df[x], df[y], c=codes, cmap="tab10", alpha=0.8)
        handles, _ = scatter.legend_elements()
        ax.legend(handles, categories.cat.categories, title=color, bbox_to_anchor=(1.05, 1), loc="upper left")
    else:
        ax.scatter(df[x], df[y], alpha=0.8, color="#4C72B0")
    ax.set_title(f"{y} vs {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.tight_layout()
    return fig


def plot_pairplot(df, columns):
    n = len(columns)
    fig, axes = plt.subplots(n, n, figsize=(3 * n, 3 * n))
    for i, col_i in enumerate(columns):
        for j, col_j in enumerate(columns):
            ax = axes[i, j] if n > 1 else axes
            if i == j:
                ax.hist(df[col_i].dropna(), bins=20, color="#4C72B0")
            else:
                ax.scatter(df[col_j], df[col_i], s=10, alpha=0.6, color="#4C72B0")
            if i == n - 1:
                ax.set_xlabel(col_j)
            if j == 0:
                ax.set_ylabel(col_i)
    fig.suptitle("Pairwise relationships")
    fig.tight_layout()
    return fig
