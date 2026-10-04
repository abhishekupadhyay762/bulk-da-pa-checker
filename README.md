# Bulk DA/PA Checker Pro 🚀

A clean, modern, and open-source web application to bulk check Domain Authority (DA) and Page Authority (PA) using the official Moz API. Built with Python (Flask) and Bootstrap 5.

## ✨ Features

- **Bulk URL Checking**: Check multiple URLs at once (up to 50 per month on the Moz free tier).
- **Beautiful UI/UX**: Designed with Bootstrap 5, FontAwesome icons, and custom CSS for a modern SaaS look.
- **Color-Coded Metrics**: Instantly identify high, medium, and low authority scores via color-coded badges.
- **Export & Copy**: Easily export your results to a CSV file or copy them directly to your clipboard for use in Excel/Google Sheets.
- **Error Handling**: Graceful error handling for API limits, authentication failures, and network issues.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Requests
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, FontAwesome

## 🚀 Getting Started

### Prerequisites
1. You must have [Python 3](https://www.python.org/downloads/) installed.
2. You need a free Moz API key. Sign up at [moz.com/products/api](https://moz.com/products/api) to get your **Access ID** and **Secret Key**.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bulk-da-pa-checker.git
   cd bulk-da-pa-checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Or simply run `pip install flask requests`)*

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   Navigate to [http://localhost:5000](http://localhost:5000)

## ⚠️ Important Note on Moz API Free Tier

The Moz API "Free Tier" is strictly limited:
- You are allowed **50 rows (URLs) per month**.
- You are limited to **1 request every 10 seconds**.
If you exceed these limits, the application will display an error from Moz. If you need to check thousands of URLs, you will need a paid Moz API subscription or switch to an alternative API like Open PageRank.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/yourusername/bulk-da-pa-checker/issues).

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
