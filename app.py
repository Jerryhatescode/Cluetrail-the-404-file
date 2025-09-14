import random
import json
import io
from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, current_user, login_required
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


from models import db, User, Case, Review, Leaderboard


from auth import auth_bp


app = Flask(__name__)
app.secret_key = "change-this-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clue_trail.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


WORDS = ["cop", "hide", "spy", "agent", "fbi", "clue", "case", "shadow", "hunter"]

def is_safe_url(target):
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@app.context_processor
def inject_globals():
    return {"current_user": current_user, "is_authenticated": current_user.is_authenticated}


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
    case = Case.query.get(case_id)
    if not case:
        return render_template("case_detail.html", case=None), 404

    try:
        details = json.loads(case.desc) if case.desc else {}
    except json.JSONDecodeError:
        details = {}

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
    return render_template("case_detail.html", case=case, details=details, reviews=reviews)


@app.route("/case/<case_id>/download")
def case_download(case_id):
    case = Case.query.get(case_id)
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

    if case.reviews:
        story.append(Paragraph("<b>User Reviews:</b>", styles["Heading2"]))
        for r in case.reviews:
            story.append(Paragraph(f"{r.user}: {r.text}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{case.title}.pdf", mimetype="application/pdf")


@app.route("/leaderboard")
def leaderboard():
    rows = Leaderboard.query.order_by(Leaderboard.points.desc()).all()
    return render_template("leaderboard.html", rows=rows)
@app.route("/blog")
def blog():
    return render_template("blog.html")
# in your blueprint or app.py

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


with app.app_context():
    db.create_all()

if __name__ == "__main__":
   app.run(debug=True)
