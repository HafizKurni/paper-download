import streamlit as st
import re

# Set the page configuration
st.set_page_config(page_title="Scribd Link Generator", page_icon="🔗")

st.title("Scribd Download Link Generator")
st.info("This app replicates the logic from the 'Download(PDF)' function of the userscript. It generates a download link for a third-party service. (Khusus Untuk Ut Ut)")

# Get user input
scribd_url = st.text_input(
    "Paste your Scribd URL here:",
    placeholder="https://www.scribd.com/document/123456/example-doc-title"
)

# Create a button to generate the link
if st.button("Generate Download Link", type="primary"):
    if scribd_url:
        # This is the Python equivalent of the regex from the userscript:
        # /https:\/\/www\.scribd\.com\/(?:doc|document|presentation)\/(\d+)\/([^/?#]+)/
        regex_pattern = r"https:\/\/www\.scribd\.com\/(?:doc|document|presentation)\/(\d+)\/([^\/?#]+)"
        
        match = re.search(regex_pattern, scribd_url)
        
        if match:
            # Extract the two parts from the regex match
            doc_id = match.group(1)    # e.g., "505139221"
            doc_title = match.group(2) # e.g., "xtream-codes-4"
            
            st.success("Successfully parsed URL!")
            st.write(f"**Document ID:** `{doc_id}`")
            st.write(f"**Document Title:** `{doc_title}`")
            
            # Construct the final download service URL, just like the userscript
            final_url = f"https://compress-pdf.vietdreamhouse.com/?fileurl=https://scribd.downloader.tips/pdownload/{doc_id}/{doc_title}"
            
            st.subheader("Your Download Link:")
            # Use st.link_button to create a clickable button
            st.link_button("Go to Download Page", final_url)

            st.warning(
                """
                **Disclaimer:** This button sends you to two third-party websites 
                (`vietdreamhouse.com` and `downloader.tips`) that are not affiliated with Scribd.
                We cannot guarantee their safety, functionality, or privacy. Proceed with caution.
                """
            )
        
        else:
            # The regex did not match the input URL
            st.error("Invalid Scribd URL. Please make sure it looks like a standard document URL (e.g., .../document/12345/...).")
    else:
        # The user clicked the button without pasting a URL
        st.warning("Please paste a Scribd URL into the box above.")
