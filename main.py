import streamlit as st
from ack_dashboard.data.loader import load_data
from ack_dashboard.calculations.metrics import calculate_overall_metrics, create_service_dataframe
from ack_dashboard.ui.views import (
    show_overall_coverage,
    show_service_analysis,
    show_control_plane_overview,
    show_per_service_control_plane
)


st.set_page_config(
    page_title="AWS ACK API Coverage Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff6b35;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">🚀 AWS ACK API Coverage Dashboard</h1>', unsafe_allow_html=True)
    
    data = load_data()
    if not data:
        st.stop()
    
    # Initialize session state for service selection
    if 'selected_services' not in st.session_state:
        st.session_state.selected_services = list(data.keys())
    
    overall_metrics = calculate_overall_metrics(data, st.session_state.selected_services)
    service_df = create_service_dataframe(data, st.session_state.selected_services)
    
    st.sidebar.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
    view = st.sidebar.selectbox(
        "Select View",
        ["Overall Coverage", "Per-Service Analysis", "Control Plane Overview", "Per-Service Control Plane"]
    )
    
    if view == "Overall Coverage":
        show_overall_coverage(data, overall_metrics, service_df)
    elif view == "Per-Service Analysis":
        show_service_analysis(data, service_df)
    elif view == "Control Plane Overview":
        show_control_plane_overview(data, overall_metrics, service_df)
    else:
        show_per_service_control_plane(data, service_df)


if __name__ == "__main__":
    main()
