# Automation Platform - Team Incognito

An all-in-one automation platform that combines document extraction, RPA (Robotic Process Automation), chatbots, and workflow automation. This project was developed for Hack4Nepal hackathon.

## 🚀 Features

### 1. Document Extraction & Chatbot Platform
- Intelligent document parsing and data extraction
- RAG (Retrieval-Augmented Generation) based chatbot for document interactions
- User-friendly interface for document uploads and queries

### 2. Automated Data Pipeline
- Apache Airflow integration for daily data updates
- Automated ingestion of chatbot training data
- Scheduled workflow management
- ChromaDB integration for vector storage

### 3. RPA Automation Suite
#### Website Data Entry Automation
- Custom RPA solution for automated form filling
- Simulated website environment for testing
- Efficient data entry workflow

#### Google Forms Automation
- Automated form submission
- Data extraction and processing
- Streamlined data collection

### 4. WhatsApp Integration
- N8N powered WhatsApp bot
- Image data extraction capabilities
- RAG-based chatbot functionality
- Real-time response system

## 🛠️ Technology Stack

- **Backend Framework**: Django
- **Workflow Automation**: Apache Airflow
- **RPA Tools**: Custom RPA solutions
- **Database**: ChromaDB (Vector Database)
- **Integration Platform**: N8N
- **Messaging Platform**: WhatsApp Business API
- **AI/ML**: RAG (Retrieval-Augmented Generation)

## 📋 Prerequisites

- Python 3.8+
- Django
- Apache Airflow
- ChromaDB
- N8N
- WhatsApp Business API access
- Required Python packages (see requirements.txt)

## 🔧 Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/stha-sanket/Team_Incognito_Hack4Nepal.git
cd Team_Incognito_Hack4Nepal
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Airflow:
```bash
# Initialize the database
airflow db init

# Start the web server
airflow webserver -p 8080

# Start the scheduler
airflow scheduler
```

5. Set up N8N:
```bash
# Install n8n
npm install n8n -g

# Start n8n
n8n start
```

## 🏗️ Project Structure

```
Team_Incognito_Hack4Nepal/
├── django_hackathon/        # Main Django project
│   ├── chatbot/            # Document extraction & chatbot
│   ├── rpa_launcher/       # RPA control interface
│   └── api/                # REST API endpoints
├── airflow_code/           # Airflow DAGs and tasks
│   ├── dags/              # Airflow workflow definitions
│   └── scripts/           # Data ingestion scripts
├── RPA_HACKATHON/         # RPA automation projects
│   ├── website_automation/ # Website data entry RPA
│   └── google_forms/      # Google Forms automation
└── n8n_code/              # N8N workflows for WhatsApp bot
```

## 🚀 Usage

1. **Document Extraction & Chatbot**:
   - Upload documents through the web interface
   - Interact with the chatbot to query document content
   - View extracted information in structured format

2. **RPA Automation**:
   - Access the RPA launcher through the web interface
   - Select automation type (Website/Google Forms)
   - Monitor automation progress

3. **WhatsApp Bot**:
   - Send images or queries to the WhatsApp number
   - Receive extracted data or chatbot responses
   - Use natural language for interactions

## 👥 Contributors

- Team Incognito Members

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

We thank the following individuals for their valuable contributions to this project:

- [**Sanket Shrestha**](https://github.com/stha-sanket)
- [**Dip Darpan Kandel**](https://github.com/dip051030)
- [**Krrishpana Karmacharya**](https://github.com/krrishpana)
- [**Aarif Shrestha**](https://github.com/Aarif-Shrestha)

Your efforts are deeply appreciated! ❤️

## 📞 Support

For issues or questions, please contact the admin at `sanketshrestha09@gmail.com` or open an issue in the project repository.
