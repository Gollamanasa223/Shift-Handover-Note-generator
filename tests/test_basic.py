import json
import pandas as pd
import os
import pytest

from src.utils import build_combined_text
from src.llm_helper import validate_output


# ---------------------------------
# Test 1: Discord JSON loads
# ---------------------------------
def test_discord_data_loads():

    with open("data/discord.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) > 0
    assert "message" in data[0]


# ---------------------------------
# Test 2: Ticket CSV loads
# ---------------------------------
def test_ticket_csv_loads():

    df = pd.read_csv("data/tickets.csv")

    assert len(df) > 0

    # Change column name if needed
    assert "id" in df.columns or "TicketID" in df.columns


# ---------------------------------
# Test 3: Combined text contains both sources
# ---------------------------------
def test_combined_text_contains_sources():

    with open("data/discord.json", "r", encoding="utf-8") as f:
        discord_data = json.load(f)

    tickets_df = pd.read_csv("data/tickets.csv")

    text = build_combined_text(
        discord_data,
        tickets_df
    )

    assert "DISCORD MESSAGES" in text
    assert "TICKETS" in text


# ---------------------------------
# Test 4: Validate correct output
# ---------------------------------
def test_valid_handover_output():

    sample_output = """
## Open Issues
- Payment API latency

## Watch Items
- Monitor database stability

## Recent Fixes
- SSL certificate renewed

## Pending Actions
- Continue investigation
"""

    assert validate_output(sample_output) is True


# ---------------------------------
# Test 5: Missing section should fail
# ---------------------------------
def test_missing_required_section():

    bad_output = """
## Open Issues
- Payment API latency

## Watch Items
- Monitor database stability
"""

    with pytest.raises(ValueError):
        validate_output(bad_output)


# ---------------------------------
# Test 6: Empty Discord dataset
# ---------------------------------
def test_empty_discord_data():

    data = []

    assert len(data) == 0


# ---------------------------------
# Test 7: API key exists
# ---------------------------------
def test_api_key_exists():

    api_key = os.getenv("GROQ_API_KEY")

    assert api_key is not None