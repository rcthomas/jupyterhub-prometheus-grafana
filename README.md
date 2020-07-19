
# jupyterhub-prometheus-grafana

Demo of proxying grafana as hub service.

Should be just `docker-compose up` I think.

Grafana appears as a hub service via a proxy service.
The proxy service is just a rip-off of jupyter-server-proxy mostly.
There's some hard code here and there.
WebSockets would be an issue here but I think it could be handled.

Admin users are able to access Grafana but non-admin users can't.
It's probably a good idea to add some visibility control to hub services in JupyterHub.

If there's a better way to do this I'm interested in suggestions.
For instance is there already a generic proxy I could use as a hub service for anything, with hub authentication?

Are there arguments for not proxying Grafana as a hub service?
I as an admin would find it useful.

A neat (?) idea might be to have the Grafana instance available to users too but it would show them their notebook stats?
