# Oratis : AI guide to ace interview

![Oratis Demo Animation](https://raw.githubusercontent.com/Ronin-117/Mock_Online_InterviewAi/master/assets/oratis_short.gif)


Project Repository: https://github.com/Ronin-117/Mock_Online_InterviewAi

# Overview

Oratis is an AI-powered mock interview platform designed to help users improve their soft skills, particularly communication, confidence, and interview performance.
Recognizing that over 90% of firms value soft skills, yet many technically skilled individuals lack them, Oratis aims to provide an engaging, interactive, and effective training solution beyond traditional methods.
It simulates realistic interview scenarios using an animated 3D interviewer, offers real-time feedback on verbal and non-verbal communication, and adapts to the user's pace, ultimately boosting user confidence and readiness for real-world interviews.

# Key Features

*   **Interactive 3D Interviewer:** A realistic, animated interviewer built with Three.js provides a more immersive experience than static chatbots or pre-recorded videos. Features lip-synced animations and dynamic gestures.
*   **Feedback-Driven Speech Recognition:** Utilizes Faster-Whisper for real-time transcription. A fine-tuned BERT model checks for sentence completeness before triggering the AI interviewer's response, preventing awkward interruptions and promoting a natural conversational flow.
*   **Multiple Interviewer Personas:** Simulates various interview dynamics (e.g., empathetic, challenging) by adjusting response tone and difficulty, preparing users for diverse real-life scenarios.
*   **Non-Verbal Communication Analysis:** Leverages computer vision libraries (OpenCV, MediaPipe) to analyze eye contact, posture, and facial expressions, providing crucial feedback on body language and professional presence.
*   **Real-time Feedback:** Offers immediate insights into both verbal delivery (fluency, filler words) and non-verbal cues.

# Technology Stack

*   **Frontend:** React.js, Three.js (for 3D rendering and animation)
*   **Backend:** Django (Python web framework)
*   **AI & Machine Learning:**
    *   **Core AI/LLM:** Google Gemini (specifically `gemini-2.0-flash-exp`)
    *   **Speech-to-Text (STT):** Faster-Whisper (OpenAI)
    *   **Text-to-Speech (TTS):** GTTS
    *   **Sentence Completeness:** Fine-tuned BERT model (custom dataset)
    *   **Non-Verbal Analysis:** OpenCV, MediaPipe
*   **Configuration Management:** Python (`config.py` for API keys)

# Project Structure Analysis

*   The project uses a standard Django backend structure, likely located within a subdirectory like `app2/backend/`.
*   `manage.py` is the entry point for Django administrative tasks.
*   A separate `frontend` directory contains the React application code.
*   Configuration, particularly sensitive API keys like `GEMINI_API_KEY`, is managed via `config.py` `. 

# Setup and Installation

1.  **Clone the repository:**
    ```bash
     git clone https://github.com/Ronin-117/Mock_Online_InterviewAi.git
     cd Mock_Online_InterviewAi
    ```
2.  **Set up Backend (Django):**
    *   Navigate to the backend directory (likely `app2/backend/` or where `manage.py` resides).
        ```bash
         cd app2/backend
        ```
    *   Install Python dependencies (ensure `requirements.txt` is present in the root or backend folder):
        ```bash
         pip install -r requirements.txt
        ```
    *   **Configure API Keys:** See the Configuration section below.
    *   Apply database migrations (if any):
        ```bash
         python manage.py migrate
        ```
3.  **Set up Frontend (React):**
    *   Navigate to the frontend directory .
        ```bash
         cd app2/frontend
        ```
    *   Install Node.js dependencies:
        ```bash
         npm install
        ```
    *   Ensure the frontend is configured to communicate with the Django backend API (likely running on `http://localhost:8000`). This might involve setting proxy settings in `package.json` or using environment variables.

# Configuration

*   **Google Gemini API Key:** This project requires a Google Gemini API Key.
    *   Add your API key to `config.py` like this:
        ```python
        # config.py
         GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
        ```
    *   **CRITICAL:** Add `config.py` to your `.gitignore` file immediately to prevent accidentally committing your secret API key.
        ```
        # .gitignore
        config.py
        venv/
        __pycache__/
        *.pyc
        # Add other necessary ignores (e.g., node_modules, .env files)
        ```

# Running the Application

You need to run the backend and frontend servers concurrently in separate terminals.

1.  **Start the Backend Server:**
    *   Navigate to the directory containing `manage.py`.
        ```bash
         cd app2/backend
        ```
    *   Run the Django development server:
        ```bash
         python manage.py runserver
        ```
    *   By default, this usually runs on `http://localhost:8000`.

2.  **Start the Frontend Development Server:**
    *   Open a **new terminal**.
    *   Navigate to the frontend directory.
        ```bash
         cd app2/frontend
        ```
    *   Run the React development server:
        ```bash
         npm run dev
        ```
    *   This usually runs on `http://localhost:3000` and should open automatically in your browser.

3.  **Access the Application:**
    *   Open your web browser and navigate to the address provided by the React development server (typically `http://localhost:3000`). The React app will interact with the Django backend API running on port 8000.

# Future Work

*   Expanding the platform to include AI-driven group discussion simulations.
*   Further optimization of real-time latency for TTS and AI responses.
*   Conducting formal user evaluations to quantitatively measure the platform's effectiveness.
*   Refining non-verbal cue analysis and feedback mechanisms.

# Acknowledgements

*   Inspired by the need for better soft skills training tools.
*   Leverages open-source technologies like Django, React, Three.js, Faster-Whisper, Tortoise TTS, OpenCV, MediaPipe, and models from the Hugging Face ecosystem (BERT).
*   Utilizes the Google Gemini API for advanced AI capabilities.
