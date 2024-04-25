from urllib import request, parse

data = parse.urlencode({"text": "Done"}).encode()
req = request.Request(
    "https://api.chanify.net/v1/sender/CIDL3bMGEiJBQlM0QzVVRDROUkRLVUs2RkwyMkkyR1RWR1pGQ1lSUEVNGhT0a2z-IdYNqtsOK3Xkx2Yab9jqmCIECAEQAQ.pQ3yGhUPcXpdQXDUZw6h1cbb8lcBGaA3UMKE4Hci6fw",
    data=data,
)
request.urlopen(req)
