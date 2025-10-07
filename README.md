

> Publish-subscibe from HTML <br /><br />
---
> curl http://localhost:5000/list-subscribers <br />
> <br />
> curl -X POST   -H "Content-Type: application/json"   -d '{"name":"Bob","URI":"http://other.good.site.com"}'   http://localhost:5000/add-subscriber <br />