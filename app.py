from flask import Flask, request, render_template, jsonify
import requests
import base64

app = Flask(__name__)

# Define Alloy API credentials
workflow_token = "workflow_token"
workflow_secret = "workflow_secret"

# Define API endpoint
api_url = "https://sandbox.alloy.co"

# Fnction to make API requests with HTTP Basic Auth
def make_api_request(data):
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{workflow_token}:{workflow_secret}".encode()).decode(),
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()

# Flask routes
@app.route("/", methods = ["GET", "POST"])

def application_form():
    if request.method == "POST":
        # Applicant details needed
        applicant_data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "address": {
                "line1": request.form["line1"],
                "line2": request.form["line2"],
                "city": request.form["city"],
                "state": request.form["state"],
                "zip": request.form["zip"],
                "country": request.form["country"],
            },
            "ssn": request.form["ssn"],
            "email": request.form["email"],
            "date_of_birth": request.form["date_of_birth"],
        }



        # Make API request
        response = make_api_request(applicant_data)

        # Process the response and display a message
        outcome = response.get({"summary":{"outcome":"Approved"}})#.get("outcome", "")


        if outcome == "Approved":
            message = "Success! Your account has been approved."
        elif outcome == "Manual Review":
            message = "Thanks for submitting your application. We'll be in touch shortly for a manual review."
        elif outcome == "Deny":
            message = "Sorry, your application was not successful."
        else:
            message = "An unknown error occurred."

        return render_template("result.html", message = message)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
