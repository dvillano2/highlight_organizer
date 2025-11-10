@bp.route("/info", methods=("GET"))
def info():
    return render_template("/schedule/info.html")
