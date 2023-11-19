ARG PYTHON_VERSION=3.10.12

FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app
COPY ./backend .
#COPY . .

# Where store apt libs
ARG APT_LIB_DIR=/var/lib/apt
# Where store apt cache
ARG APT_CACHE_DIR=/var/cache/apt

RUN --mount=type=cache,target=$APT_CACHE_DIR,sharing=locked \
    --mount=type=cache,target=$APT_LIB_DIR,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache && \
    apt-get update && apt install tree

#RUN apt-get  update
#RUN apt install tree
RUN tree

COPY ./ci/requirements/backend-dev-requirements.txt ./requirements.txt
# RUN pip install -r requirements.txt

ARG PIP_CACHE_DIR=/var/cache/pip
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    pip install -r requirements.txt && rm requirements.txt
#CMD
CMD ["python","manage.py", "runserver","0.0.0.0:8000"]
