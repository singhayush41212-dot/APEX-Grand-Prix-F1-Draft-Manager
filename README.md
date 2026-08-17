# F1 Draft & Season Simulator 🏎️

An interactive Formula 1 management game built with Python and Streamlit. Draft your driver lineup, choose your chassis and team principal, customize your team branding, and simulate a 20-race World Championship season.

## Features

- **Custom Roster Draft:** Pick two drivers, an official constructor chassis, and a team principal.
- **Dynamic 20-Race Engine:** Tracks feature varying layouts (street, speed, balanced) that interact with driver stats, car performance, and principal special abilities.
- **Championship Tables:** Complete Drivers' and Constructors' Standings generated with round-by-round point breakdowns.
- **2026 Grid Integration:** Includes active constructors and teams like Cadillac F1.

## Project Structure

```text
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── drivers.json
├── requirements.txt
└── src/
    ├── data_loader.py
    ├── database.py
    ├── draft.py
    ├── models.py
    └── simulation.py
