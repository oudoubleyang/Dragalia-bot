import json
import base64
from botInfo import self_id
from botDB import groups, lang_code
# DO NOT IMPORT BOTSESSION


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def write_file(content, filename, encrypt=False):
    if encrypt:
        with open(filename, 'wb') as f:
            f.write(base64.b64encode(content.encode('utf-8')))
        return True
    else:
        with open(filename, 'w') as f:
            f.write(content)
        return True


def query_token(token_id=self_id):
    return read_file(f'token_{token_id}', True)


def session_update(session, original):
    changed = False
    session_headers = session.headers
    session_cookies = session.cookies.get_dict()
    for item in original['headers']:
        if original['headers'][item] != session_headers[item]:
            original['headers'][item] = session_headers[item]
            changed = True
    for item in original['cookies']:
        if original['cookies'][item] != session_cookies[item]:
            original['cookies'][item] = session_cookies[item]
            changed = True
    if changed:
        write_file(json.dumps(original), 'token_nga', True)


def detect_lang(message):
    lang = None
    chat_id = message.chat_id
    user_lang = message.from_user.language_code
    if user_lang and 'zh' in user_lang.lower():
        for i in lang_code:
            for j in lang_code[i]:
                if j in user_lang.lower():
                    lang = i
                    break
    if not lang:
        if chat_id in groups:
            lang = groups[chat_id]['lang']
        else:
            lang = 'chs'
    return lang
