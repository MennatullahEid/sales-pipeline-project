import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def extract_sales_data():
    """Extract sales data from PostgreSQL database"""
    
    # Database connection parameters
    conn = psycopg2.connect(
        host="localhost",
        database="retaildb",
        user="kiwilytics",
        password="kiwilytics"
    )
    
    # SQL query to calculate daily revenue
    query = """
    SELECT 
        o.orderdate,
        SUM(od.quantity * p.price) AS total_revenue
    FROM orders o
    JOIN order_details od ON o.orderid = od.orderid
    JOIN products p ON od.productid = p.productid
    GROUP BY o.orderdate
    ORDER BY o.orderdate;
    """
    
    # Execute query and load into pandas DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"Extracted {len(df)} rows of sales data")
    return df

def visualize_revenue(df, output_path):
    """Create time series plot of daily revenue"""
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['orderdate'], df['total_revenue'], marker='o', linestyle='-', linewidth=2)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    plt.title('Daily Sales Revenue', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    plt.close()

def main():
    """Main execution function"""
    
    print("Starting sales data pipeline...")
    
    # Extract data
    df = extract_sales_data()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'daily_revenue_{timestamp}.png')
    visualize_revenue(df, output_path)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()