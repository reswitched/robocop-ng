import json


def get_restrictions():
    with open("data/restrictions.json", "r") as f:
        return json.load(f)


def set_restrictions(contents):
    with open("data/restrictions.json", "w") as f:
        f.write(contents)


def get_user_restrictions(uid):
    uid = str(uid)
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
        if uid in rsts:
            return rsts[uid]
        return []


def add_restriction(uid, rst):
    # mostly from kurisu source, credits go to ihaveamac
    uid = str(uid)
    rsts = get_restrictions()
    if uid not in rsts:
        rsts[uid] = []
    if rst not in rsts[uid]:
        rsts[uid].append(rst)
    set_restrictions(json.dumps(rsts))


def remove_restriction(uid, rst):
    # mostly from kurisu source, credits go to ihaveamac
    uid = str(uid)
    rsts = get_restrictions()
    if uid not in rsts:
        rsts[uid] = []
    if rst in rsts[uid]:
        rsts[uid].remove(rst)
    set_restrictions(json.dumps(rsts))
