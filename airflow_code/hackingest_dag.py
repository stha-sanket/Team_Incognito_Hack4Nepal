from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.context import Context
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to the Python path
dag_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dag_path)

# Import the ingestion function
from hackingest import ingest_documents

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

@dag(
    dag_id='document_ingestion_pipeline',
    default_args=default_args,
    description='Pipeline for ingesting documents and creating embeddings',
    start_date=datetime(2024, 1, 1),
    schedule='0 0 * * *',  # Run daily at midnight
    catchup=False,
    tags=['nlp', 'document_processing', 'embeddings'],
)
def create_document_ingestion_dag():
    
    @task
    def validate_input_data(**context) -> str:
        """Validate that input data exists and is accessible"""
        data_path = os.path.join(dag_path, "data")
        if not os.path.exists(data_path):
            raise ValueError(f"Data directory not found at {data_path}")
        
        txt_files = list(Path(data_path).glob("*.txt"))
        if not txt_files:
            raise ValueError(f"No .txt files found in {data_path}")
        
        print(f"Found {len(txt_files)} text files for processing")
        return data_path

    @task
    def cleanup_old_embeddings(**context) -> str:
        """Clean up old embedding database if it exists"""
        chroma_db_path = os.path.join(dag_path, "chroma_db")
        if os.path.exists(chroma_db_path):
            import shutil
            shutil.rmtree(chroma_db_path)
            print(f"Cleaned up old embedding database at {chroma_db_path}")
        return chroma_db_path

    @task
    def run_ingestion(data_path: str, chroma_db_path: str, **context) -> str:
        """Wrapper function to run the ingestion process"""
        try:
            # Pass the ChromaDB persistence directory
            persist_dir = ingest_documents(persist_dir=chroma_db_path)
            if not os.path.exists(persist_dir):
                raise ValueError(f"Ingestion failed: {persist_dir} not created")
            return persist_dir
        except Exception as e:
            print(f"Error during ingestion: {str(e)}")
            raise

    @task
    def verify_embeddings(persist_dir: str, **context) -> str:
        """Verify that embeddings were created successfully"""
        if not os.path.exists(persist_dir):
            raise ValueError(f"Embedding database not found at {persist_dir}")
        
        # Check for essential Chroma DB files
        required_files = ['chroma.sqlite3']  # Removed 'index' as it's not required in newer versions
        for file in required_files:
            file_path = os.path.join(persist_dir, file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(
                    f"Missing required file: {file} at {file_path}. Did ingestion run correctly?"
                )
        
        print(f"Successfully verified embeddings at {persist_dir}")
        return "Embedding verification successful"

    @task
    def log_completion(result: str, **context) -> str:
        """Log the completion of the pipeline"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Document ingestion completed successfully at {timestamp}"
        print(log_message)
        return log_message

    # Define the task dependencies with data flow
    data_path = validate_input_data()
    chroma_path = cleanup_old_embeddings()
    persist_dir = run_ingestion(data_path, chroma_path)
    verification = verify_embeddings(persist_dir)
    log_completion(verification)

# Create the DAG
document_ingestion_dag = create_document_ingestion_dag()
