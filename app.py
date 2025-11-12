import json
import io
import requests
from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import LoginManager, current_user, login_required
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Local imports
from models import db, User, Case, Review, Leaderboard
from auth import auth_bp
from data import LEADERBOARD   # optional fallback data


app = Flask(__name__)
app.secret_key = "change-this-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clue_trail.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and login
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# Register auth blueprint
app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@app.context_processor
def inject_globals():
    return {"current_user": current_user, "is_authenticated": current_user.is_authenticated}



UNSPLASH_ACCESS_KEY = "StBNPVGnC8bjRhm_9xpNFfookHgalZqolhgMuYYkqBQ"  

def fetch_case_image(case_name):
    url = "https://api.unsplash.com/search/photos"
    params = {"query": case_name, "client_id": UNSPLASH_ACCESS_KEY, "per_page": 1}
    try:
        r = requests.get(url, params=params, timeout=5)
        print("Unsplash status:", r.status_code)
        data = r.json()
        if data.get("results"):
            image_url = data["results"][0]["urls"]["regular"]
            print("Fetched image:", image_url)
            return image_url
    except Exception as e:
        print("Image fetch error:", e)
    return "/static/images/404.jpg"



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    recent = Case.query.order_by(Case.year.desc()).limit(3).all()
    top = Case.query.first()
    return render_template("home.html", cases=Case.query.all(), recent=recent, top=top)


@app.route("/cases")
def case_list():
    status = request.args.get("status")
    year = request.args.get("year", type=int)
    location = request.args.get("location")

    query = Case.query
    if status:
        query = query.filter(Case.status.ilike(f"%{status}%"))
    if year:
        query = query.filter(Case.year == year)
    if location:
        query = query.filter(Case.location.ilike(f"%{location}%"))

    return render_template("case_list.html", cases=query.all())



@app.route("/case/<case_id>", methods=["GET", "POST"])
def case_detail(case_id):
    # Find case by alphanumeric ID
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return render_template("case_detail.html", case=None), 404

    # Parse JSON safely
    try:
        details = json.loads(case.desc) if case.desc else {}
    except json.JSONDecodeError:
        details = {}

    # Auto-fetch Unsplash image
    image_url = fetch_case_image(case.title)
    gallery = [image_url]

    # Extract fields safely from details JSON
    story = details.get("story", {})
    rumors = details.get("rumors", [])
    investigation = details.get("investigation", {})
    suspects = details.get("suspects", [])
    timeline = details.get("timeline", [])
    impact = details.get("impact", {})
    evidence = details.get("evidence", [])
    podcast = details.get("podcast", [])
    reddit_links = details.get("reddit", [])
    suggestions = details.get("suggestions", [])
    map_data = details.get("location", {})

    # Map for iframe embedding
    if isinstance(map_data, dict) and "lat" in map_data and "lng" in map_data:
        map_embed = f"https://www.google.com/maps?q={map_data['lat']},{map_data['lng']}&output=embed"
    else:
        map_embed = f"https://www.google.com/maps?q={case.location.replace(' ', '+')}&output=embed"

    # Handle review submission
    if request.method == "POST":
        review_text = request.form.get("review")
        user = current_user.username if current_user.is_authenticated else "Anonymous"
        if review_text:
            review = Review(case_id=case_id, user=user, text=review_text)
            db.session.add(review)
            db.session.commit()
            flash("Review added!", "success")
            return redirect(url_for("case_detail", case_id=case_id))

    reviews = Review.query.filter_by(case_id=case_id).all()

    # Render detail page with all extracted data
    return render_template(
        "case_detail.html",
        case=case,
        details=details,
        gallery=gallery,
        story=story,
        rumors=rumors,
        investigation=investigation,
        suspects=suspects,
        timeline=timeline,
        impact=impact,
        evidence=evidence,
        podcast=podcast,
        reddit_links=reddit_links,
        suggestions=suggestions,
        map_embed=map_embed,
        reviews=reviews
    )


@app.route("/case/<case_id>/download")
def case_download(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return "Case not found", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{case.title}</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Genre: {case.genre} | Status: {case.status} | Location: {case.location} | Year: {case.year}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(case.desc or "", styles["Normal"]))
    story.append(Spacer(1, 12))

    reviews = Review.query.filter_by(case_id=case_id).all()
    if reviews:
        story.append(Paragraph("<b>User Reviews:</b>", styles["Heading2"]))
        for r in reviews:
            story.append(Paragraph(f"{r.user}: {r.text}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{case.title}.pdf", mimetype="application/pdf")



@app.route("/leaderboard")
def leaderboard():
    rows = Leaderboard.query.order_by(Leaderboard.points.desc()).all()
    if not rows:
        rows = [type("TempRow", (), r)() for r in LEADERBOARD]
    return render_template("leaderboard.html", rows=rows)


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/admin")
@login_required
def admin():
    stats = {
        "total_cases": Case.query.count(),
        "solved_cases": Case.query.filter(Case.status.ilike("%solved%")).count(),
        "users_active": 85,  # placeholder
    }
    return render_template("admin.html", cases=Case.query.all(), stats=stats)



@app.route("/api/case/<case_id>")
def api_case(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return jsonify({}), 404
    try:
        details = json.loads(case.desc) if case.desc else {}
    except:
        details = {}
    return jsonify({
        "title": case.title,
        "status": case.status,
        "date_reported": case.year,
        "summary": details.get("summary", ""),
        "facts": details.get("facts", []),
        "victim_name": details.get("victim_name", ""),
        "victim_age": details.get("victim_age", ""),
        "last_location": details.get("location", {})
    })


@app.route("/api/case/photos/<case_id>")
def api_case_photos(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return jsonify([])
    try:
        details = json.loads(case.desc)
    except:
        details = {}
    return jsonify(details.get("gallery", []))


@app.route("/api/case/recordings/<case_id>")
def api_case_recordings(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return jsonify([])
    try:
        details = json.loads(case.desc)
    except:
        details = {}
    return jsonify(details.get("podcast", []))


@app.route("/api/case/reddit/<case_id>")
def api_case_reddit(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return jsonify([])
    try:
        details = json.loads(case.desc)
    except:
        details = {}
    return jsonify(details.get("reddit", []))


@app.route("/api/case/suggestions/<case_id>")
def api_case_suggestions(case_id):
    case = Case.query.filter_by(id=case_id).first()
    if not case:
        return jsonify([])
    try:
        details = json.loads(case.desc)
    except:
        details = {}
    return jsonify(details.get("suggestions", []))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
