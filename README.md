# Eleana

**Eleana** is a free software application for analyzing and modifying spectra from electron paramagnetic resonance (EPR) spectrometers. Originally developed in **LabVIEW**, it is now being completely rewritten in **Python** for better flexibility and broader accessibility. 

Eleana supports direct data import from **Bruker** spectrometers (ESP300E, EMX, ElexSys) and is available for any system running **Python**

The software is freely available for scientific and educational use, while commercial use requires authorization.

### Requirements

- [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3123/)
- **pip** or **pipenv**

### Setup
1. Clone the **Eleana** repository:
    ```bash
    git clone https://github.com/KarritPrimorph/Eleana
    ```
2. Navigate into **Eleana** directory:

    ```bash
    cd Eleana
    ```

3. Install project dependencies using `pipenv`:

    ```bash
    pipenv install
    ```

4. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

5. Start the **Eleana** by running the main script:

    ```bash
    python main.py
    ```

### Without pipenv

If you prefer using `pip` directly clone the repo, enter **Eleana** directory, then:

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```