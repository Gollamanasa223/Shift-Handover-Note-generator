import streamlit as st
from datetime import datetime

from src.processor import process_handover
from src.utils import (
    load_discord_export,
    load_tickets_csv
)
from src.external_data import (
    get_current_utc_time
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Shift Handover Note Generator",
    page_icon="📋",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📋 Shift Handover Note Generator")

st.write(
    "Upload the last 12 hours of Discord chat and ticket data "
    "to generate a structured handover report."
)

# -----------------------------
# File Uploaders
# -----------------------------
discord_file = st.file_uploader(
    "Discord Export (JSON)",
    type=["json"]
)

ticket_file = st.file_uploader(
    "Tickets (CSV)",
    type=["csv"]
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate Handover Note"):

    # Validate Uploads
    if discord_file is None:
        st.warning(
            "⚠️ Please upload a Discord JSON file."
        )
        st.stop()

    if ticket_file is None:
        st.warning(
            "⚠️ Please upload a Tickets CSV file."
        )
        st.stop()

    try:

        # -----------------------------
        # Read Data for Statistics
        # -----------------------------
        discord_file.seek(0)
        discord_data = load_discord_export(
            discord_file
        )

        ticket_file.seek(0)
        tickets_df = load_tickets_csv(
            ticket_file
        )

        discord_count = len(
            discord_data
        )

        ticket_count = len(
            tickets_df
        )

        # Reset file pointers
        discord_file.seek(0)
        ticket_file.seek(0)

        # -----------------------------
        # Generate Report
        # -----------------------------
        with st.spinner(
            "Generating handover note..."
        ):

            note = process_handover(
                discord_file,
                ticket_file
            )

        # -----------------------------
        # Success Message
        # -----------------------------
        st.success(
            "✅ Handover note generated successfully!"
        )

        # -----------------------------
        # Report Timestamp
        # -----------------------------
        st.info(
            f"🕒 Report Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # -----------------------------
        # External API Time
        # -----------------------------
        utc_time = get_current_utc_time()

        st.info(
            f"🌍 External API Time (UTC): {utc_time}"
        )

        # -----------------------------
        # Source Statistics
        # -----------------------------
        st.info(
            f"""
📊 Source Statistics

• Discord Messages Processed: {discord_count}

• Tickets Processed: {ticket_count}

• Coverage Window: Last 12 Hours
"""
        )

        # -----------------------------
        # Metrics Dashboard
        # -----------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Discord Messages",
                discord_count
            )

        with col2:
            st.metric(
                "Tickets",
                ticket_count
            )

        with col3:
            st.metric(
                "Report Status",
                "Generated"
            )

        st.divider()

        # -----------------------------
        # Report Section
        # -----------------------------
        st.subheader(
            "📄 Generated Handover Report"
        )

        st.markdown(note)

        # -----------------------------
        # Download Button
        # -----------------------------
        st.download_button(
            label="📥 Download Markdown",
            data=note,
            file_name="handover_note.md",
            mime="text/markdown"
        )

    except ValueError as e:

        st.error(
            f"❌ Validation Error: {str(e)}"
        )

    except FileNotFoundError as e:

        st.error(
            f"❌ File Error: {str(e)}"
        )

    
    except Exception as e:

        st.error(
            f"❌ Unexpected Error: {str(e)}"
        )

        st.exception(e)


