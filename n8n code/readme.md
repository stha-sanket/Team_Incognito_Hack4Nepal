# n8n WhatsApp Document Extraction & Chatbot Workflow

This workflow automates WhatsApp message handling, document extraction, and chatbot responses using n8n, Google Gemini, and email notifications. It is designed for Nepali government document support (e.g., citizenship, PAN) and general chatbot queries.

## 🚀 Features

- **WhatsApp Integration:** Receives and processes both text and image messages from WhatsApp users
- **Document Extraction:** Extracts and analyzes data from images of Nepali government documents (e.g., citizenship, PAN cards)
- **Chatbot (RAG):** Answers user questions about Nepali citizenship and taxation using a Retrieval-Augmented Generation (RAG) approach, powered by Google Gemini
- **Contextual Memory:** Maintains conversation context for personalized responses
- **Automated Email Notification:** Sends extracted data and user details to an admin email for review
- **Smart Routing:** Distinguishes between text and image messages and processes them accordingly

## 🏗️ Workflow Overview

```
graph TD
    A[WhatsApp Trigger] --> B{Switch: Text or Image?}
    B -- Text --> C[Edit Fields]
    C --> D[AI Agent (Chatbot)]
    D --> E[Google Gemini Chat Model]
    D --> F[Simple Memory]
    D --> G[WhatsApp Business Cloud (Reply)]
    B -- Image --> H[WhatsApp Business Cloud (Get Media URL)]
    H --> I[HTTP Request (Download Image)]
    I --> J[Google Gemini Chat Model (Vision)]
    J --> K[Simple Memory (Image)]
    J --> L[Image Agent (Extract Data)]
    L --> M[WhatsApp Business Cloud (Reply)]
    L --> N[AI Agent1 (Email Compose)]
    N --> O[Google Gemini Chat Model (Email)]
    N --> P[Simple Memory (Email)]
    N --> Q[Gmail (Send Email)]
```

## 🧩 Node Breakdown

- **WhatsApp Trigger:** Listens for new WhatsApp messages (text or image)
- **Switch:** Determines if the incoming message is text or image
- **Edit Fields:** Prepares text for the chatbot
- **AI Agent:** Handles text queries using a RAG-based prompt and Google Gemini
- **Google Gemini Chat Model:** Processes both text and image queries
- **Simple Memory:** Maintains conversation context for each user
- **WhatsApp Business Cloud:** Sends replies back to the user
- **HTTP Request:** Downloads images sent by users
- **Image Agent:** Extracts data from government document images using Gemini Vision
- **AI Agent1:** Composes an email with extracted data for admin review
- **Gmail:** Sends the email to the admin

## 📝 How It Works

1. **User sends a message (text or image) to WhatsApp**
2. **Switch node** checks if the message is text or image
3. **Text Message:**
   - Routed to the chatbot (AI Agent) with a RAG prompt about Nepali citizenship/taxation
   - Gemini LLM generates a response
   - Context is maintained for follow-up questions
   - Reply is sent back to the user on WhatsApp
4. **Image Message:**
   - Image is downloaded and processed
   - Gemini Vision extracts and analyzes document data
   - If the image is a valid government document, extracted data is sent to the user and also emailed to the admin for review
   - If not, the user is informed that only government documents are supported
5. **Admin Notification:**
   - An email is sent to the admin (`sanketshrestha09@gmail.com`) with the user's details and extracted data for verification

## ⚙️ Setup Instructions

1. **n8n Instance:**  
   Install and run n8n (see [n8n docs](https://docs.n8n.io/))

2. **Credentials:**  
   - WhatsApp Business Cloud API
   - Google Gemini (PaLM) API
   - Gmail OAuth2
   - HTTP Header Auth (for image download)

3. **Import Workflow:**  
   - Copy the provided JSON and import it into n8n

4. **Configure Webhooks:**  
   - Set up WhatsApp webhook URLs in your WhatsApp Business settings to point to your n8n instance

5. **Set Environment Variables:**  
   - Configure any required API keys and secrets in n8n credentials

## 🛡️ Security & Privacy

- Only government document images are processed
- User data is sent to admin email for manual review
- No sensitive data is stored in the workflow code

## 📚 Example Use Cases

- **Citizenship/PAN Help:**  
  Users can ask questions about Nepali citizenship or PAN, and get accurate, document-based answers
- **Document Submission:**  
  Users can send images of their documents for automated extraction and admin review
- **Automated Admin Alerts:**  
  Admin receives an email whenever a user submits a document

## 👤 Contributors

- Sanket Shrestha (D-ASK Ai)
- Team Incognito

## 📞 Support

For issues or questions, please contact the admin at `sanketshrestha09@gmail.com` or open an issue in the project repository.
