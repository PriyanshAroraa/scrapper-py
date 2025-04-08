from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from search import get_search_results
from scraper import scrape_all_urls
from summarizer import summarize_content
import markdown
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic')
        session['topic'] = topic
        return redirect(url_for('loading'))
    return render_template("index.html")

@app.route('/loading')
def loading():
    return render_template("loading.html")

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.json.get('topic')
    session['topic'] = topic

    # Step 1: Get search → scrape → summarize
    urls = get_search_results(topic, max_results=10)
    scraped_data = scrape_all_urls(urls)
    summary = summarize_content(scraped_data)

    # Step 2: Split into sections
    lines = summary.split('\n')
    summary_intro = []
    key_trends = []
    competitors = []
    insights = []

    current_section = "summary"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "Key Trends" in line:
            current_section = "trends"
            continue
        elif "Competitors" in line:
            current_section = "competitors"
            continue
        elif "Insights" in line:
            current_section = "insights"
            continue

        if current_section == "summary":
            summary_intro.append(line)
        elif current_section == "trends":
            key_trends.append(line.lstrip("1234.-• "))
        elif current_section == "competitors":
            competitors.append(line.lstrip("1234.-• "))
        elif current_section == "insights":
            insights.append(line.lstrip("1234.-• "))

    # Step 3: Convert each section to HTML using markdown
    session['summary_html'] = markdown.markdown(" ".join(summary_intro))
    session['trends_html'] = markdown.markdown("\n".join(f"- {t}" for t in key_trends))
    session['competitors_html'] = markdown.markdown("\n".join(f"- {c}" for c in competitors))
    session['insights_html'] = markdown.markdown("\n".join(f"- {i}" for i in insights))

    return jsonify({"status": "ok"})

@app.route('/results')
def results():
    summary_html = session.get('summary_html', '')
    trends_html = session.get('trends_html', '')
    competitors_html = session.get('competitors_html', '')
    insights_html = session.get('insights_html', '')

    if not summary_html:
        return redirect(url_for('index'))

    return render_template(
        "results.html",
        summary_html=summary_html,
        trends_html=trends_html,
        competitors_html=competitors_html,
        insights_html=insights_html
    )

if __name__ == '__main__':
    app.run(debug=True)
