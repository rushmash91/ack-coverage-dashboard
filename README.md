# ACK Coverage Dashboard

A Streamlit dashboard for visualizing AWS ACK API coverage metrics across AWS services.

## Features

- **Overall Coverage**: Aggregated metrics with service filtering via checkboxes
- **Per-Service Analysis**: Detailed view of individual AWS services
- **Control Plane Overview**: Focus on control plane operation coverage
- **Interactive Filtering**: Select/unselect services to customize dashboard views


## Requirements

- Python 3.13+
- uv package manager

## Usage

```bash
uv sync
uv run python -m streamlit run main.py
```

Access the dashboard at http://localhost:8501
