from shortuuid import uuid as shortuuid
from redis import StrictRedis as Redis
from time import sleep
import string

rds = Redis()
api_path = "/api/"
base_url = "https://localhost" + api_path

def die(code, error):
    print code, '{error: "%s"}' % error

def get_requestor_fingerprint():
    # IP alone is not ideal.. defeats proxies.
    # try to fingerprint remote hosts
    # instead or use unique cookies
    return "192.168.1.1"

def check_throttle(ttl=1):
    if rds.get("throttle:%s" % get_requestor_fingerprint()):
        sleep(ttl)
        die(403, "Request throttled.")

def set_throttle(ttl=5):
    # throttle bad requests
    rds.setex(get_requestor_fingerprint(), ttl, True)

def whitelist_text(text, safe=""):
    return ''.join([c for c in text
        if c in (safe or string.ascii_letters + string.digits)])

def blacklist_text(text, bad=""):
    return ''.join([c for c in text
        if c not in (bad or "<>?#&\"'\\\n\r")])

# @get(api_path + "code/<code>")
def lookup_url(code):
    check_throttle()
    code = whitelist_text(code)
    url = rds.get(code)
    if not url:
        set_throttle()
        die(404, "URL expired.")
    return whitelist_text(url,
        safe=string.printable)

# @post(api_path + "url/<url>")
def generate_code(url):
    code = shortuuid()
    days = 365
    rds.setex(code, days * 86400, url)
    set_throttle()
    return code

if __name__ == "__main__":
    # demo:
    url = "https://example.com/a/b/c"
    print "URL: " + url
    code = generate_code(url)
    print "Shortened URL: " + base_url + code
    print "Looking up code: " + code
    print "URL: " + lookup_url(code)

