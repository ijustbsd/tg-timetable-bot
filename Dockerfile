FROM alpine

COPY bot.py /bot/bot.py
COPY exec.sh /bot/exec.sh

RUN \
    chmod +x /bot/exec.sh && \
    apk add --update --no-cache python3 tzdata && \
    pip3 install --upgrade pip && \
    pip3 install pyTelegramBotAPI pyyaml && \
    rm -rf /var/cache/apk/*

CMD ["/bot/exec.sh"]
