import json
import time

userlog_event_types = {
    "warns": "Warn",
    "bans": "Ban",
    "kicks": "Kick",
    "mutes": "Mute",
    "notes": "Note",
}


def get_userlog():
    with open("data/userlog.json", "r") as f:
        return json.load(f)


def set_userlog(contents):
    with open("data/userlog.json", "w") as f:
        f.write(contents)


def fill_userlog(userid, uname):
    userlogs = get_userlog()
    uid = str(userid)
    if uid not in userlogs:
        userlogs[uid] = {
            "warns": [],
            "mutes": [],
            "kicks": [],
            "bans": [],
            "notes": [],
            "watch": False,
            "name": "n/a",
        }
    if uname:
        userlogs[uid]["name"] = uname

    return userlogs, uid


def userlog(uid, issuer, reason, event_type, uname: str = ""):
    userlogs, uid = fill_userlog(uid, uname)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_data = {
        "issuer_id": issuer.id,
        "issuer_name": f"{issuer}",
        "reason": reason,
        "timestamp": timestamp,
    }
    if event_type not in userlogs[uid]:
        userlogs[uid][event_type] = []
    userlogs[uid][event_type].append(log_data)
    set_userlog(json.dumps(userlogs))
    return len(userlogs[uid][event_type])


def setwatch(uid, issuer, watch_state, uname: str = ""):
    userlogs, uid = fill_userlog(uid, uname)

    userlogs[uid]["watch"] = watch_state
    set_userlog(json.dumps(userlogs))
    return
