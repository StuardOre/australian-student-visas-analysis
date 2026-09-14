"""
Shared chart styling for the Australian Student Visa analysis.

Provides a consistent professional theme (palette, fonts, sizes), a chart
saver that injects a data-source caption, and small helpers for annotations.
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
PALETTE = {
    "higher_ed": "#1f77b4",
    "vet": "#ff7f0e",
    "elicos": "#2ca02c",
    "other": "#7f7f7f",
    "granted": "#2ca02c",
    "refused": "#d62728",
    "accent": "#d62728",
    "grid": "#dddddd",
}

PLOT_DPI = 300
FIGWIDTH = 14
FIGHEIGHT = 7

FONT_FAMILY = "DejaVu Sans"  # default matplotlib font, consistent across OSes


def apply_theme():
    """Apply the shared matplotlib theme (fonts, grid, colors)."""
    plt.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.size": 12,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            "axes.labelsize": 13,
            "axes.grid": True,
            "grid.alpha": 0.6,
            "grid.linestyle": "--",
            "grid.color": PALETTE["grid"],
            "figure.dpi": PLOT_DPI,
            "savefig.dpi": PLOT_DPI,
            "legend.frameon": True,
        }
    )


def save_chart(fig, path, source_note=None):
    """Save a figure with an optional data-source caption at the bottom.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to save.
    path : Path
        Output PNG path.
    source_note : str, optional
        e.g. "Source: Department of Home Affairs, Subclass 500 reports (lock date 2026-07-31)".
        If provided, it is rendered as a small italic caption.
    """
    if source_note:
        fig.text(
            0.01, 0.01, source_note,
            ha="left", va="bottom", fontsize=8, style="italic", color="#555555",
        )
    fig.savefig(path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)


def annotate_point(ax, x, y, text, offset=(8, 8), **kwargs):
    """Annotate a data point with an arrow and text."""
    ax.annotate(
        text,
        xy=(x, y),
        xytext=offset,
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8),
        fontsize=11,
        fontweight="bold",
        color="#333333",
        **kwargs,
    )


def tidy_x_ticks(ax, rotate=45):
    """Rotate x ticks and limit their count for readability."""
    plt.xticks(rotation=rotate)
    ax.xaxis.set_major_locator(MaxNLocator(prune="both"))