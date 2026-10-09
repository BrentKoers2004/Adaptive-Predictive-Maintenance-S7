from pathlib import Path

import matplotlib.pyplot as plt
import pdmdata
from pdmdata.datasets.cmapss import inventory, load
from pdmdata.datasets.cmapss.viz import plot_waveforms


OUTPUT = Path(__file__).parent / "figures"

subsets = ["FD001", "FD002", "FD003", "FD004"]

"""
This file is to get the waveform results for single engines.
"""

def main():
    pdmdata.download("cmapss")
    summary = inventory()
    print(summary)
    print(f"Train/test trajectories: {summary['units'].sum():,}; cycle rows: {summary['rows'].sum():,}")

    for subset in subsets:
        show_enginecourse(subset, 1)


def show_enginecourse(subset_name, unit_id):
    train_unit = load(subset_name, "train", unit=unit_id, with_rul=True)
    print(train_unit.select("unit_number", "cycle", "sensor_2", "sensor_11", "RUL").head())

    waveforms = plot_waveforms(train_unit, subset=subset_name)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    waveforms.savefig(OUTPUT / f"waveforms_{subset_name}_unit{unit_id}.png", dpi=100)
    plt.show()


if __name__ == "__main__":
    main()