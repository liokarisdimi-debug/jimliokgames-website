from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)

# =========================================================
# CORS
# Επιτρέπει στο GitHub Pages site να επικοινωνεί με το API
# =========================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)


# =========================================================
# ROBLOX GAMES
# =========================================================

GAMES = {
    "ARMMAGEDON": 9972819827,
    "Jims Laser Tag": 9696622861,
    "Zombie World": 7949170676,
    "Mega Hyper Obby": 8772376332,
    "OP Fun Obby": 9705260160
}


# =========================================================
# API: /api/games
# =========================================================

@app.route("/api/games", methods=["GET"])
def games():

    results = []

    for name, universe_id in GAMES.items():

        url = (
            "https://games.roblox.com/v1/games"
            f"?universeIds={universe_id}"
        )

        try:

            response = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": "JimliokGames/1.0"
                }
            )

            print(
                f"[Roblox] {name} -> HTTP {response.status_code}"
            )

            if response.ok:

                data = response.json()

                if data.get("data"):

                    game = data["data"][0]

                    results.append({
                        "name": name,
                        "universeId": universe_id,
                        "visits": game.get(
                            "visits",
                            0
                        ),
                        "playing": game.get(
                            "playing",
                            0
                        ),
                        "favorites": game.get(
                            "favoritedCount",
                            0
                        ),
                        "likes": game.get(
                            "likeCount",
                            0
                        )
                    })

                else:

                    print(
                        f"[Roblox] No data for {name}"
                    )

            else:

                print(
                    f"[Roblox] Error {response.status_code} "
                    f"for {name}"
                )

        except requests.exceptions.Timeout:

            print(
                f"[Roblox] Timeout loading {name}"
            )

        except requests.exceptions.RequestException as error:

            print(
                f"[Roblox] Request error for "
                f"{name}: {error}"
            )

        except Exception as error:

            print(
                f"[Roblox] Unexpected error for "
                f"{name}: {error}"
            )


    return jsonify(results)


# =========================================================
# API STATUS
# =========================================================

@app.route("/api/status", methods=["GET"])
def status():

    return jsonify({
        "status": "online",
        "service": "Jimliok Games API",
        "roblox": "connected",
        "games": len(GAMES),
        "timestamp": int(time.time())
    })


# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Jimliok Games API</title>

        <style>

            body {
                margin: 0;
                background: #05060d;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }

            .box {
                text-align: center;
                padding: 40px;
                border-radius: 20px;
                background: #101326;
                border: 1px solid #292d4d;
                box-shadow:
                    0 0 50px rgba(100,60,255,.25);
            }

            h1 {
                color: #9b6cff;
            }

            .online {
                color: #22c55e;
                font-weight: bold;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>JIMLIOK GAMES API</h1>

            <p class="online">
                ● API ONLINE
            </p>

            <p>
                Roblox statistics server is running.
            </p>

            <p>
                <a
                    href="/api/games"
                    style="color:#8b5cf6"
                >
                    View Roblox Games API
                </a>
            </p>

        </div>

    </body>

    </html>
    """


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print("       JIMLIOK GAMES API")
    print("======================================")
    print("API: http://127.0.0.1:5000")
    print("Games: http://127.0.0.1:5000/api/games")
    print("Status: http://127.0.0.1:5000/api/status")
    print("======================================")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    ) 