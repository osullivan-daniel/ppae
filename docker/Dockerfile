FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    ssh \
    vim \
    apt-transport-https \
    ca-certificates \
    sudo\
    build-essential \
    curl \
    file \
    git \
    libglib2.0-0 \
    libcairo2 \
    libgtk-3-0 \
    libxml2 \
    libbrotli1 \
    libgl1 \
    libegl1 \
    libnotify4 \
    libgdk-pixbuf2.0-0 \
    libvpx5 \
    libopus0 \
    libicu60 \
    libxslt1.1 \
    libwoff1 \
    libfontconfig1 \
    libfreetype6 \
    libharfbuzz0b\
    libharfbuzz-icu0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    libjpeg-turbo8 \
    libpng16-16 \
    libopenjp2-7 \
    libwebpdemux2 \
    libwebp6 \
    libenchant1c2a \
    libsecret-1-0 \
    libhyphen0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libwayland-server0 \
    libwayland-egl1 \
    libwayland-client0 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libxkbcommon0 \
    libepoxy0 \
    libatk-bridge2.0-0 \
    libgles2 \
    gstreamer1.0-libav \
    libdbus-glib-1-2 \
    libxt6 \
    libnss3 \
    libnspr4 \
    --no-install-recommends \
    && apt-get purge

RUN groupadd -r keyserSoze && useradd -r -g keyserSoze keyserSoze \
    && mkdir -p /home/keyserSoze && chown -R keyserSoze:keyserSoze /home/keyserSoze

USER keyserSoze

RUN git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew \
    && mkdir ~/.linuxbrew/bin \
    && ln -s ../Homebrew/bin/brew ~/.linuxbrew/bin \
    && eval $(~/.linuxbrew/bin/brew shellenv) \
    && brew install allure \
    && pip3 install pytest \
    allure-pytest \
    pytest-playwright \
    beautifulsoup4 \
    && python3 -m playwright install

WORKDIR /home/keyserSoze

ENTRYPOINT ["/bin/bash"]

