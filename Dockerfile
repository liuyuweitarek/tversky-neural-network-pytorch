ARG UBUNTU_VERSION \
    PYTHON_VERSION \
    PROJECT_NAME

FROM ubuntu:${UBUNTU_VERSION}

ARG UBUNTU_VERSION \
    PYTHON_VERSION \
    PROJECT_NAME

ENV DEBIAN_FRONTEND=noninteractive \
    UBUNTU_VERSION=${UBUNTU_VERSION} \
    PYTHON_VERSION=${PYTHON_VERSION} \
    PROJECT_NAME=${PROJECT_NAME}\
    # UV Configuration
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=0 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python${PYTHON_VERSION}

RUN apt-get update \
    && apt install --no-install-recommends -y curl wget build-essential gpg-agent software-properties-common python-pkg-resources\
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=/root/.local/bin/:$PATH

WORKDIR /code

RUN printf '#!/bin/bash\n\
if [ ! -d $PROJECT_NAME ]; then\n\
    uv init --package $PROJECT_NAME --python=$PYTHON_VERSION;\n\
fi\n\
\n\
cd $PROJECT_NAME;\n\
\n\
exec "$@"\n' > /usr/local/bin/entrypoint.sh \
  && chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]