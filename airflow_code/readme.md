# Airflow Data Pipeline
> olease insure that you have already cloned the parent repo and are setting up this repo
This directory contains Apache Airflow DAGs and scripts for automated data ingestion and processing for our chatbot system.

## 🚀 Features

- Daily data ingestion for chatbot training
- Automated document processing
- ChromaDB vector database updates
- Scheduled workflow management

## 📁 Directory Structure

```
airflow_code/
├── dags/                  # Airflow DAG definitions
│   └── hackingest_dag.py  # Main ingestion DAG
├── scripts/               # Processing scripts
│   └── hackingest.py      # Data ingestion script
├── data/                  # Data storage
│   └── text.txt          # Processed text data
└── chroma_db/            # Vector database storage
```

## 🔧 Setup

1. Install dependencies:
```bash
pip install apache-airflow
pip install chromadb
pip install pandas
pip install langchain
```

2. Configure Airflow:
```bash
# Set Airflow home
export AIRFLOW_HOME=~/airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

3. Start Airflow services:
```bash
# Start webserver
airflow webserver -p 8080

# Start scheduler
airflow scheduler
```

## 📊 DAG Details

### hackingest_dag.py
- Schedule: Daily at midnight
- Tasks:
  1. Data Collection
  2. Text Processing
  3. Vector Database Update
  4. Chatbot Model Update

## 💾 Data Processing

The pipeline handles:
- Document text extraction
- Data cleaning and formatting
- Vector embeddings generation
- ChromaDB database updates

## 🔍 Monitoring

- Access Airflow UI: http://localhost:8080
- Monitor task status and logs
- View success/failure metrics
- Track data processing statistics

## ⚙️ Configuration

Key configurations in `hackingest_dag.py`:
```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
```

## 📝 Logging

Logs are stored in:
- Task logs: `~/airflow/logs/[dag_id]/[task_id]/[execution_date]`
- Scheduler logs: `~/airflow/logs/scheduler`
- Webserver logs: `~/airflow/logs/webserver`
