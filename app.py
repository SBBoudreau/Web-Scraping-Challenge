from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo



import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)




@app.route("/")
def index():
    mars_results = mongo.db.mars.find_one()
    return render_template("index.html", mars_results=mars_results)


@app.route("/scrape")
def scraper():


    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert = True)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
