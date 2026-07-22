import os
from flask import Flask, render_template, request, session, redirect, url_for

from content import LAB

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "grc-labs-suite-dev-key")

ETYPE = LAB["exercise_type"]  # "maturity" | "risk_register" | "quiz"


def heat(score):
    if score <= 6:
        return "risk-low"
    if score <= 14:
        return "risk-med"
    return "risk-high"


def maturity_summary(avg, max_score):
    ratio = avg / max_score if max_score else 0
    if ratio >= 0.8:
        return "Strong — well established"
    if ratio >= 0.55:
        return "Developing — foundational elements in place"
    if ratio >= 0.3:
        return "Weak — significant gaps remain"
    return "Not established — start here"


def compute_results(sc, answers):
    if ETYPE == "maturity":
        rows = []
        for item in sc["entries"]:
            raw = answers.get(item["id"], item.get("suggested", 0))
            try:
                score = int(raw)
            except (TypeError, ValueError):
                score = int(item.get("suggested", 0))
            rows.append({
                "id": item["id"], "label": item["label"], "score": score,
                "slabel": LAB["scale"].get(score, ""),
            })
        max_score = max(LAB["scale"].keys())
        avg = round(sum(r["score"] for r in rows) / len(rows), 2) if rows else 0
        lowest = sorted(rows, key=lambda r: r["score"])[:3]
        return {"rows": rows, "avg": avg, "max": max_score, "lowest": lowest,
                "summary": maturity_summary(avg, max_score)}

    if ETYPE == "risk_register":
        rows = []
        for item in sc["entries"]:
            like = int(answers.get(f"like__{item['id']}", item.get("likelihood", 3)))
            impact = int(answers.get(f"impact__{item['id']}", item.get("impact", 3)))
            treat = answers.get(f"treat__{item['id']}", item.get("treatment", "Mitigate"))
            score = like * impact
            rows.append({
                "id": item["id"], "label": item["label"], "likelihood": like,
                "impact": impact, "score": score, "treatment": treat, "heat": heat(score),
            })
        rows.sort(key=lambda r: -r["score"])
        return {"rows": rows, "top": rows[:3]}

    if ETYPE == "quiz":
        tally = {}
        for item in sc["entries"]:
            chosen = answers.get(item["id"], item.get("suggested"))
            opt = next((o for o in item["options"] if o["value"] == chosen), None)
            if opt:
                tally[opt["category"]] = tally.get(opt["category"], 0) + 1
        best = max(tally, key=tally.get) if tally else None
        recommendation = LAB.get("recommendations", {}).get(best) if best else None
        return {"tally": tally, "best": best, "recommendation": recommendation}

    return {}


@app.route("/")
def index():
    return render_template("index.html", lab=LAB)


@app.route("/exercise/<scenario>", methods=["GET", "POST"])
def exercise(scenario):
    if scenario not in LAB["scenarios"]:
        return redirect(url_for("index"))
    sc = LAB["scenarios"][scenario]
    key = f"answers__{scenario}"

    if request.method == "POST":
        answers = {}
        if ETYPE == "risk_register":
            for item in sc["entries"]:
                for prefix in ("like__", "impact__", "treat__"):
                    field = f"{prefix}{item['id']}"
                    if field in request.form:
                        answers[field] = request.form.get(field)
        else:
            for item in sc["entries"]:
                if item["id"] in request.form:
                    answers[item["id"]] = request.form.get(item["id"])
                elif f"ans__{item['id']}" in request.form:
                    answers[item["id"]] = request.form.get(f"ans__{item['id']}")
        session[key] = answers
        return redirect(url_for("results", scenario=scenario))

    answers = session.get(key, {})
    return render_template("exercise.html", lab=LAB, scenario=scenario, sc=sc, answers=answers)


@app.route("/results/<scenario>")
def results(scenario):
    if scenario not in LAB["scenarios"]:
        return redirect(url_for("index"))
    sc = LAB["scenarios"][scenario]
    answers = session.get(f"answers__{scenario}", {})
    computed = compute_results(sc, answers)
    return render_template("results.html", lab=LAB, scenario=scenario, sc=sc,
                            answers=answers, computed=computed)


@app.route("/reset/<scenario>")
def reset(scenario):
    session.pop(f"answers__{scenario}", None)
    return redirect(url_for("exercise", scenario=scenario))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
