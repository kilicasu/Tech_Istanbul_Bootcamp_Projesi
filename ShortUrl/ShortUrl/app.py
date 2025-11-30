from flask import Flask, render_template, request, redirect, url_for, flash
from models import URL, db
from helpers import generate_short_code
import validators

app = Flask(__name__)

# Database ayarları
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/asuma/Desktop/TechIstanbulProje/ShortUrl/urlshortener.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "gizli-key"

# Database başlatma
db.init_app(app)
with app.app_context():
    db.create_all()

# Ana sayfa ve URL kısaltma
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("original_url")
        if not original_url or not validators.url(original_url):
            flash("Lütfen geçerli bir URL girin", "error")
            return redirect(url_for("index"))

        short_url = generate_short_code()
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        flash("URL başarıyla kısaltıldı!", "success")
        # POST sonrası redirect → PRG pattern
        return redirect(url_for("index"))

    urls = URL.query.order_by(URL.id.desc()).all()
    return render_template("index.html", urls=urls)

# Kısa URL yönlendirme
@app.route("/<short_url>")
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if not url:
        return "URL bulunamadı", 404

    url.visit_count += 1
    db.session.commit()
    return redirect(url.original_url)

# API endpoint
@app.route("/api/urls")
def api_urls():
    urls = URL.query.order_by(URL.id.desc()).all()
    data = []
    for u in urls:
        data.append({
            "original_url": u.original_url,
            "short_url": request.host_url + u.short_url,
            "visit_count": u.visit_count
        })
    return {"urls": data}

if __name__ == "__main__":
    app.run(debug=True)
