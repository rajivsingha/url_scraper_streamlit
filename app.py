import streamlit as st
import asyncio
import os
import sys

# --- Install Browsers (Hack for Streamlit Cloud) ---
# Streamlit Cloud doesn't install Playwright browsers by default.
# We run this command once on the first load.
def install_playwright():
    if "playwright_installed" not in st.session_state:
        os.system("playwright install chromium")
        st.session_state.playwright_installed = True

try:
    from crawl4ai import AsyncWebCrawler
except ImportError:
    # If import fails, install dependencies (fallback)
    os.system("pip install crawl4ai playwright")
    os.system("playwright install chromium")
    from crawl4ai import AsyncWebCrawler

# Run the installation check
install_playwright()

# --- Async Crawler Function ---
async def run_crawler(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

# --- Main Logic ---
def main():
    # Check Query Params for API usage
    query_params = st.query_params
    api_mode = query_params.get("api")
    target_url = query_params.get("url")

    # --- API MODE ---
    if api_mode == "true" and target_url:
        # Hide UI
        st.markdown("""
            <style>
                #MainMenu, header, footer, .stApp {visibility: hidden;}
                div.block-container {padding-top: 0rem;}
            </style>
        """, unsafe_allow_html=True)
        
        # Run Async Crawler
        try:
            markdown_content = asyncio.run(run_crawler(target_url))
            st.text(markdown_content)
        except Exception as e:
            st.text(f"Error: {str(e)}")

    # --- GUI MODE ---
    else:
        st.title("🤖 JS-Enabled Scraper (Crawl4AI)")
        st.warning("Note: First run may be slow (installing browser).")

        url_input = st.text_input("Enter URL (JS/SPA supported):", "https://js.stripe.com/v3/")
        
        if st.button("Scrape"):
            with st.spinner("Starting browser & scraping..."):
                try:
                    # Run the async function
                    result = asyncio.run(run_crawler(url_input))
                    st.subheader("Markdown Output")
                    st.text_area("Result", result, height=500)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
