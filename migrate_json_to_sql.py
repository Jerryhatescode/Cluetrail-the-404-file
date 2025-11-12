import json
from app import db, Case, Review, Leaderboard, app

# ---- Load JSON Files ----
with open("cases.json", "r", encoding="utf-8") as f:
    cases_data = json.load(f)

with open("leaderboard.json", "r", encoding="utf-8") as f:
    leaderboard_data = json.load(f)

with app.app_context():
    # ---- Normalize JSON format ----
    # Handle both dict {"id": {...}} and list [{...}] formats
    if isinstance(cases_data, list):
        cases_iter = [(c.get("id") or str(i), c) for i, c in enumerate(cases_data) if isinstance(c, dict)]
    else:
        cases_iter = cases_data.items()

    # ---- Import or Update Cases ----
    for cid, c in cases_iter:
        if not isinstance(c, dict):
            print(f"⚠️ Skipping invalid case entry: {cid}")
            continue

        case = Case.query.get(cid)
        if not case:
            case = Case(id=cid)
            db.session.add(case)

        # ---- Basic Info ----
        case.title = c.get("title") or c.get("name") or "Untitled Case"
        case.genre = c.get("genre") or c.get("type") or "Crime"
        case.status = c.get("status") or "Unknown"

        # ---- Location ----
        location = c.get("location")
        if isinstance(location, dict):
            case.location = json.dumps(location, ensure_ascii=False)
            case.lat = location.get("lat")
            case.lng = location.get("lng")
        else:
            case.location = location or "Unknown"

        # ---- Year ----
        year = c.get("year")
        if not year and c.get("date"):
            try:
                year = int(str(c["date"]).split("-")[0])
            except Exception:
                year = None
        case.year = year

        # ---- JSON Fields (story, rumors, timeline, etc.) ----
        json_fields = [
            "story", "rumors", "timeline", "evidence", "suspects",
            "gallery", "podcast", "reddit", "suggestions", "impact", "unsplash_queries"
        ]
        for field in json_fields:
            value = c.get(field)
            if value is not None:
                setattr(case, field, json.dumps(value, ensure_ascii=False))
            else:
                setattr(case, field, json.dumps({}, ensure_ascii=False))

        # ---- Backup Description ----
        case.desc = json.dumps(c, ensure_ascii=False)
        case.image = c.get("image")

        # ---- Reviews ----
        for r in c.get("reviews", []):
            if not isinstance(r, dict) or not r.get("text"):
                continue
            exists = Review.query.filter_by(case_id=cid, user=r.get("user"), text=r.get("text")).first()
            if not exists:
                db.session.add(Review(case_id=cid, user=r.get("user", "Anonymous"), text=r["text"]))

    db.session.commit()

    # ---- Leaderboard ----
    for r in leaderboard_data:
        if not isinstance(r, dict) or not r.get("user"):
            continue
        exists = Leaderboard.query.filter_by(user=r["user"]).first()
        if not exists:
            db.session.add(Leaderboard(user=r["user"], points=r.get("points", 0)))

    db.session.commit()

print("✅ Migration completed successfully with story, rumors, timeline, and leaderboard support!")
