import pandas as pd
from typing import Dict, Any, List, Optional


def calculate_overall_metrics(data: Dict[str, Any], selected_services: Optional[List[str]] = None) -> Dict[str, Any]:
    if not data:
        return {}
    
    if selected_services is not None:
        filtered_data = {k: v for k, v in data.items() if k in selected_services}
    else:
        filtered_data = data
    
    if not filtered_data:
        return {
            'total_operations': 0,
            'total_supported': 0,
            'total_control_plane': 0,
            'total_supported_control_plane': 0,
            'overall_coverage': 0,
            'control_plane_coverage': 0,
            'num_services': 0
        }
    
    total_operations = sum(service['total_operations'] for service in filtered_data.values())
    total_supported = sum(service['supported_operations'] for service in filtered_data.values())
    total_control_plane = sum(service['control_plane_operations'] for service in filtered_data.values())
    total_supported_control_plane = sum(service['supported_control_plane_operations'] for service in filtered_data.values())
    
    # Calculate average overall coverage (arithmetic mean of individual service coverage)
    overall_coverages = []
    cp_coverages = []
    for service_data in filtered_data.values():
        if service_data['total_operations'] > 0:
            overall_cov = (service_data['supported_operations'] / service_data['total_operations'] * 100)
            overall_coverages.append(overall_cov)
        
        if service_data['control_plane_operations'] > 0:
            cp_cov = (service_data['supported_control_plane_operations'] / service_data['control_plane_operations'] * 100)
            cp_coverages.append(cp_cov)
    
    overall_coverage = sum(overall_coverages) / len(overall_coverages) if overall_coverages else 0
    control_plane_coverage = sum(cp_coverages) / len(cp_coverages) if cp_coverages else 0
    
    return {
        'total_operations': total_operations,
        'total_supported': total_supported,
        'total_control_plane': total_control_plane,
        'total_supported_control_plane': total_supported_control_plane,
        'overall_coverage': overall_coverage,
        'control_plane_coverage': control_plane_coverage,
        'num_services': len(filtered_data)
    }


def create_service_dataframe(data: Dict[str, Any], selected_services: Optional[List[str]] = None) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    
    # Filter data based on selected services
    if selected_services is not None:
        filtered_data = {k: v for k, v in data.items() if k in selected_services}
    else:
        filtered_data = data
    
    if not filtered_data:
        return pd.DataFrame()
    
    services = []
    for service_name, service_data in filtered_data.items():
        coverage = (service_data['supported_operations'] / service_data['total_operations'] * 100) if service_data['total_operations'] > 0 else 0
        control_plane_coverage = (service_data['supported_control_plane_operations'] / service_data['control_plane_operations'] * 100) if service_data['control_plane_operations'] > 0 else 0
        
        services.append({
            'Service': service_name.upper(),
            'Total Operations': service_data['total_operations'],
            'Supported Operations': service_data['supported_operations'],
            'Coverage %': round(coverage, 1),
            'Control Plane Operations': service_data['control_plane_operations'],
            'Supported Control Plane': service_data['supported_control_plane_operations'],
            'Control Plane Coverage %': round(control_plane_coverage, 1)
        })
    
    return pd.DataFrame(services).sort_values('Coverage %', ascending=False)