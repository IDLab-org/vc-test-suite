#!/bin/python3
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--operation", required=True, choices=["test-credential", "test-presentation"])
parser.add_argument("-e", "--endpoint", required=True)
parser.add_argument("--jwt", metavar="JWT", help="Generators can choose between RS256 and ES256K private keys to generate JWS for verifiable credentials and presentations. contains a base64encoded JSON object containing es256kPrivateKeyJwk and rs256PrivateKeyJwk.")
parser.add_argument("--jwt_aud", "--jwt-aud", metavar="AUD", help="Generators have to use <AUD> as the aud attribute in all JWTs")
parser.add_argument("--jwt_no_jws", "--jwt-no-jws", action="store_true", help="Generators have to suppress the JWS although keys are present")
parser.add_argument("--jwt_presentation", "--jwt-presentation", action="store_true", help="Generators have to generate a verifiable presentation")
parser.add_argument("--jwt_decode", "--jwt-decode", action="store_true", help="	Generators have to generate a credential from a JWT verifiable credential. The input file will be a JWT instead of a JSON-LD file.")
parser.add_argument("input")
args = parser.parse_args()

with open(args.input, "r") as f:
    DATA = f.read()
HEADERS = {
    "Content-Type": "application/json"
    }

if args.operation == "test-credential":
    r = requests.post(f"{args.endpoint}/createCredFromInput", headers=HEADERS, data=DATA)
    if r.status_code != 200:
        raise RuntimeError(r.text)
    else:
        print(r.json()["VcToken"])

elif args.operation == "test-presentation":
    r = requests.post(f"{args.endpoint}/createpresentationToken", headers=HEADERS, data=DATA)
    if r.status_code != 200:
        raise RuntimeError(r.text)
    else:
        print(r.json()["VpToken"])