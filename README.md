# url_shortener

This is a URL shortener service which implements an (extremely restrictive) URL sanitation policy and brute force request throttling. It is written in Python and uses Redis as the perfect data store for such URL's.

This is designed to be a readable and concise demo highlighting things that need additional attention, but not really useful as is. (For example, URL sanitation is very strict; think carefully about what characters you will allow and deny for security; see below for details.)

Also, to be useful as more than a demo or HOWTO, some parts of this have to be rewritten to fit your framework (and pull requests are welcomed). Also, for readability, globals have been used, which may not be appropriate in your larger app.


    1.  Finish implementing URL sanitation.
        See https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet,
        RFC 3986, etc. Example provided uses a very strict whitelist and doesn't
        support unicode. using a blacklist would be far more useful.

    2.  Replace die() and get_requestor_fingerprint() with framework-specific code that actually
        does something relevant (ie emit appropriate HTTP status code or lookup
        requesting IP from HTTP headers. Note that only tracking IP will block legitimate
        requests, so a combination of techniques is suggested (external fingerprinting PLUS
        signed cookies is suggested; don't rely on cookies alone, as those are easily 
        or removed from the client side.)

    3.  (re)write methods and configure routing for your framework (see @get and @post comments)
