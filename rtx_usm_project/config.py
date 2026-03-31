RSS_DATABASE = {
    "antaranews": "https://www.antaranews.com/rss/top-news.xml",
    "tribun jateng": "https://jateng.tribunnews.com/rss",
    "republika": "https://www.republika.co.id/rss"
}

CUSTOM_CSS = """
<style>
.stApp { background-color: #F8F9FA; }
.main-header {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.time-display {
    text-align: center;
    font-size: 16px;
    color: #555;
    margin-bottom: 20px;
    font-weight: bold;
}
.news-card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #1e3c72;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
.news-meta {
    font-size: 13px; 
    color: gray; 
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.news-meta a {
    color: #2a5298;
    text-decoration: none;
    font-weight: bold;
}
.news-meta a:hover {
    text-decoration: underline;
}
</style>
"""