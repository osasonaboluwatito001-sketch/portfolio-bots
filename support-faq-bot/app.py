"""Flask web endpoint: POST /ask {"question": "..."}."""
import os

from flask import Flask, jsonify, request

from faq_engine import FAQEngine


def create_app(engine: FAQEngine | None = None) -> Flask:
    app = Flask(__name__)
    eng = engine or FAQEngine.from_file(os.getenv("FAQ_PATH", "faq.json"),
                                        float(os.getenv("FAQ_THRESHOLD", "0.5")))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/ask")
    def ask():
        data = request.get_json(silent=True) or {}
        q = data.get("question")
        if not isinstance(q, str) or not q.strip():
            return jsonify(error="JSON body must include a non-empty 'question' string"), 400
        m = eng.ask(q)
        if not m:
            return jsonify(matched=False, answer=None,
                           suggestions=[s.question for s in eng.rank(q)])
        return jsonify(matched=True, answer=m.answer, question=m.question, score=m.score)

    return app


if __name__ == "__main__":
    create_app().run(port=int(os.getenv("PORT", "5000")))
