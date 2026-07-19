"""
Charting and visualization functions for SocksQuads CRM.
Uses Plotly for interactive, modern charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional


def create_metric_card(value, label, change_percent=None, color="primary"):
    """Create a styled metric card display."""
    html = f"""
    <div style="background: white; padding: 20px; border-radius: 8px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0;">
        <p style="font-size: 14px; color: #666; margin: 0;">{label}</p>
        <h3 style="font-size: 28px; color: #0066cc; margin: 10px 0;">{value}</h3>
        {f'<p style="font-size: 12px; color: green; margin: 0;">↑ {change_percent}%</p>' if change_percent else ''}
    </div>
    """
    return html


def sales_by_day_chart(df: pd.DataFrame):
    """Create a line chart for sales by day."""
    if df.empty:
        return None
    
    try:
        df_plot = df.copy()
        df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
        daily = df_plot.groupby(df_plot['Date'].dt.date)['Order Value'].sum().reset_index()
        daily.columns = ['Date', 'Sales']
        daily['Sales'] = daily['Sales'].astype(float)
        
        fig = px.line(daily, x='Date', y='Sales', 
                     title='Daily Sales Trend',
                     markers=True,
                     color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            yaxis_title='Sales (₹)',
            xaxis_title='Date',
            height=400
        )
        return fig
    except:
        return None


def sales_by_month_chart(df: pd.DataFrame):
    """Create a bar/line chart for sales by month."""
    if df.empty:
        return None
    
    try:
        df_plot = df.copy()
        df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
        monthly = df_plot.groupby(df_plot['Date'].dt.to_period('M')).agg({
            'Order Value': 'sum',
            'Collection': 'sum'
        }).reset_index()
        monthly['Date'] = monthly['Date'].astype(str)
        monthly.columns = ['Month', 'Sales', 'Collection']
        
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        fig.add_trace(
            go.Bar(x=monthly['Month'], y=monthly['Sales'], name='Sales', 
                   marker_color='#0066cc', showlegend=True),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=monthly['Month'], y=monthly['Collection'], name='Collection',
                      mode='lines+markers', line=dict(color='#00cc66', width=3),
                      showlegend=True),
            secondary_y=False
        )
        
        fig.update_layout(
            title_text='Monthly Sales & Collection',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        fig.update_xaxes(title_text='Month')
        fig.update_yaxes(title_text='Amount (₹)')
        
        return fig
    except:
        return None


def top_salesman_chart(df: pd.DataFrame, top_n=5):
    """Create a bar chart for top salesmen."""
    if df.empty:
        return None
    
    try:
        top = df.groupby('Salesman')['Order Value'].sum().nlargest(top_n).reset_index()
        top.columns = ['Salesman', 'Sales']
        top['Sales'] = top['Sales'].astype(float)
        
        fig = px.bar(top, x='Salesman', y='Sales',
                    title=f'Top {top_n} Salesmen',
                    color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            hovermode='x',
            template='plotly_white',
            yaxis_title='Sales (₹)',
            xaxis_title='Salesman',
            height=400,
            showlegend=False
        )
        return fig
    except:
        return None


def top_retailer_chart(df: pd.DataFrame, top_n=5):
    """Create a bar chart for top retailers."""
    if df.empty:
        return None
    
    try:
        top = df.groupby('Retailer')['Order Value'].sum().nlargest(top_n).reset_index()
        top.columns = ['Retailer', 'Sales']
        top['Sales'] = top['Sales'].astype(float)
        
        fig = px.bar(top, x='Retailer', y='Sales',
                    title=f'Top {top_n} Retailers',
                    color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            hovermode='x',
            template='plotly_white',
            yaxis_title='Sales (₹)',
            xaxis_title='Retailer',
            height=400,
            showlegend=False
        )
        return fig
    except:
        return None


def sales_by_area_chart(df: pd.DataFrame):
    """Create a pie chart for sales distribution by area."""
    if df.empty:
        return None
    
    try:
        area_sales = df.groupby('Area')['Order Value'].sum().reset_index()
        area_sales.columns = ['Area', 'Sales']
        area_sales['Sales'] = area_sales['Sales'].astype(float)
        
        fig = px.pie(area_sales, names='Area', values='Sales',
                    title='Sales Distribution by Area',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400)
        return fig
    except:
        return None


def collection_vs_outstanding_chart(df: pd.DataFrame):
    """Create a chart comparing collection vs outstanding."""
    if df.empty:
        return None
    
    try:
        df_plot = df.copy()
        df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
        
        daily = df_plot.groupby(df_plot['Date'].dt.date).agg({
            'Collection': 'sum',
            'Outstanding': 'sum'
        }).reset_index()
        daily.columns = ['Date', 'Collection', 'Outstanding']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily['Date'],
            y=daily['Collection'],
            name='Collection',
            marker_color='#00cc66'
        ))
        
        fig.add_trace(go.Bar(
            x=daily['Date'],
            y=daily['Outstanding'],
            name='Outstanding',
            marker_color='#ff6600'
        ))
        
        fig.update_layout(
            title='Collection vs Outstanding',
            barmode='stack',
            hovermode='x unified',
            template='plotly_white',
            height=400,
            yaxis_title='Amount (₹)',
            xaxis_title='Date'
        )
        
        return fig
    except:
        return None


def retailer_growth_chart(df: pd.DataFrame):
    """Create a chart showing retailer growth over time."""
    if df.empty:
        return None
    
    try:
        df_plot = df.copy()
        df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
        
        retailer_count = df_plot.groupby(df_plot['Date'].dt.date)['Retailer'].nunique().reset_index()
        retailer_count.columns = ['Date', 'Unique Retailers']
        retailer_count['Cumulative'] = retailer_count['Unique Retailers'].cumsum()
        
        fig = px.line(retailer_count, x='Date', y='Cumulative',
                     title='Unique Retailers Visited (Cumulative)',
                     markers=True,
                     color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            yaxis_title='Unique Retailers',
            xaxis_title='Date',
            height=400
        )
        return fig
    except:
        return None


def order_distribution_chart(df: pd.DataFrame):
    """Create a histogram of order values."""
    if df.empty:
        return None
    
    try:
        df_plot = df.copy()
        df_plot['Order Value'] = df_plot['Order Value'].astype(float)
        
        fig = px.histogram(df_plot, x='Order Value', nbins=20,
                          title='Order Value Distribution',
                          color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            template='plotly_white',
            yaxis_title='Number of Orders',
            xaxis_title='Order Value (₹)',
            height=400,
            showlegend=False
        )
        return fig
    except:
        return None


def salesman_performance_table(df: pd.DataFrame):
    """Create a performance table for salesmen."""
    if df.empty:
        return None
    
    try:
        stats = df.groupby('Salesman').agg({
            'Order Value': ['sum', 'count', 'mean'],
            'Collection': 'sum',
            'Outstanding': 'sum'
        }).round(2)
        
        stats.columns = ['Total Sales', 'Orders', 'Avg Order', 'Collection', 'Outstanding']
        stats = stats.reset_index()
        stats = stats.sort_values('Total Sales', ascending=False)
        
        return stats
    except:
        return None


def area_performance_table(df: pd.DataFrame):
    """Create a performance table for areas."""
    if df.empty:
        return None
    
    try:
        stats = df.groupby('Area').agg({
            'Order Value': ['sum', 'count'],
            'Collection': 'sum',
            'Outstanding': 'sum',
            'Retailer': 'nunique'
        }).round(2)
        
        stats.columns = ['Total Sales', 'Orders', 'Collection', 'Outstanding', 'Retailers']
        stats = stats.reset_index()
        stats = stats.sort_values('Total Sales', ascending=False)
        
        return stats
    except:
        return None


def top_products_chart(df: pd.DataFrame, top_n=5):
    """Create a chart for top products by quantity."""
    if df.empty:
        return None
    
    try:
        # Assuming products are mentioned in Remarks field
        top = df.groupby('Remarks')['Order Qty'].sum().nlargest(top_n).reset_index()
        top.columns = ['Product', 'Quantity']
        top['Quantity'] = top['Quantity'].astype(float)
        
        fig = px.bar(top, x='Product', y='Quantity',
                    title=f'Top {top_n} Products by Quantity',
                    color_discrete_sequence=['#0066cc'])
        fig.update_layout(
            hovermode='x',
            template='plotly_white',
            yaxis_title='Quantity',
            xaxis_title='Product',
            height=400,
            showlegend=False
        )
        return fig
    except:
        return None


def collection_rate_chart(df: pd.DataFrame):
    """Create a gauge chart for collection rate."""
    if df.empty:
        return None
    
    try:
        total_sales = df['Order Value'].astype(float).sum()
        total_collection = df['Collection'].astype(float).sum()
        
        if total_sales == 0:
            rate = 0
        else:
            rate = (total_collection / total_sales) * 100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Collection Rate (%)"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0066cc"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcccc"},
                    {'range': [50, 80], 'color': "#ffffcc"},
                    {'range': [80, 100], 'color': "#ccffcc"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=400)
        return fig
    except:
        return None


def create_multiline_chart(df: pd.DataFrame, x_col: str, y_cols: list, title: str):
    """Create a multi-line chart."""
    if df.empty:
        return None
    
    try:
        fig = go.Figure()
        
        colors = ['#0066cc', '#00cc66', '#ff6600', '#ff0066']
        for i, col in enumerate(y_cols):
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[col],
                mode='lines+markers',
                name=col,
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        fig.update_layout(
            title=title,
            hovermode='x unified',
            template='plotly_white',
            height=400,
            yaxis_title='Amount (₹)'
        )
        
        return fig
    except:
        return None
