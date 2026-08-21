from flask import Flask, jsonify
import requests

app = Flask(__name__)

GAMES = {
    "ARMMAGEDON": 9972819827,
    "Jims Laser Tag": 9696622861,
    "Zombie World": 7949170676,
    "Mega Hyper Obby": 8772376332
}


@app.route("/api/games")
def games():

    results = []

    for name, universe_id in GAMES.items():

        url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"

        try:
            response = requests.get(url, timeout=10)

            if response.ok:

                data = response.json()

                if data.get("data"):

                    game = data["data"][0]

                    results.append({
                        "name": name,
                        "universeId": universe_id,
                        "visits": game.get("visits", 0),
                        "playing": game.get("playing", 0),
                        "favorites": game.get("favoritedCount", 0),
                        "likes": game.get("likeCount", 0)
                    })

        except Exception as error:

            print(
                f"Error loading {name}: {error}"
            )

    return jsonify(results)


@app.route("/")
def home():

    return """
    <h1>Jimliok Games API</h1>
    <p>Live Roblox statistics server is running.</p>
    """


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )