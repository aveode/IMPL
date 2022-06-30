import requests
import hashlib
from getpass import getpass


def request_api(link, info):
    req = requests.get(f"{link}{info}")

    #return [req if req.status_code != "200"]
    if req.status_code == "200":
        return req
    else:
        raise RuntimeError


def sha1_password(pw):
    return str(hashlib.sha1(pw.encode('utf-8')).hexdigest()).upper()


def analyze_response(res, pw):
    hashes = (item.split(":") for item in res.text.splitlines())
    for hsh,count in hashes:
        if hsh == pw:
            return count

    return 0


def main():
    password = getpass("\n\n- Enter password -\n-> ")
    hashPassword = sha1_password(password)

    print(request_api("https://api.pwnedpasswords.com/range/", hashPassword[:5]))
    return
    res = request_api("https://api.pwnedpasswords.com/range/", hashPassword[:5])
    count = analyze_response(res, hashPassword[5:])

    if count:
        print(f"There was {count} leaks found, you should change your password.\n\nRead more at www.passwordsgenerator.net")
    else:
        print("No match found :)")


if __name__ == "__main__":
    main()