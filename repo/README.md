Android repo tool in a multiarch container and a wrapper script

## How to use this image

```

docker run --rm -v `pwd`:/src -v $HOME/.netrc:/root/.netrc repo init -u https://source.foundries.io/zmp-manifest
docker run --rm -v `pwd`:/src -v $HOME/.netrc:/root/.netrc repo sync
```
