# gmxQTools
This repository provides tools and scripts for working with molecular dynamics (MD) simulations using GROMACS (e.g., PyMemDyn), as well as for performing simulations with Q (e.g., QligFEP) on the same molecular system. It includes tools for system preparation, simulation execution, results analysis, and more.

All the scripts and the pipeline are optimized for batch processing of MD simulations, handling numerous ligands, folders, and proteins.

## Directory Structure

### 1.setup
The `setup` directory contains essential files and scripts to initialize and configure systems for molecular dynamics (MD) and free energy perturbation (FEP) simulations using the `pymemdyn` package. This includes:

- Configuration files for MD and FEP simulations.
- Initialization scripts to set up the simulation environment.
- Parameter and topology files needed for the simulations.

### 2.analysis
The `analysis` directory is dedicated to tools and scripts for analyzing the results of MD and FEP simulations. This includes:

- Python scripts for processing and visualizing simulation data.
- Tools to calculate various properties from the simulation outputs.
- Templates and other files.

### 3.developer
The `developer` directory contains unstable versions and experimental features. This area is for development purposes and may include:

- Beta versions of scripts and tools.
- Experimental features under development.
- Testing scripts and temporary files.

Use these files with caution, as they may not be fully tested or stable.

## :construction: Disclaimer
This repository, gmxQTools, is currently under construction and is continuously evolving. We are dedicated to improving and expanding the functionalities of our tools and scripts regularly. Please be aware that some features may be incomplete or may change in future updates.

## Bug Reporting and Contributions
If you encounter any issues or bugs while using these tools, please report them to ruben.prieto@usc.es. We welcome contributions and suggestions that can help improve this project.

# Setup Instructions

## Necessary dependencies

### Python Packages (requirements.txt)
- Numpy: `pip install numpy`
- Biopython: `pip install biopython`

### Necessary Software
- **GROMACS** (tested on gmx 2020 MPI and 2021): Install from [GROMACS official site](http://www.gromacs.org/)
- **PyModSim**: Clone and install from [PyModSim GitHub](https://github.com/GPCR-ModSim/pymodsim)
- **PyMemDyn**: Clone and install from [PyMemDyn GitHub](https://github.com/GPCR-ModSim/pymemdyn)
  - **Ligpargen**: Clone and install from [Ligpargen GitHub](https://github.com/Isra3l/ligpargen)
- **Q6**: Clone and install from [Q6 GitHub](https://github.com/esguerra/Q6)