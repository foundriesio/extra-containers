Python Flask Web Application for controlling a ZmP Candy Dispenser.

## How to use this image

```
docker run -it --rm --name candy-dispenser -p 5000:5000 -e HOST=https://mgmt.foundries.io/lshan -e CLIENT=zmp:sn:1d0ca460 hub.foundries.io/candy-dispenser:latest

The dashboard can be viewed at http://localhost:5000

```
