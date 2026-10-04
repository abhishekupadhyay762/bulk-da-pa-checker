import streamlit as st
import requests
import uuid
import pandas as pd

# Set up the page
st.set_page_config(page_title="Bulk DA/PA Checker", page_icon="📈", layout="centered")
st.title("📈 Bulk DA/PA Checker")
st.markdown("Powered by the [Moz API](https://moz.com/products/api)")

MOZ_API_URL = "https://api.moz.com/jsonrpc"

# Input Fields
api_token = st.text_input("Moz API Token", type="password", help="Get your free token from moz.com/products/api")
urls_input = st.text_area("URLs to Analyze (One per line)", height=150, help="Max 50 URLs per month on the Moz Free Tier")

if st.button("Fetch Metrics", type="primary"):
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    if not api_token:
        st.error("Please provide your Moz API Token.")
    elif not urls:
        st.error("Please enter at least one URL.")
    elif len(urls) > 50:
        st.error("You can only check up to 50 URLs at a time (Moz Free Tier monthly limit).")
    else:
        with st.spinner(f"Analyzing {len(urls)} URLs... Please wait."):
            headers = {
                "x-moz-token": api_token,
                "Content-Type": "application/json"
            }

            payload = []
            for url in urls:
                payload.append({
                    "id": str(uuid.uuid4()),
                    "jsonrpc": "2.0",
                    "method": "data.site.metrics.fetch",
                    "params": {
                        "data": {
                            "site_query": {
                                "query": url,
                                "scope": "domain"
                            }
                        }
                    }
                })

            try:
                response = requests.post(MOZ_API_URL, headers=headers, json=payload)
                
                if response.status_code in [401, 403]:
                    st.error("Authentication failed. Please check your Moz API Token.")
                else:
                    api_data = response.json()
                    
                    if isinstance(api_data, dict) and "error" in api_data:
                        st.error(f"Moz API Error: {api_data['error'].get('message', 'Unknown Error')}")
                    else:
                        if not isinstance(api_data, list):
                            api_data = [api_data]

                        results = []
                        for item in api_data:
                            if "error" in item:
                                results.append({
                                    "URL": "Error",
                                    "Domain Authority (DA)": "Error",
                                    "Page Authority (PA)": item['error'].get('message', 'Unknown Error')
                                })
                                continue

                            result_data = item.get("result", {})
                            site_query = result_data.get("site_query", {})
                            target_url = site_query.get("query", "Unknown URL")
                            
                            metrics = result_data.get("site_metrics", {})
                            da_val = metrics.get("domain_authority")
                            pa_val = metrics.get("page_authority")
                            
                            results.append({
                                "URL": target_url,
                                "Domain Authority (DA)": round(da_val, 2) if da_val is not None else "N/A",
                                "Page Authority (PA)": round(pa_val, 2) if pa_val is not None else "N/A"
                            })

                        # Display Results
                        df = pd.DataFrame(results)
                        st.success("Analysis Complete!")
                        st.dataframe(df, use_container_width=True)
                        
                        # Export to CSV feature built into Streamlit
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download data as CSV",
                            data=csv,
                            file_name='da_pa_results.csv',
                            mime='text/csv',
                        )

            except requests.exceptions.RequestException as e:
                st.error(f"Network error connecting to Moz: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
