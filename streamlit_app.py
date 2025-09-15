import streamlit as st
import re
import requests
from urllib.parse import urlparse
import os

# --- Helper Functions from your Scripts ---

def get_filename_from_url(url):
    """Parses a URL to get the final filename."""
    try:
        parsed_url = urlparse(url)
        return os.path.basename(parsed_url.path)
    except Exception:
        return "download.pdf" # Fallback filename

def get_scribd_link(scribd_url):
    """Parses a Scribd URL and returns a third-party download service link."""
    regex_pattern = r"https:\/\/www\.scribd\.com\/(?:doc|document|presentation)\/(\d+)\/([^\/?#]+)"
    match = re.search(regex_pattern, scribd_url)
    
    if match:
        doc_id = match.group(1)
        doc_title = match.group(2)
        # Construct the final URL based on the userscript's logic
        final_url = f"https://compress-pdf.vietdreamhouse.com/?fileurl=https://scribd.downloader.tips/pdownload/{doc_id}/{doc_title}"
        return final_url, doc_id, doc_title
    return None, None, None

def get_academia_download_url(url, cookie_string):
    """
    Uses the provided cookie to find the direct download URL from Academia.edu.
    This is Part 1 of the Academia download process.
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie_string,  # Use the cookie provided by the user
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an error for bad responses (4xx, 5xx)

        # Pattern from your script: 'bulkDownloadUrl&quot;:&quot;(.*?)&quot;'
        pattern = r'bulkDownloadUrl&quot;:&quot;(.*?)&quot;'
        matches = re.findall(pattern, response.text)
        
        if matches:
            download_link = matches[0]
            # Replace escaped characters
            download_link = download_link.replace('\\u0026', '&')
            return download_link
    except Exception as e:
        st.error(f"Error finding download link: {e}")
        return None
    
    return None

def fetch_file_content(download_url):
    """
    Fetches the raw bytes of the file from the generated download URL.
    This is Part 2 of the Academia download process.
    """
    try:
        # Academia download links often don't require the full header/cookie set,
        # but we pass the user-agent just in case.
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        return response.content  # Return the raw file bytes
    except Exception as e:
        st.error(f"Error downloading file content: {e}")
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="Doc Link Generator", page_icon="🔗")
st.title("Scribd & Academia.edu Link Generator 🔗")

main_url = st.text_input(
    "Paste your Scribd or Academia.edu URL here:",
    placeholder="https://www.scribd.com/document/..."
)

st.divider()

# --- Academia.edu Specific Inputs ---
st.subheader("Academia.edu Requirements")
st.warning("Downloads from Academia.edu require your browser's login cookie.")

cookie_string = st.text_area(
    "Paste your Academia.edu cookie string here:",
    height=150,
    placeholder="auvid=MT...; _ga=GA1.2...; login_token=..."
)

with st.expander("How to get your cookie string"):
    st.markdown("""
        1.  Open `academia.edu` in your browser (Chrome/Firefox) and log in.
        2.  Open **Developer Tools** (Press `F12` or `Ctrl+Shift+I`).
        3.  Go to the **Network** tab.
        4.  Refresh the Academia page (or click any link on the site).
        5.  Find and click on any request in the list (e.g., the document name).
        6.  In the panel that appears, find the **Request Headers** section.
        7.  Scroll down until you find the `cookie:` field.
        8.  Copy the **ENTIRE** long value of that field and paste it above.
    """)

st.divider()

# --- Main Logic Button ---
if st.button("Generate Link / Download File", type="primary"):
    if "scribd.com" in main_url:
        st.info("Processing Scribd link...")
        final_url, doc_id, doc_title = get_scribd_link(main_url)
        
        if final_url:
            st.success(f"Generated link for: {doc_title} ({doc_id})")
            st.link_button("Go to Download Page (External Service)", final_url)
            st.warning(
                "This sends you to a third-party service. We do not control its safety or privacy."
            )
        else:
            st.error("Invalid Scribd URL. Could not parse.")

    elif "academia.edu" in main_url:
        st.info("Processing Academia.edu link...")
        if not cookie_string:
            st.error("Cookie string is required for Academia.edu links. Please paste it above.")
        else:
            # Step 1: Get the download URL
            download_link = get_academia_download_url(main_url, cookie_string)
            
            if download_link:
                st.success("Successfully found download link. Now fetching file...")
                # Step 2: Download the file content using the URL
                file_data = fetch_file_content(download_link)
                
                if file_data:
                    # Step 3: Provide the download button
                    filename = get_filename_from_url(download_link)
                    st.download_button(
                        label=f"Click to Download '{filename}'",
                        data=file_data,
                        file_name=filename,
                        mime="application/pdf" # Assuming it's a PDF
                    )
                else:
                    st.error("Failed to fetch the file content. Your cookie may be expired or the link is bad.")
            else:
                st.error("Could not find a download link. Your cookie is likely invalid or expired.")
    
    elif not main_url:
        st.warning("Please paste a URL in the box above.")
    
    else:
        st.error("URL not recognized. Please use a valid Scribd or Academia.edu link.")
