# Eleana

**Eleana** is a free software application for analyzing and modifying spectra from electron paramagnetic resonance (EPR) spectrometers. Originally developed in **LabVIEW**, it is now being completely rewritten in **Python** for better flexibility and broader accessibility. 

Eleana supports direct data import from **Bruker** spectrometers (ESP300E, EMX, ElexSys) and is available for any system running **Python**

The software is freely available for scientific and educational use, while commercial use requires authorization.

### Requirements

- **Python** 3.12 or higher
- **pip** or **pipenv**

### Setup
1. Clone the **Eleana** repository:
    ```bash
    clone https://github.com/KarritPrimorph/Eleana
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

If you prefer using `pip` directly clone the repo, enter **Eleana**, then:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```