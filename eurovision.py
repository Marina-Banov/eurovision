import json
from app import app, models


@app.cli.command("seed")
def seed():
    with open("seed.json", 'r', encoding="utf8") as f:
        data = json.load(f)
        models.Country.clean()
        for i in data["Country"]:
            models.Country.seed(i)
