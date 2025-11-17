import os

# MAIN AUTH
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# BOT TOKENS
BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1")   # BOT 1 → KillMe + Filter
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2")   # BOT 2 → Reply Bot Only


# FOR BOT 1 (Kill Me Bot Channels)
def get_list(env):
    return [int(x.strip()) for x in os.getenv(env, "").split(",") if x.strip()]

KILLME_CHANNELS = get_list("KILLME_CHANNELS")

# FOR BOT 2 (Reply Bot Groups)
REPLYBOT_GROUP = get_list("REPLYBOT_GROUP")
GROUP_EXCLUDED_IDS = get_list("GROUP_EXCLUDED_IDS")
