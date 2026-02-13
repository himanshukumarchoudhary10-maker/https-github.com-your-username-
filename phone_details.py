import os
import argparse
import requests
import sys


def get_phone_details(number: str):
    """Fetch phone details from a configured API, or return demo data if no API key is set."""
    # Prefer Twilio lookup if Twilio credentials are present
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID") or os.environ.get("NUMBERLOOKUP_TWILIO_ACCOUNT_SID")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN") or os.environ.get("NUMBERLOOKUP_TWILIO_AUTH_TOKEN")

    if twilio_sid and twilio_token:
        url = f"https://lookups.twilio.com/v1/PhoneNumbers/{number}"
        # Request both carrier and caller-name when available
        params = [("Type", "carrier"), ("Type", "caller-name")]
        try:
            resp = requests.get(url, auth=(twilio_sid, twilio_token), params=params, timeout=10)
        except requests.RequestException as e:
            return {"error": f"Twilio request failed: {e}"}

        if resp.status_code != 200:
            # Twilio returns useful error body; bubble it up
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            return {"error": f"Twilio API returned {resp.status_code}: {body}"}

        try:
            data = resp.json()
        except ValueError:
            return {"error": "Invalid JSON response from Twilio."}

        # Twilio fields: phone_number, country_code, carrier (dict), caller_name (dict)
        carrier = data.get("carrier", {}) or {}
        caller = data.get("caller_name", {}) or {}

        details = {
            "Number": data.get("phone_number", number),
            "Name": caller.get("caller_name") or "N/A",
            "Location": f"{data.get('national_format','')}".strip(),
            "Carrier": carrier.get("name", "N/A"),
            "Country Code": data.get("country_code", "N/A"),
            "Phone Type": carrier.get("type", "N/A")
        }

        return details

    # Generic provider fallback (environment-configured URL + API key)
    api_key = os.environ.get("NUMBERLOOKUP_API_KEY")
    api_url = os.environ.get("NUMBERLOOKUP_API_URL")

    if not api_key or not api_url:
        # Demo/fallback data when no provider is configured
        return {
            "Number": number,
            "Name": "John Doe (demo)",
            "Location": "San Francisco CA",
            "Carrier": "Demo Carrier",
            "Country Code": "+1",
            "Phone Type": "mobile"
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(api_url, headers=headers, params={"number": number}, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}

    if resp.status_code != 200:
        return {"error": f"API returned status {resp.status_code}: {resp.text}"}

    try:
        data = resp.json()
    except ValueError:
        return {"error": "Invalid JSON response from API."}

    # Map common fields; APIs differ, so this is intentionally generic
    details = {
        "Number": data.get("number", number),
        "Name": data.get("name", data.get("owner", "N/A")),
        "Location": f"{data.get('city','N/A')} {data.get('region','')}".strip(),
        "Carrier": data.get("carrier", "N/A"),
        "Country Code": data.get("country_code", "N/A"),
        "Phone Type": data.get("phone_type", data.get("type", "N/A"))
    }

    return details


def main():
    parser = argparse.ArgumentParser(description="Lookup phone number details (demo if no API key).")
    parser.add_argument("--number", "-n", help="Phone number to lookup (e.g. +15555555555)")
    args = parser.parse_args()

    if args.number:
        number = args.number
    else:
        try:
            number = input("Enter the phone number: ")
        except (EOFError, KeyboardInterrupt):
            print("No number provided; exiting.")
            sys.exit(1)

    details = get_phone_details(number)

    print("\n--- Phone Details ---")
    if isinstance(details, dict):
        for k, v in details.items():
            print(f"{k}: {v}")
    else:
        print(details)
    print("---------------------")


if __name__ == "__main__":
    main()
