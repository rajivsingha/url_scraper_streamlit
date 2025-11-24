import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- Scrape Logic ---
def get_page_content(url):
    try:
        # Fake a user agent to avoid 403 errors
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Get text and strip whitespace
        text = soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

# --- Handle Query Parameters ---
query_params = st.query_params
api_mode = query_params.get("api")
target_url = query_params.get("url")

# --- API / CLEAN MODE ---
if api_mode == "true" and target_url:
    # 1. Hide standard Streamlit UI elements via CSS
    hide_ui = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {margin-top: -80px;}
        div.block-container {padding-top: 0rem;}
        </style>
    """
    st.markdown(hide_ui, unsafe_allow_html=True)
    
    # 2. Get Content
    content = get_page_content(target_url)
    
    # 3. Output ONLY the content
    # st.text preserves newlines and doesn't interpret Markdown
    st.text(content)

# --- GUI MODE (Interactive) ---
else:
    st.title("📄 content-only Scraper")
    st.write("This tool extracts raw text from a webpage.")

    url_input = st.text_input("Enter URL:", "https://www.example.com")

    if st.button("Get Content"):
        if url_input:
            with st.spinner("Fetching..."):
                result = get_page_content(url_input)
                st.text_area("Raw Content:", result, height=400)
    
    st.markdown("---")
    st.info("To use the 'Clean View' via URL, use the format below:")
    
    base_url = "https://YOUR-APP.streamlit.app"
    example = f"{base_url}/?api=true&url={url_input}"
    st.code(example, language="text")