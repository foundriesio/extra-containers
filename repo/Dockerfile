FROM opensourcefoundries/minideb:stretch

RUN install_packages ca-certificates curl git-core python

RUN curl https://storage.googleapis.com/git-repo-downloads/repo > /bin/repo \
    && chmod a+x /bin/repo
