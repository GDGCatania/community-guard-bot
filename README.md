# community-guard-bot

A Telegram bot built with Python for community management purposes (go away fake bots!).

## Requirements

- Python 3.13+
- `pixi` package manager
- Docker (optional)

## Environment Setup

Required environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot API token from [@BotFather](https://t.me/botfather) | Required |
| `LOG_LEVEL` | Logging configuration (`module=LEVEL`) | `__root__=INFO` |

Example:
```sh
export BOT_TOKEN="your_token_here"
export LOG_LEVEL="__root__=DEBUG,modules.bot=INFO"
```

## Project Structure

```
├── main.py               # Entry point
├── modules/
│   ├── bot/              # Telegram bot implementation 
│   │   └── __init__.py
│   ├── logging/          # Logging configuration
│   │   └── __init__.py
├── pixi.toml             # Dependencies
└── Dockerfile            # Container definition
```

## Development

1. Install dependencies:

```
pixi install
```

2. Run bot:

```
pixi run run
```

3. Code quality:

```
pixi run lint    # Lint code
```

## Docker Deployment

Build and run the bot:

```
docker build -t community-guard-bot .
docker run -e BOT_TOKEN=your_token_here community-guard-bot
```

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.