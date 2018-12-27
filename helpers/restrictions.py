import json


def add_restriction(self, member, rst):
    # from kurisu source, credits go to ihaveamac
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
    if str(member.id) not in rsts:
        rsts[str(member.id)] = []
    if rst not in rsts[str(member.id)]:
        rsts[str(member.id)].append(rst)
    with open("data/restrictions.json", "w") as f:
        json.dump(rsts, f)


def remove_restriction(self, member, rst):
    # from kurisu source, credits go to ihaveamac
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
    if str(member.id) not in rsts:
        rsts[str(member.id)] = []
    if rst in rsts[str(member.id)]:
        rsts[str(member.id)].remove(rst)
    with open("data/restrictions.json", "w") as f:
        json.dump(rsts, f)
