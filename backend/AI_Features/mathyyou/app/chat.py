chat_sessions = {}


def create_chat_session(model):
    chat_session = model.start_chat(history=[])
    chat_id = id(chat_session)
    chat_sessions[chat_id] = {"session": chat_session, "history": []}
    return chat_id


def get_chat_session(chat_id):
    return chat_sessions.get(chat_id)
