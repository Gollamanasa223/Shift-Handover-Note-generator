import json
import pandas as pd
from datetime import datetime, timedelta


# -----------------------------
# Discord Loader
# -----------------------------
def load_discord_export(file):

    try:
        data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Discord export must be a list of messages."
            )

        required_fields = [
            "author",
            "message",
            "timestamp"
        ]

        for i, msg in enumerate(data):

            for field in required_fields:

                if field not in msg:
                    raise ValueError(
                        f"Message {i + 1} missing field: {field}"
                    )

        return data

    except json.JSONDecodeError:
        raise ValueError(
            "Invalid JSON format in Discord export."
        )


# -----------------------------
# Ticket Loader
# -----------------------------
def load_tickets_csv(file):

    try:
        df = pd.read_csv(file)

        required_columns = [
            "TicketID",
            "Issue",
            "Status"
        ]

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing ticket columns: {missing}"
            )

        return df

    except Exception as e:
        raise ValueError(
            f"Invalid CSV file: {str(e)}"
        )


# -----------------------------
# Last 12 Hours Filter
# -----------------------------
def filter_last_12_hours(discord_data):

    filtered = []

    cutoff = datetime.now() - timedelta(hours=12)

    for msg in discord_data:

        try:

            timestamp = datetime.strptime(
                msg["timestamp"],
                "%Y-%m-%d %H:%M"
            )

            if timestamp >= cutoff:
                filtered.append(msg)

        except Exception:
            # Skip malformed timestamps
            continue

    return filtered


# -----------------------------
# Build Combined Context
# -----------------------------
def build_combined_text(discord_data, tickets_df):

    discord_data = filter_last_12_hours(
        discord_data
    )

    combined_text = ""

    combined_text += "DISCORD MESSAGES\n"
    combined_text += "=" * 40 + "\n"

    for msg in discord_data:

        author = msg.get(
            "author",
            "Unknown"
        )

        timestamp = msg.get(
            "timestamp",
            "Unknown Time"
        )

        channel = msg.get(
            "channel",
            "general"
        )

        message = msg.get(
            "message",
            ""
        )

        combined_text += (
            f"[{timestamp}] "
            f"{author} "
            f"({channel}): "
            f"{message}\n"
        )

    combined_text += "\n\n"

    combined_text += "TICKETS\n"
    combined_text += "=" * 40 + "\n"

    combined_text += tickets_df.to_string(
        index=False
    )

    return combined_text