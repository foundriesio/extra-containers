# Repo in a multiarch container and a wrapper script

[![Microbadger](https://images.microbadger.com/badges/image/linarotechnologies/repo.svg)](http://microbadger.com/images/linarotechnologies/repo "Image size")
[![Docker Stars](https://img.shields.io/docker/stars/linarotechnologies/repo.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/repo/)
[![Docker Pulls](https://img.shields.io/docker/pulls/linarotechnologies/repo.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/repo/)


### How to use this image with default widgets

```
ruby -e "$(curl -o repo https://raw.githubusercontent.com/linaro-technologies/extra-containers/master/repo/repo)"
chmod +x repo

./repo init -u http://url to repo
./repo sync
```

This will run repo in an isolated container.
