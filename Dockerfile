FROM alpine

COPY bot.py /bot/bot.py
COPY exec.sh /bot/exec.sh

RUN \
    chmod +x /bot/exec.sh && \
    apk add --update --no-cache python3 python3-dev cmd:pip3 build-base tzdata && \
    pip3 install --upgrade pip && \
    pip3 install aiogram pyyaml && \
    rm -rf /var/cache/apk/*

CMD ["/bot/exec.sh"]
