# Cascode Differential Pair in SKY130

This repository contains ngspice netlists for exploring MOSFET operating points and a cascode differential-pair amplifier using the open-source SKY130A PDK.

The examples progress from individual NMOS and PMOS devices to an ideal-tail cascode differential pair, and finally to a version with an NMOS current-source tail load. The final circuit includes differential-mode gain, common-mode gain, and CMRR analysis.

## Requirements

- ngspice
- Python 3
- NumPy
- Matplotlib
- The SKY130A PDK installed at:

	`/usr/local/share/pdk/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice`

The netlists use the SKY130 typical-typical (`tt`) model corner. If the PDK is installed elsewhere, update the `.lib` path in the netlists.

Install the Python plotting dependencies with:

```bash
python3 -m pip install numpy matplotlib
```

## Directory layout

```text
Diffpair/
├── IdealDiff/
│   ├── diffpair.spice       # DC operating point of the cascode pair
│   └── diff_ac.spice        # AC gain and phase response
├── MosLoad/
│   ├── Mosload.spice        # DC operating point with an NMOS tail load
│   ├── Mosload_ac.spice     # Differential/common-mode AC analysis and CMRR
│   ├── data/                # AC data written by Mosload_ac.spice
│   │   ├── cm.txt
│   │   ├── cmrr.txt
│   │   └── diff.txt
│   └── PythonPlot/
│       └── plot.py          # Plots all data files in ../data/
├── Nmos/
│   ├── bulkfloat.spice      # NMOS operating-point parameters
│   └── log.txt              # Saved NMOS results used for sizing
│── Pmos/
│	└── pmos.spice           # PMOS operating-point parameters
└── readme.md				 # Here !!! 
```

## Circuit overview

The differential pair uses two cascoded NMOS input branches and PMOS cascode loads. The two inputs share the tail node `Nbias` and are biased at 1.245 V. The supply is 1.8 V.

The device multiplicities in the differential-pair netlists are based on the operating-point values recorded in `Nmos/log.txt`:

| Device role | Reference current | Approximate `gm` | Approximate `gds` |
| --- | ---: | ---: | ---: |
| Input NMOS, `L=0.15` | 0.3597 mA | 1.797 mS | 0.308 mS |
| Cascode NMOS, `L=0.15` | 0.3719 mA | 1.807 mS | 0.318 mS |
| Tail NMOS, `L=0.30` | 0.1134 mA | 0.733 mS | 0.187 mS |

## Running the simulations

The repository contains the netlists in the nested `Diffpair/` directory. Run commands from `/path/to/Diffpair/Diffpair` (the directory containing `IdealDiff/`, `MosLoad/`, `Nmos/`, and `Pmos/`).

### Individual MOSFET checks

```bash
ngspice -b Nmos/bulkfloat.spice -o Nmos/nmos.out
ngspice -b Pmos/pmos.spice -o Pmos/pmos.out
```

Both netlists perform an operating-point analysis and print device quantities such as threshold voltage, transconductance, and output conductance.

### Cascode differential pair

Run the DC operating-point version:

```bash
ngspice -b IdealDiff/diffpair.spice -o IdealDiff/diffpair.out
```

Run the AC version:

```bash
ngspice -b IdealDiff/diff_ac.spice -o IdealDiff/diff_ac.out
```

The AC netlist sweeps from 1 Hz to 1 GHz with 100 points per decade. It calculates the differential output voltage, plots gain in dB and phase, and measures the first 3 dB roll-off frequency as `f_p1`.

### Differential pair with NMOS tail load

The DC version reports the operating point of the circuit including `XNload`:

```bash
ngspice -b MosLoad/Mosload.spice -o MosLoad/Mosload.out
```

The AC version runs two sweeps:

- Differential mode: `Vin1 AC=+0.5`, `Vin2 AC=-0.5`
- Common mode: `Vin1 AC=+0.5`, `Vin2 AC=+0.5`

It writes the results to `MosLoad/data/`:

```bash
ngspice -b MosLoad/Mosload_ac.spice -o MosLoad/Mosload_ac.out
```

The `wrdata` commands create the data files. Existing files with the same names are replaced by ngspice.

## Plotting the AC results

After running `MosLoad/Mosload_ac.spice`, run:

```bash
python3 MosLoad/PythonPlot/plot.py
```

The script discovers every `.txt` file in `MosLoad/data/`, reads paired frequency/value columns, and creates one semilog-x plot per file. In a graphical environment it opens a Matplotlib window. With a non-interactive backend it saves the result as:

```text
MosLoad/PythonPlot/plots.png
```

The generated files contain:

- `diff.txt`: differential-mode gain and phase
- `cm.txt`: common-mode gain and phase
- `cmrr.txt`: CMRR in dB

## Notes

- The output node names differ between the ideal DC/AC netlists (`Vout+`, `Vout-`) and the AC netlist's internal aliases (`vout_p`, `vout_n`). Use the node names defined by the netlist when extending the simulations.
- The AC analyses use the magnitude of the differential output, expressed in dB with ngspice's `db()` function.
- The saved data files are generated artifacts. Re-run the AC simulation whenever the circuit or model parameters change.
