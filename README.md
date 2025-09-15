# 🔗 Scribd Download Link Generator (Streamlit App)

This is a simple Streamlit web application that replicates the PDF download logic from the "Scribd Content Viewer/Downloader" JavaScript userscript.

It provides a simple UI to paste any Scribd document URL. The app then parses this URL to extract the document's ID and title, and uses them to construct a download URL that points to a third-party downloader service.

This app **does not** scrape or download any content itself; it only generates a link based on the logic found in the original userscript.

## 🚀 How to Run the App

You can run this application locally on your machine.

**Requirements:**

  * Python 3.7+
  * Streamlit

<!-- end list -->

1.  **Install the required library:**
    Open your terminal and install Streamlit using pip:

    ```bash
    pip install streamlit
    ```

2.  **Save the Code:**
    Save the application code as a Python file (e.g., `app.py`).

3.  **Run the App:**
    In your terminal, navigate to the directory where you saved the file and run:

    ```bash
    streamlit run app.py
    ```

Your default web browser will automatically open a new tab with the running application (usually at `http://localhost:8501`).

## ⚙️ How to Use

1.  Navigate to Scribd.com and find a document you want to access.
2.  Copy the full URL from your browser's address bar (e.g., `https://www.scribd.com/document/123456/example-doc-title`).
3.  Paste this URL into the text input box in the Streamlit app.
4.  Click the **"Generate Download Link"** button.
5.  If the URL is valid, the app will display the parsed Document ID and Title, along with a new button: **"Go to Download Page"**.
6.  Click this new button to be taken to the external download service.

## ⚠️ Disclaimer

This tool is provided for educational and convenience purposes only.

  * This app relies entirely on **two external, third-party services** (`compress-pdf.vietdreamhouse.com` and `scribd.downloader.tips`) that are not affiliated with this project or Scribd.
  * These services may become unavailable, change their functionality, or be discontinued at any time without notice, which would cause this tool to stop working.
  * We cannot guarantee the safety, security, or privacy practices of these external services. **Proceed with caution.**
  * Bypassing paywalls may violate the terms of service of Scribd. Please support content creators by using official channels where possible.
