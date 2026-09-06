from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DATA_DIR = Path(__file__).resolve().parent / ".." / "data"


def plot_data_files():
	data_files = sorted(DATA_DIR.glob("*.txt"))
	if not data_files:
		raise FileNotFoundError(f"No .txt files found in {DATA_DIR}")

	figure, axes = plt.subplots(
		len(data_files),
		1,
		figsize=(9, 3.5 * len(data_files)),
		squeeze=False,
	)

	for axis, data_file in zip(axes.flat, data_files):
		data = np.loadtxt(data_file)
		if data.ndim != 2 or data.shape[1] % 2:
			raise ValueError(
				f"{data_file.name} must contain pairs of x/y columns"
			)

		for column in range(0, data.shape[1], 2):
			axis.semilogx(
				data[:, column],
				data[:, column + 1],
				label=f"columns {column + 1}/{column + 2}",
			)

		axis.set_title(data_file.stem)
		axis.set_xlabel("Frequency (Hz)")
		axis.set_ylabel("Magnitude")
		axis.grid(True, which="both", alpha=0.3)
		axis.legend()

	figure.tight_layout()
	if plt.get_backend().lower() == "agg":
		output_file = Path(__file__).resolve().parent / "plots.png"
		figure.savefig(output_file, dpi=150)
		print(f"Saved plot to {output_file}")
	else:
		plt.show()


if __name__ == "__main__":
	plot_data_files()
