import streamlit as st
from typing import List


def render_service_selector(all_services: List[str], key_prefix: str) -> List[str]:
    for service in all_services:
        checkbox_key = f"service_checkbox_{service}"
        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = service in st.session_state.selected_services
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Select All", key=f"select_all_{key_prefix}"):
            for service in all_services:
                st.session_state[f"service_checkbox_{service}"] = True
            st.rerun()
    with col2:
        if st.button("Clear All", key=f"clear_all_{key_prefix}"):
            for service in all_services:
                st.session_state[f"service_checkbox_{service}"] = False
            st.rerun()
    
    # Services checkboxes in grid layout
    cols = st.columns(4)
    selected_services = []
    
    for i, service in enumerate(all_services):
        col_idx = i % 4
        with cols[col_idx]:
            checkbox_key = f"service_checkbox_{service}"
            if st.checkbox(service.upper(), key=checkbox_key):
                selected_services.append(service)
    
    return selected_services


def render_selection_info(selected_count: int, total_count: int) -> None:
    if selected_count < total_count:
        st.info(f"📊 Showing data for **{selected_count}** of **{total_count}** services")


def render_no_data_message(message: str = "No data available") -> None:
    st.info(message)