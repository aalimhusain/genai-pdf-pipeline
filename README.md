# 📄 AI PDF Summarizer + Entity Extractor

## 🚀 Overview
This project lets you **upload any PDF document** and automatically:
- Generate a **summary**
- Extract **People, Organizations, Locations, Dates**
- Save results into **Google Sheets** (via n8n workflow)

It is built for the **GenAI Automation Assignment**.

---

## 🖥️ How to Run (Step by Step)

### 1️⃣ Install Requirements (only once)
1. Install [Python 3.10+](https://www.python.org/downloads/)  
2. Install dependencies:
   - Open a terminal/command prompt in this folder
   - Run:
     ```bash
     pip install -r requirements.txt
     ```

*(Don’t worry — all libraries are automatically installed with this one command.)*

---

### 2️⃣ Start the Application
Run this command in the project folder:

```bash
uvicorn api:app --reload

Keep this window open
If successful, you will see something like:
Uvicorn running on http://127.0.0.1:8000

3️⃣ Open the Browser 

Go to: http://127.0.0.1:8000/docs
(This is a ready-made testing page provided by FastAPI.)

Scroll down to POST /process → Click it.

Click Try it out.

Under file, click Choose File → select any PDF (an example test_document.pdf is included).

{"Example test PDFs is included: "test_document.pdf" and "test_doc.pdf"
Contains a person, an organization, a location, and a date so you can see all fields extracted."}

Click Execute.

You will instantly see a JSON response as output.

✅ Deliverables

Code (FastAPI app)
Example PDF for testing
n8n Workflow Export (workflow_without_creds.json) for Google Sheets integration
Instructions (this readme file)
A csv template to store output in google sheets before running app.

Notes:
No high technical background needed: just run the app, open the browser, click upload, and see results.
If you face any issue, check that Python is installed and internet is available for model download. I used facebook's 'bart-large-cnn' its small,fast and reliable.
You must connect your own Google Sheets account in n8n after importing the workflow, since credentials are not included.

After importing workflow_without_creds.json into n8n:
- Open the Google Sheets node
- Replace <<<YOUR_GOOGLE_SHEET_ID>>> with your own Sheet ID
- Add your own Google credentials
- Replace <<<ADD_YOUR_OWN_CREDENTIALS_IN_N8N>>> with your OAuth2 credential ID
