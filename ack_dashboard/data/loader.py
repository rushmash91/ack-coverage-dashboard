import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional


def load_data() -> Optional[Dict[str, Any]]:
    results_dir = Path("results")
    data = {}
    
    if not results_dir.exists():
        st.error("Results directory not found!")
        return None
    
    for json_file in results_dir.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                service_data = json.load(f)
                service_name = service_data.get('service_name', json_file.stem.replace('-operations', ''))
                data[service_name] = service_data
        except Exception as e:
            st.error(f"Error loading {json_file}: {e}")
    
    return data