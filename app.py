from flask import Flask, render_template, request, jsonify
import requests
import time
import uuid

app = Flask(__name__)

MOZ_API_URL = "https://api.moz.com/jsonrpc"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    urls = data.get('urls', [])
    api_token = data.get('api_token', '').strip()

    if not urls or not api_token:
        return jsonify({"error": "Please provide your Moz API Token and at least one URL."}), 400

    # Ensure URLs list is clean
    urls = [url.strip() for url in urls if url.strip()]
    if len(urls) > 50:
        return jsonify({"error": "You can only check up to 50 URLs at a time (Moz Free Tier monthly limit)."}), 400

    # Moz API V2 uses x-moz-token header (NOT Basic Auth)
    headers = {
        "x-moz-token": api_token,
        "Content-Type": "application/json"
    }

    # Prepare a batch of JSON-RPC requests (one per URL)
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
        
        if response.status_code == 401 or response.status_code == 403:
            return jsonify({"error": "Authentication failed. Please check your Moz API Token."}), 401
            
        api_data = response.json()
        
        # If the API returned a top-level error dictionary instead of a list
        if isinstance(api_data, dict) and "error" in api_data:
            return jsonify({"error": f"Moz API Error: {api_data['error'].get('message', 'Unknown Error')}"}), 400

        results = []
        # api_data should be a list of responses (batch response)
        if not isinstance(api_data, list):
            api_data = [api_data]

        for item in api_data:
            if "error" in item:
                results.append({
                    "url": "Error",
                    "da": "Error",
                    "pa": item['error'].get('message', 'Unknown Error')
                })
                continue

            result_data = item.get("result", {})
            site_query = result_data.get("site_query", {})
            target_url = site_query.get("query", "Unknown URL")
            
            metrics = result_data.get("site_metrics", {})
            da_val = metrics.get("domain_authority")
            pa_val = metrics.get("page_authority")
            
            results.append({
                "url": target_url,
                "da": round(da_val, 2) if da_val is not None else "N/A",
                "pa": round(pa_val, 2) if pa_val is not None else "N/A"
            })
        
        return jsonify({"results": results})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error connecting to Moz: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
