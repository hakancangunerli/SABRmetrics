# Description: This script generates a 3x3 grid plot with 9 zones and a 2x2 grid plot with 4 zones.
import matplotlib.pyplot as plt
import numpy as np



def zone_plot(nine_zone_data: np.ndarray, four_zone_data: np.ndarray):
    fig, ax = plt.subplots(figsize=(5, 5))
    cmap_4 = plt.cm.YlOrRd
    norm_4 = plt.Normalize(vmin=min(four_zone_data), vmax=max(four_zone_data))

    four_zone_positions = [(-1, -1), (2, -1), (-1, 2), (2, 2)]


    four_zone_text_positions = [
        (-0.25, 4.75),
        (4.25, 4.75),
        (-0.25, -0.75),
        (4.25, -0.75),
    ]

    for value, pos, text_pos in zip(
        four_zone_data, four_zone_positions, four_zone_text_positions
    ):
        color = cmap_4(norm_4(value))
        rect = plt.Rectangle(
            pos, 3, 3, facecolor=color, edgecolor="black", linewidth=2, alpha=0.3
        )
        ax.add_patch(rect)
        ax.text(
            text_pos[0],
            text_pos[1],
            str(int(value)),
            va=("top" if text_pos[1] > 0 else "bottom"),
            ha=("left" if text_pos[0] > 0 else "right"),
            color="black",
            fontsize=12,
            fontweight="bold",
        )


    cmap_9 = plt.cm.RdYlBu_r
    norm_9 = plt.Normalize(
        vmin=min(nine_zone_data.flatten()), vmax=max(nine_zone_data.flatten())
    )


    for i in range(3):
        for j in range(3):
            value = nine_zone_data[i, j]
            color = cmap_9(norm_9(value))

            rect = plt.Rectangle(
                (j + 0.5, 2.5 - i),
                1,
                1,
                facecolor=color,
                edgecolor="black",
                linewidth=2,
                alpha=0.7,
            )
            ax.add_patch(rect)
            text_color = "white" if norm_9(value) > 0.5 else "black"
            ax.text(
                j + 1,
                2.5 - i + 0.5,
                str(int(value)),
                va="center",
                ha="center",
                color=text_color,
                fontsize=14,
                fontweight="bold",
            )


    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.5, 5.5)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()