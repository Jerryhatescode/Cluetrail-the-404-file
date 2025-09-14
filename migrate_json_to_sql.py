import json
from app import db, Case, Review, Leaderboard, app

# Load JSON files
with open("cases.json", "r", encoding="utf-8") as f:
    cases_data = json.load(f)

with open("leaderboard.json", "r", encoding="utf-8") as f:
    leaderboard_data = json.load(f)

with app.app_context():
    # ----- Import Cases -----
    for cid, c in cases_data.items():
        case = Case.query.get(cid)
        if not case:
            case = Case(id=cid)
            db.session.add(case)

        # Store full JSON in desc
        case.desc = json.dumps(c)

        # ----- Handle NOT NULL fields safely -----
        case.title = c.get("title") or c.get("name") or "Untitled"
        case.genre = c.get("genre") or c.get("type")
        case.status = c.get("status") or "Unknown"

        # Serialize location if it's a dict
        location = c.get("location")
        if isinstance(location, dict):
            case.location = json.dumps(location)
        else:
            case.location = location or "Unknown"

        # Extract year from 'year' or 'date'
        year = c.get("year")
        if not year and c.get("date"):
            try:
                year = int(c["date"].split("-")[0])
            except ValueError:
                year = None
        case.year = year

        case.image = c.get("image")

        # ----- Import Reviews -----
        for r in c.get("reviews", []):
            existing_review = Review.query.filter_by(
                case_id=cid, user=r.get("user"), text=r.get("text")
            ).first()
            if not existing_review:
                review = Review(case_id=cid, user=r.get("user", "Anonymous"), text=r.get("text"))
                db.session.add(review)

    db.session.commit()

    # ----- Import Leaderboard -----
    for r in leaderboard_data:
        existing_lb = Leaderboard.query.filter_by(user=r.get("user")).first()
        if not existing_lb:
            lb = Leaderboard(user=r.get("user"), points=r.get("points", 0))
            db.session.add(lb)

    db.session.commit()

print("Migration completed successfully!")
