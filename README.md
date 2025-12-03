# Sales Revenue Pipeline with Apache Airflow

An automated data pipeline that analyzes daily sales revenue from a PostgreSQL database using Apache Airflow.

## Project Overview

This project extracts sales data from a retail database, calculates total revenue per day, and visualizes the results as a time series plot. The entire workflow is automated using Apache Airflow.

## Answer to Assignment Question

**What is the total revenue on 1996-08-08?**
- **Answer: 525**

## Technologies Used

- **Python 3.10**
- **PostgreSQL** - Database
- **Apache Airflow** - Workflow orchestration
- **Pandas** - Data processing
- **Matplotlib** - Data visualization
- **psycopg2** - PostgreSQL adapter

## Project Structure
```
sales-pipeline-project/
├── dags/
│   └── sales_pipeline_dag.py       # Airflow DAG definition
├── scripts/
│   └── process_sales.py            # Data extraction and processing
├── output/
│   └── daily_revenue_*.png         # Generated visualizations
└── README.md
```

## Pipeline Workflow

1. **Extract**: Query PostgreSQL database for sales data (orders, order_details, products)
2. **Transform**: Calculate total revenue per day using SQL JOIN and aggregation
3. **Visualize**: Generate time series plot of daily revenue
4. **Automate**: Schedule daily execution via Airflow

## SQL Query

The pipeline uses this query to calculate daily revenue:
```sql
SELECT 
    o.orderdate,
    SUM(od.quantity * p.price) AS total_revenue
FROM orders o
JOIN order_details od ON o.orderid = od.orderid
JOIN products p ON od.productid = p.productid
GROUP BY o.orderdate
ORDER BY o.orderdate;
```

## Setup Instructions

### Prerequisites
- PostgreSQL with RetailDB database
- Python 3.x
- Apache Airflow

### Installation

1. Clone the repository
2. Install required Python packages:
```bash
pip install pandas matplotlib psycopg2-binary apache-airflow
```

3. Update database credentials in `scripts/process_sales.py` if needed

4. Copy the DAG to Airflow's dags folder:
```bash
cp dags/sales_pipeline_dag.py ~/airflow/dags/
```

5. Start Airflow:
```bash
# Terminal 1
airflow webserver --port 8080

# Terminal 2
airflow scheduler
```

6. Access Airflow UI at `http://localhost:8080`

## Running the Pipeline

### Manual Execution
```bash
python3 scripts/process_sales.py
```

### Airflow Execution
1. Navigate to `http://localhost:8080`
2. Enable the `sales_revenue_pipeline` DAG
3. Trigger the DAG manually or wait for scheduled run

## Results

The pipeline generates:
- Time series visualization of daily sales revenue
- PNG files saved in `output/` directory with timestamps
- Console output showing number of records processed

### Sample Output Files

Generated visualizations from pipeline runs:
- `daily_revenue_20251201_090240.png` - Initial test run
- `daily_revenue_20251201_094746.png` - Second test run
- `daily_revenue_20251201_094808.png` - Airflow automated run

### Sample Visualization

![Daily Revenue Chart](output/daily_revenue_20251201_094808.png)

The chart displays daily sales revenue trends over time, showing 160 days of transaction data from the RetailDB database.

## Database Schema

Key tables used:
- `orders` - Order information with dates
- `order_details` - Line items with quantities
- `products` - Product information with prices

## Author

Kiwilytics

## License

This project is for educational purposes.