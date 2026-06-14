from src.utils import (
    load_discord_export,
    load_tickets_csv,
    build_combined_text
)

from src.llm_helper import (
    generate_handover_note
)


def process_handover(
    discord_file,
    ticket_file
):

    # -------------------------
    # File Validation
    # -------------------------
    if discord_file is None:
        raise ValueError(
            "Discord JSON file is required."
        )

    if ticket_file is None:
        raise ValueError(
            "Ticket CSV file is required."
        )

    # -------------------------
    # Load Data
    # -------------------------
    discord_data = load_discord_export(
        discord_file
    )

    tickets_df = load_tickets_csv(
        ticket_file
    )

    # -------------------------
    # Empty Data Checks
    # -------------------------
    if len(discord_data) == 0:
        raise ValueError(
            "Discord export contains no messages."
        )

    if tickets_df.empty:
        raise ValueError(
            "Ticket CSV contains no records."
        )

    # -------------------------
    # Build Context
    # -------------------------
    combined_text = build_combined_text(
        discord_data,
        tickets_df
    )

    if not combined_text.strip():
        raise ValueError(
            "No usable data found."
        )

    # -------------------------
    # Generate Report
    # -------------------------
    note = generate_handover_note(
        combined_text
    )

    if not note:
        raise ValueError(
            "Failed to generate handover note."
        )

    return note