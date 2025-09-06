import requests
import xml.etree.ElementTree as ET
from rag_service import generate_summary  # Use relative import for script testing

def get_medlineplus_topic(query):
    """
    Query MedlinePlus Connect API for health topics.
    Returns the first matching topic summary.
    """
    # MedlinePlus Connect API endpoint for search
    endpoint = "https://wsearch.nlm.nih.gov/ws/query"
    params = {
        "db": "healthTopics",
        "term": query,
        "rettype": "brief",
        "retmax": 1
    }
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        # Parse XML response
        root = ET.fromstring(response.content)
        document = root.find(".//document")
        if document is not None:
            # Try both child elements and attributes, fallback to url if only url is present
            title = document.findtext("title")
            summary = document.findtext("summary")
            url = document.findtext("url")
            # Fallback to attributes if elements are empty
            if not title:
                title = document.attrib.get("title", "")
            if not summary:
                summary = document.attrib.get("summary", "")
            if not url:
                url = document.attrib.get("url", "")
            # If still empty, try to extract text from the document itself
            if not title and document.text:
                title = document.text.strip()
            # If only url is present, set a default title
            result = {
                "title": title,
                "summary": summary,
                "url": url
            }
            # Only fetch GPT summary if ONLY the URL was returned (title and summary are both empty)
            if url and not title and not summary:
                print(f"Only URL found. Gathering info from: {url}")
                gpt_summary = None
                try:
                    page_response = requests.get(url, timeout=10)
                    page_response.raise_for_status()
                    page_text = page_response.text
                    gpt_summary = generate_summary(page_text)
                except Exception as e:
                    print(f"Error fetching or summarizing URL: {str(e)}")
                if gpt_summary:
                    print("GPT summary from URL:", gpt_summary)
            return result
        else:
            print("Debug: No document found. Raw XML:", response.text)
            return None
    except Exception as e:
        print(f"MedlinePlus API error: {str(e)}")
        return None

