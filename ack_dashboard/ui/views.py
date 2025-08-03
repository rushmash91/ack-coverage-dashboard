import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

from ..calculations.metrics import calculate_overall_metrics, create_service_dataframe
from .components import render_service_selector, render_selection_info, render_no_data_message


def show_overall_coverage(data: Dict[str, Any], metrics: Dict[str, Any], service_df: pd.DataFrame) -> None:
    st.header("📈 Overall API Coverage")
    
    with st.expander("🔧 Filter Services", expanded=False):
        all_services = list(data.keys())
        selected_services = render_service_selector(all_services, "overall")
    
    st.session_state.selected_services = selected_services
    metrics = calculate_overall_metrics(data, selected_services)
    service_df = create_service_dataframe(data, selected_services)
    
    render_selection_info(len(selected_services), len(all_services))
    if not selected_services:
        st.warning("Please select at least one service to display data.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Services",
            value=metrics['num_services']
        )
    
    with col2:
        st.metric(
            label="Total Operations",
            value=f"{metrics['total_operations']:,}"
        )
    
    with col3:
        st.metric(
            label="Supported Operations", 
            value=f"{metrics['total_supported']:,}"
        )
    
    with col4:
        st.metric(
            label="Mean Coverage",
            value=f"{metrics['overall_coverage']:.1f}% | CP: {metrics['control_plane_coverage']:.1f}%"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Supported', 'Not Supported'],
            values=[metrics['total_supported'], metrics['total_operations'] - metrics['total_supported']],
            hole=0.4,
            marker_colors=['#2ecc71', '#e74c3c']
        )])
        fig_pie.update_layout(
            title="Overall API Coverage",
            title_x=0.5,
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        if not service_df.empty:
            top_services = service_df.head(10)
            fig_bar = px.bar(
                top_services,
                x='Coverage %',
                y='Service',
                orientation='h',
                title="Top 10 Services by Coverage",
                color='Coverage %',
                color_continuous_scale='RdYlGn'
            )
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            render_no_data_message("No services selected for chart display.")
    
    st.subheader("📋 Services Overview")
    if not service_df.empty:
        st.dataframe(
            service_df[['Service', 'Total Operations', 'Supported Operations', 'Coverage %']],
            use_container_width=True,
            height=400
        )
    else:
        render_no_data_message("No services selected for table display.")


def show_control_plane_overview(data: Dict[str, Any], metrics: Dict[str, Any], service_df: pd.DataFrame) -> None:
    st.header("⚙️ Control Plane Overview")
    with st.expander("🔧 Filter Services", expanded=False):
        all_services = list(data.keys())
        selected_services = render_service_selector(all_services, "cp")
    
    st.session_state.selected_services = selected_services
    metrics = calculate_overall_metrics(data, selected_services)
    service_df = create_service_dataframe(data, selected_services)
    
    render_selection_info(len(selected_services), len(all_services))
    if not selected_services:
        st.warning("Please select at least one service to display data.")
        return
    
    if not service_df.empty and 'Control Plane Operations' in service_df.columns:
        cp_service_df = service_df[service_df['Control Plane Operations'] > 0].copy()
    else:
        cp_service_df = pd.DataFrame()
    
    if cp_service_df.empty:
        st.info("No services with control plane operations found in the selected services.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Services with Control Plane",
            value=len(cp_service_df)
        )
    
    with col2:
        st.metric(
            label="Total Control Plane Ops",
            value=f"{metrics['total_control_plane']:,}"
        )
    
    with col3:
        st.metric(
            label="Supported Control Plane", 
            value=f"{metrics['total_supported_control_plane']:,}",
            delta=f"{metrics['control_plane_coverage']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="Mean Coverage",
            value=f"{metrics['control_plane_coverage']:.1f}%"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Supported', 'Not Supported'],
            values=[metrics['total_supported_control_plane'], metrics['total_control_plane'] - metrics['total_supported_control_plane']],
            hole=0.4,
            marker_colors=['#2ecc71', '#e74c3c']
        )])
        fig_pie.update_layout(
            title="Control Plane Coverage",
            title_x=0.5,
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        if not cp_service_df.empty:
            top_cp_services = cp_service_df.head(10)
            fig_bar = px.bar(
                top_cp_services,
                x='Control Plane Coverage %',
                y='Service',
                orientation='h',
                title="Top 10 Services by Control Plane Coverage",
                color='Control Plane Coverage %',
                color_continuous_scale='RdYlGn'
            )
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            render_no_data_message("No services with control plane operations selected.")
    
    st.subheader("📋 Control Plane Services Overview")
    if not cp_service_df.empty:
        st.dataframe(
            cp_service_df[['Service', 'Control Plane Operations', 'Supported Control Plane', 'Control Plane Coverage %']],
            use_container_width=True,
            height=400
        )
    else:
        render_no_data_message("No services with control plane operations found in selection.")


def show_service_analysis(data: Dict[str, Any], service_df: pd.DataFrame) -> None:
    """Display per-service analysis."""
    st.header("🔍 Per-Service Analysis")
    
    selected_service = st.selectbox(
        "Select a service for detailed analysis:",
        options=list(data.keys()),
        format_func=lambda x: x.upper()
    )
    
    if selected_service:
        service_data = data[selected_service]
        col1, col2, col3, col4 = st.columns(4)
        
        coverage = (service_data['supported_operations'] / service_data['total_operations'] * 100) if service_data['total_operations'] > 0 else 0
        
        with col1:
            st.metric("Service", selected_service.upper())
        with col2:
            st.metric("Total Operations", service_data['total_operations'])
        with col3:
            st.metric("Supported", service_data['supported_operations'])
        with col4:
            st.metric("Coverage", f"{coverage:.1f}%")
        
        col1, col2 = st.columns(2)    
        with col1:
            control_plane_ops = service_data['control_plane_operations']
            data_plane_ops = service_data['total_operations'] - control_plane_ops
            
            fig_ops = go.Figure(data=[go.Pie(
                labels=['Control Plane', 'Data Plane'],
                values=[control_plane_ops, data_plane_ops],
                marker_colors=['#3498db', '#9b59b6']
            )])
            fig_ops.update_layout(title=f"{selected_service.upper()} - Operation Types")
            st.plotly_chart(fig_ops, use_container_width=True)
        
        with col2:
            supported = service_data['supported_operations']
            unsupported = service_data['total_operations'] - supported
            
            fig_support = go.Figure(data=[go.Pie(
                labels=['Supported', 'Not Supported'],
                values=[supported, unsupported],
                marker_colors=['#2ecc71', '#e74c3c']
            )])
            fig_support.update_layout(title=f"{selected_service.upper()} - Support Status")
            st.plotly_chart(fig_support, use_container_width=True)
        
        st.subheader("📝 Operations Details")   
        operations_data = []
        for op in service_data['operations']:
            operations_data.append({
                'Operation': op['name'],
                'Type': op['type'].replace('_', ' ').title(),
                'Supported': 'Yes' if op['file'] and op['line'] > 0 else 'No',
                'File': op['file'] if op['file'] else 'N/A',
                'Line': str(op['line']) if op['line'] > 0 else 'N/A'
            })
        
        operations_df = pd.DataFrame(operations_data)
        
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.multiselect(
                "Filter by Type:",
                options=operations_df['Type'].unique(),
                default=operations_df['Type'].unique()
            )
        with col2:
            support_filter = st.multiselect(
                "Filter by Support Status:",
                options=['Yes', 'No'],
                default=['Yes', 'No']
            )
        
        filtered_df = operations_df[
            (operations_df['Type'].isin(type_filter)) &
            (operations_df['Supported'].isin(support_filter))
        ]
        
        st.dataframe(filtered_df, use_container_width=True, height=400)


def show_per_service_control_plane(data: Dict[str, Any], service_df: pd.DataFrame) -> None:
    st.header("🔧 Per-Service Control Plane Analysis")
    
    cp_services = [service for service, service_data in data.items() if service_data['control_plane_operations'] > 0]
    
    if not cp_services:
        st.warning("No services found with control plane operations.")
        return
    
    selected_service = st.selectbox(
        "Select a service for control plane analysis:",
        options=cp_services,
        format_func=lambda x: x.upper()
    )
    
    if selected_service:
        service_data = data[selected_service]
        col1, col2, col3, col4 = st.columns(4)
        
        cp_coverage = (service_data['supported_control_plane_operations'] / service_data['control_plane_operations'] * 100) if service_data['control_plane_operations'] > 0 else 0
        
        with col1:
            st.metric("Service", selected_service.upper())
        with col2:
            st.metric("Control Plane Ops", service_data['control_plane_operations'])
        with col3:
            st.metric("Supported CP Ops", service_data['supported_control_plane_operations'])
        with col4:
            st.metric("CP Coverage", f"{cp_coverage:.1f}%")
        
        col1, col2 = st.columns(2)
        with col1:
            supported_cp = service_data['supported_control_plane_operations']
            unsupported_cp = service_data['control_plane_operations'] - supported_cp
            
            fig_cp_support = go.Figure(data=[go.Pie(
                labels=['Supported', 'Not Supported'],
                values=[supported_cp, unsupported_cp],
                marker_colors=['#2ecc71', '#e74c3c']
            )])
            fig_cp_support.update_layout(title=f"{selected_service.upper()} - Control Plane Support")
            st.plotly_chart(fig_cp_support, use_container_width=True)
        
        with col2:
            control_plane_ops = service_data['control_plane_operations']
            data_plane_ops = service_data['total_operations'] - control_plane_ops
            
            fig_ops = go.Figure(data=[go.Pie(
                labels=['Control Plane', 'Data Plane'],
                values=[control_plane_ops, data_plane_ops],
                marker_colors=['#3498db', '#9b59b6']
            )])
            fig_ops.update_layout(title=f"{selected_service.upper()} - Operation Types")
            st.plotly_chart(fig_ops, use_container_width=True)
        
        st.subheader("📝 Control Plane Operations Details")
        cp_operations_data = []
        for op in service_data['operations']:
            if op['type'] == 'control_plane':
                cp_operations_data.append({
                    'Operation': op['name'],
                    'Supported': 'Yes' if op['file'] and op['line'] > 0 else 'No',
                    'File': op['file'] if op['file'] else 'N/A',
                    'Line': str(op['line']) if op['line'] > 0 else 'N/A'
                })
        
        if cp_operations_data:
            cp_operations_df = pd.DataFrame(cp_operations_data)
            col1, col2 = st.columns([1, 1])
            with col1:
                support_filter = st.multiselect(
                    "Filter by Support Status:",
                    options=['Yes', 'No'],
                    default=['Yes', 'No']
                )
            with col2:
                st.write("")  # Spacer
            
            filtered_cp_df = cp_operations_df[
                cp_operations_df['Supported'].isin(support_filter)
            ]
            
            st.dataframe(filtered_cp_df, use_container_width=True, height=400)
        else:
            st.info("No control plane operations found for this service.")