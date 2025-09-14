# data.py
CASES = {
    "mh370": {
        "id": "mh370",
        "title": "Malaysia Airlines 370",
        "genre": "Aviation Mystery",
        "status": "Cold Case",
        "location": "Indian Ocean",
        "year": 2014,
        "desc": "Flight vanished over the Indian Ocean. Satellite pings, last ATC comms and debris remain key clues.",
        "image": "/static/images/malaysia-crash.jpeg",
        "evidence": ["Last ATC comms", "Satellite pings", "Debris on beaches"]
    },
    "zodiac": {
        "id": "zodiac",
        "title": "The Zodiac Killer",
        "genre": "Serial Killer",
        "status": "Unsolved",
        "location": "California, USA",
        "year": 1969,
        "desc": "Cryptic letters, ciphers and claimed murders plagued California in the late 60s.",
        "image": "/static/images/zodiac-killer.jpeg",
        "evidence": ["Letters & ciphers", "Eyewitness sketches", "Police reports"]
    },
    "dyatlov": {
        "id": "dyatlov",
        "title": "Dyatlov Pass Incident",
        "genre": "Expedition Mystery",
        "status": "Cold Case",
        "location": "Ural Mountains, Russia",
        "year": 1959,
        "desc": "Nine hikers dead under bizarre conditions—radiation, torn tents and unexplained trauma.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/71/Dyatlov_Pass_incident_02.jpg",
        "evidence": ["Torn tents", "Radiation traces", "Strange injuries"]
    }
}

LEADERBOARD = [
    {"rank": 1, "username": "DetectiveX", "points": 1500},
    {"rank": 2, "username": "MysterySolver", "points": 1200},
    {"rank": 3, "username": "ColdCaseNerd", "points": 980},
]
