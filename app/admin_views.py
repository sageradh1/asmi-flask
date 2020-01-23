from app import app

@app.route("/admin/dashboard")
def admin_dashboard():
    return "Admin Dashboard"

@app.route("/admin/profile")
def admin_profile():
    return "Profile of admin"