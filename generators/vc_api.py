#!/bin/python3
import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--operation", required=True, choices=["issue-credential", "prove-presentation"])
parser.add_argument("-e", "--endpoint", required=True)
parser.add_argument("--jwt", metavar="JWT", help="Generators can choose between RS256 and ES256K private keys to generate JWS for verifiable credentials and presentations. contains a base64encoded JSON object containing es256kPrivateKeyJwk and rs256PrivateKeyJwk.")
parser.add_argument("--jwt_aud", "--jwt-aud", metavar="AUD", help="Generators have to use <AUD> as the aud attribute in all JWTs")
parser.add_argument("--jwt_no_jws", "--jwt-no-jws", action="store_true", help="Generators have to suppress the JWS although keys are present")
parser.add_argument("--jwt_presentation", "--jwt-presentation", action="store_true", help="Generators have to generate a verifiable presentation")
parser.add_argument("--jwt_decode", "--jwt-decode", action="store_true", help="	Generators have to generate a credential from a JWT verifiable credential. The input file will be a JWT instead of a JSON-LD file.")
parser.add_argument("input")
args = parser.parse_args()

HEADERS = {
    "Content-Type": "application/json"
    }

with open(args.input, "r") as f:
    try:
        INPUT = json.loads(f.read())
    except json.decoder.JSONDecodeError:
        INPUT = f.read()

if args.operation == "issue-credential":
    OPTIONS = {}
    DATA = {
        "credential": INPUT,
        "options": OPTIONS
    }
    DATA = json.dumps(DATA)
    r = requests.post(f"{args.endpoint}/credentials/issue", headers=HEADERS, data=DATA)
    if r.status_code != 200:
        raise RuntimeError(r.text)
    else:
        print(r.json())

elif args.operation == "prove-presentation":
    OPTIONS = {}
    DATA = {
        "presentation": INPUT,
        "options": OPTIONS
    }
    DATA = json.dumps(DATA)
    r = requests.post(f"{args.endpoint}/presentations/prove", headers=HEADERS, data=DATA)
    if r.status_code != 200:
        raise RuntimeError(r.text)
    else:
        print(r.json())