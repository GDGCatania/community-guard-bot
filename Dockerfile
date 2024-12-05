FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /app
COPY . .
RUN pixi install && rm -rf ~/.cache/rattler
EXPOSE 8000
CMD [ "pixi", "run", "run" ]
