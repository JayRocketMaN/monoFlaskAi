# 🤖 MonoFlask AI Chat Application (Flask)

A modern, responsive web-based chat application built with Python Flask and Google's latest **GenAI SDK**. This project features a clean, ChatGPT-style user interface, user session management (Login/Logout/Forgot Password), and seamless integration with Google's Gemini AI models (like `gemini-3.1-pro-preview` and `gemini-2.0-flash`).

## ✨ Features

- **Modern Chat UI:** Responsive chat interface with user/AI message bubbles, auto-scrolling, and a typing status indicator.
- **Google GenAI Integration:** Uses the official `google-genai` Python SDK for robust text generation and conversational memory.
- **Asynchronous Chat:** Uses JavaScript `fetch()` API to send and receive messages without reloading the page.
- **Authentication Pages:** Includes a beautiful Login and "Forgot Password" page with Flask flash messages for user feedback.
- **Session Management:** Secure Logout functionality that clears user sessions and redirects to the login screen.
- **Environment Security:** Uses `python-dotenv` to securely manage the Gemini API key.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## 🚀 Installation & Setup

**1. Clone the repository (or create your project folder)**
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

##  Requirements
This already exists in the requirements.txt file. This was used to save the package requirement into the file "pip freeze > requirements.txt"

After downloading project to your PC, use this command below to setup the project.

python -m venv venv
Venv\Scripts\Activate (on windows only)
source venv/bin/activate (on mac only)
pip install -r requirements.txt
External API calls Blueprint Caching email service database background queues