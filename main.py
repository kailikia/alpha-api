import sentry_sdk, psycopg2
from flask import Flask, render_template, flash
from sentry_sdk import capture_exception

sentry_sdk.init(
    dsn="https://30b24fa91ed74de1b6e8fe93011d80ac@us.sentry.io/4506695594016768",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app=Flask(__name__)
app.secret_key='secretkey'

try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
except Exception as e:
    capture_exception(e)

@app.route("/products")
def prods():
    try:
        cur = conn.cursor()
        cur.execute("Select * from products")
        prods = cur.fetchall()
        flash("Products fetched succcessfully.")
        return render_template("products.html", prods=prods)
    except Exception as e:
        capture_exception(e)
        flash("Server error. Try again later.")
        return render_template("products.html")
app.run()