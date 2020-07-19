
# jupyterhub-prometheus-grafana

Demo of proxying grafana as hub service.

## How to try it

* Clone repo
* Look at Dockerfile to see how test accounts are set up
* Then do `docker-compose up`
* Point browser at http://localhost:8000

## What is going on

The default url is set to `/hub/home` since I'm mostly interested in the service here.
Grafana appears as a hub service via a proxy service (see services dropdown).
The proxy service is mostly a rip-off of jupyter-server-proxy.
There's some hard code here and there too.
WebSockets would be an issue here but I think it could be handled.

Grafana is configured so auth is turned off since the proxy handles that.
Again only admins are expected to look at this.
Non admin's get a 403, it's probably better to keep it from appearing to them in the dropdown.

## Feedback?

If there's a better way to do this I'm interested in suggestions.
For instance is there already a generic proxy I could use as a hub service for anything, with hub authentication?

Are there arguments for not proxying Grafana as a hub service?
I as an admin would find it useful to do this and probably will.

A neat (?) idea might be to have the Grafana instance available to users too but it would show them their notebook stats?
The user would need to become authenticated to Grafana, there might be a way to do that.
