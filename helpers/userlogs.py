import json
import time

userlog_event_types = {"warns": "Warn",
                       "bans": "Ban",
                       "kicks": "Kick",
                       "mutes": "Mute",
                       "notes": "Note"}


def get_userlog():
    with open("data/userlog.json", "r") as f:
        return json.load(f)


def set_userlog(contents):
    with open("data/userlog.json", "w") as f:
        f.write(contents)


def userlog(uid, issuer, reason, event_type, uname: str = ""):
        with open("data/userlog.json", "r") as f:
            userlogs = json.load(f)
        uid = str(uid)
        if uid not in userlogs:
            userlogs[uid] = {"warns": [],
                             "mutes": [],
                             "kicks": [],
                             "bans": [],
                             "notes": [],
                             "watch": False,
                             "name": "n/a"}
        if uname:
            userlogs[uid]["name"] = uname
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_data = {"issuer_id": issuer.id,
                    "issuer_name": f"{issuer}",
                    "reason": reason,
                    "timestamp": timestamp}
        if event_type not in userlogs[uid]:
            userlogs[uid][event_type] = []
        userlogs[uid][event_type].append(log_data)
        with open("data/userlog.json", "w") as f:
            json.dump(userlogs, f)
        return len(userlogs[uid][event_type])
