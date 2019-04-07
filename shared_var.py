"""
This file is utilized to share FLAGs between play_game.py where an asyncrhonous thread is running,
enabling game_view.py to respond to FLAGs and present the User with data or decisions.
"""

JOIN_REQUEST_FLAG = False
ACTION_REQUEST_FLAG = False
GM_LEAVES_FLAG = False
MESSAGE_CONTENT = None
UPDATE_GAME_FLAG = False
ASSET_ADDED_FLAG = False
CHAT_CONTENT = []
CHAT_FLAG = False
