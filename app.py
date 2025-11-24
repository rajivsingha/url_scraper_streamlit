import streamlit as st
import asyncio
import os
import subprocess
import sys

# --- 1. SETUP: Install Browser (Hack for Streamlit Cloud) ---
def install_playwright_browser():
    """
    Checks if the browser is installed. If not, runs 'playwright install chromium'.
    This is necessary because Streamlit Cloud doesn't do this automatically.
    """
    if "browser_installed" not in st.session_state:
        with st.spinner("First run detected: Installing browser... (this takes 1 minute)"):
            try:
                # Install the browser binary
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
                # Install system deps (backup measure)
                subprocess.run([sys.executable, "-m", "playwright", "install-deps"], check=True)
                st.session_state.browser_installed = True
                st.success("Browser installed!")
            except Exception as e:
                st.error(f"Failed to install browser: {e}")

# Run setup
install_playwright_browser()

# --- 2. IMPORT CRAWL4AI ---
# We import inside a try-block or after setup to avoid import errors if setup fails
try:
    from crawl4ai import AsyncWebCrawler
except ImportError:
    # Fallback if pip install failed silently (rare but possible)
    subprocess.run([sys.executable, "-m", "pip", "install", "crawl4ai"], check=True)
    from crawl4ai import AsyncWebCrawler

# --- 3. CRAWLER LOGIC ---
async def run_crawler(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

# --- 4. APP UI ---
def main():
    st.title("🕷️ Crawl4AI Streamlit App")
    
    # API Mode Check
    query_params = st.query_params
    api_mode = query_params.get("api")
    url_param = query_params.get("url")

    if api_mode == "true" and url_param:
        # --- API MODE ---
        # Hide standard UI
        st.markdown("<style>header, footer, .stApp {visibility: hidden;}</style>", unsafe_allow_html=True)
        try:
            markdown_content = asyncio.run(run_crawler(url_param))
            st.text(markdown_content)
        except Exception as e:
            st.text(f"Error: {e}")
    else:
        # --- UI MODE ---
        url = st.text_input("Enter URL to Scrape:", "https://example.com")
        if st.button("Run Scraper"):
            if not url:
                st.warning("Please enter a URL.")
                return
            
            with st.spinner("Scraping..."):
                try:
                    result = asyncio.run(run_crawler(url))
                    st.subheader("Result (Markdown)")
                    st.text_area("Output", result, height=600)
                except Exception as e:
                    st.error(f"Error during scrape: {e}")

if __name__ == "__main__":
    main()
