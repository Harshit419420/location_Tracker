from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)

@app.route("/lookup", methods=["POST"])
def lookup_number():
    data = request.get_json()
    phone = data.get("phone")

    try:
        parsed = phonenumbers.parse(phone)

        if not phonenumbers.is_valid_number(parsed):
            return jsonify({"error": "Invalid phone number"}), 400

        result = {
            "phone": phone,
            "country_region": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "time_zone": list(timezone.time_zones_for_number(parsed))
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
