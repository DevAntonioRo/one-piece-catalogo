from flask import Flask, abort, render_template, request

from data import CHARACTERS


def create_app():
    app = Flask(__name__)

    @app.template_filter("berries")
    def format_berries(value):
        return f"{value:,.0f}".replace(",", ".")

    @app.get("/")
    def index():
        query = request.args.get("q", "").strip().lower()
        crew = request.args.get("crew", "").strip()

        characters = CHARACTERS
        if query:
            characters = [
                character
                for character in characters
                if query in character["name"].lower()
                or query in character["epithet"].lower()
            ]
        if crew:
            characters = [character for character in characters if character["crew"] == crew]

        crews = sorted({character["crew"] for character in CHARACTERS})
        return render_template(
            "index.html",
            characters=characters,
            crews=crews,
            selected_crew=crew,
            query=request.args.get("q", "").strip(),
        )

    @app.get("/personagem/<slug>")
    def character_detail(slug):
        character = next((item for item in CHARACTERS if item["slug"] == slug), None)
        if character is None:
            abort(404)
        return render_template("detail.html", character=character)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
