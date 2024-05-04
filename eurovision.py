import json
from app import app, models


@app.cli.command("seed")
def seed():
    with open("seed.json", "r", encoding="utf8") as f:
        data = json.load(f)
        models.Country.clean()
        for year in data:
            for i in data[year]:
                models.Country.seed({**i, "year": int(year)})
