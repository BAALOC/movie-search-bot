# Movie Search Bot

## About

A Telegram bot for searching movies and series via the [Kinopoisk API](https://api.kinopoisk.dev). Users can look up titles by name, IMDB rating, or production budget, browse paginated results with inline keyboards, and track a personal search history with watched/unwatched status.

## Features

- **Title search** — query the Kinopoisk `/movie/search` endpoint and page through results inline.
- **Rating filter** — find movies by exact IMDB rating, sorted by vote count; genre filter applied from user settings.
- **Budget search** — separate commands for low-budget ($100K–$5M) and high-budget ($20M–$1B) films.
- **Search history** — persistent per-user log with date filtering and watched/unwatched toggle.
- **Per-user settings** — configurable result limit and genre whitelist, stored in SQLite and applied on every API request.

## Tech stack

**Bot layer**
- pyTelegramBotAPI 3.17.6 — handler registration, FSM states, inline/reply keyboards
- python-telegram-bot-pagination — inline paginator for multi-result displays

**Data**
- Peewee ORM + SQLite — two models: `User` (settings) and `Movie` (history entries)

**External API**
- Kinopoisk API v1.4 — `movie/search` (by title) and `movie` (filter queries)

**Config**
- python-dotenv — `BOT_TOKEN` and `API_KEY` loaded from `.env`

## Architecture

Handlers are registered by import side-effect: `main.py` does `import handlers`, which triggers `handlers/__init__.py` to import every submodule, attaching all `@bot.message_handler` and `@bot.callback_query_handler` decorators at startup.

Multi-step input flows (e.g. "send me the movie title") use pyTelegramBotAPI's `StatesGroup` with `StateMemoryStorage`. Each command sets a state; the follow-up handler filters on `state=UserState.X`, then resets to `UserState.base`.

Pagination keeps the current result set in a module-level `dict` keyed by `user_id`. This is intentionally in-memory — it resets on restart and isn't meant for persistence.

## Setup

1. Get a Kinopoisk API key from [@kinopoiskdev_bot](https://t.me/kinopoiskdev_bot) on Telegram.

2. Create `.env` in the project root:
   ```
   BOT_TOKEN=your_telegram_bot_token
   API_KEY=your_kinopoisk_api_key
   ```

3. Install dependencies:
   ```sh
   uv pip install -r requirements.txt
   ```

4. Run:
   ```sh
   python main.py
   ```

## Usage

```
/movie_search
> Bot: Enter a movie title
You: Inception
> Bot: [paginated inline results with title, description, IMDB rating, year, genre, age rating, poster]
```

Use the inline arrow buttons to page through results. The `◀️ Back` button returns to the main menu. All searched titles are automatically saved to your history (`/history`).