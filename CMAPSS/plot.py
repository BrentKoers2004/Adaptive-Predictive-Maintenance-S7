import matplotlib.pyplot as plt
import numpy as np

def plot_results(stream, ys, pred, abs_error):
    units = stream["unit_number"].to_numpy()
    cycles = stream["cycle"].to_numpy()

    fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")

    # 1. Foutenstroom: wat een driftdetector straks binnenkrijgt
    ax = axes[0, 0]
    ax.plot(abs_error, linewidth=0.6)
    for start in np.where(cycles == 1)[0]:          # begin van elke nieuwe motor
        ax.axvline(start, color="grey", alpha=0.3, linewidth=0.8)
    ax.set(title="Foutenstroom (grijze lijn = nieuwe motor)",
           xlabel="Positie in de stroom (cycli)", ylabel="Absolute fout (cycli)")

    # 2. Voorspeld tegen werkelijk: op de stippellijn is het perfect
    ax = axes[0, 1]
    ax.scatter(ys, pred, s=5, alpha=0.2)
    top = max(ys.max(), pred.max())
    ax.plot([0, top], [0, top], "k--", linewidth=1)
    ax.set(title="Voorspeld vs. werkelijk",
           xlabel="Werkelijke RUL (cycli)", ylabel="Voorspelde RUL (cycli)")

    # 3. Fout per levensfase: is de fout groter als de motor nog lang meegaat?
    ax = axes[1, 0]
    ax.scatter(ys, abs_error, s=5, alpha=0.2)
    ax.set(title="Fout tegen werkelijke RUL",
           xlabel="Werkelijke RUL (cycli)", ylabel="Absolute fout (cycli)")

    # 4. Eén motor van begin tot falen
    ax = axes[1, 1]
    unit = units[0]
    mask = units == unit
    ax.plot(cycles[mask], ys[mask], linewidth=2, label="werkelijk")
    ax.plot(cycles[mask], pred[mask], linewidth=1, label="voorspeld")
    ax.set(title=f"Motor {unit}: werkelijke en voorspelde RUL",
           xlabel="Cyclus", ylabel="RUL (cycli)")
    ax.legend()

    for ax in axes.flat:
        ax.grid(alpha=0.3)

    fig.savefig("resultaten_randomforest.png", dpi=120)
    plt.show()