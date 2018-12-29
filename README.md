# Robocop-ng

Next-gen rewrite of Kurisu/Robocop bot used on ReSwitched bot with discord.py rewrite, designed to be relatively clean, consistent and un-bloated.

Code is based on https://gitlab.com/ao/dpybotbase and https://github.com/916253/Kurisu-Reswitched.


---

## How to run

- Copy `config.py.template` to `config.py`, configure all necessary parts to your server.
- Install python3.6+.
- Install python dependencies (`pip3 install -Ur requirements.txt`, you might need to put `sudo -H` before that)
- If you're moving from Kurisu or Robocop: Follow `Tips for people moving from Kurisu/Robocop` below.
- Run `Robocop.py` (`python3 Robocop.py`)

To keep the bot running, you might want to use pm2 or a systemd service.

---

## Tips for people moving from Kurisu/Robocop

If you're moving from Kurisu/Robocop, and want to preserve your data, you'll want to do the following steps:

- Copy your `data` folder over.
- Rename your `data/warnsv2.json` file to `data/userlog.json`.
- Edit `data/restrictions.json` and replace role names (`"Muted"` etc) with role IDs (`526500080879140874` etc). Make sure to have it as int, not as str (don't wrap role id with `"` or `'`).

---

## TODO

All Robocop features are now supported.

<details>
<summary>List of added Kurisu/Robocop features</summary>
<p>

- [x] .py configs
- [x] membercount command
- [x] Meme commands and pegaswitch (honestly the easiest part)
- [x] source command
- [x] robocop command
- [x] Verification: Actual verification system
- [x] Verification: Reset command
- [x] Logging: joins
- [x] Logging: leaves
- [x] Logging: role changes
- [x] Logging: bans
- [x] Logging: kicks
- [x] Moderation: speak
- [x] Moderation: ban
- [x] Moderation: silentban
- [x] Moderation: kick
- [x] Moderation: userinfo
- [x] Moderation: approve-revoke (community)
- [x] Moderation: addhacker-removehacker (hacker)
- [x] Moderation: probate-unprobate (participant)
- [x] Moderation: lock-softlock-unlock (channel lockdown)
- [x] Moderation: mute-unmute
- [x] Moderation: playing
- [x] Moderation: botnickname
- [x] Moderation: nickname
- [x] Moderation: clear/purge
- [x] Moderation: restrictions (people who leave with muted role will get muted role on join)
- [x] Warns: warn
- [x] Warns: listwarns-listwarnsid
- [x] Warns: clearwarns-clearwarnsid
- [x] Warns: delwarnid-delwarn
- [x] .serr and .err (thanks tomger!)

</p>
</details>

---

Main goal of this project is to get Robocop functionality done, secondary goal is adding new features. The following entries are secondary, less "urgent" goals:

- [x] Better security, better checks and better guild whitelisting
- [ ] New verification feature: Using log module from akbbot for logging attempts and removing old attempts
- [ ] New moderation feature: watch-unwatch (using log module from akbbot)
- [ ] New feature: Modmail
- [ ] New feature: Submiterr (relies on modmail)
- [ ] New feature: Highlights (problematic words automatically get posted to modmail channel, relies on modmail)
- [ ] Feature creep: Shortlink completion (gl/ao/etc)
- [ ] Feature creep: Pleroma embedding
- [x] A system for running jobs in background with an interval (will be called robocronp)
- [x] Commands to list said jobs and remove them
- [x] New moderation feature: timemute (mute with time, relies on robocronp)
- [x] New moderation feature: timeban (ban with expiry, relies on robocronp)
- [ ] New moderation feature: timelock (channel lockdown with time, relies on robocronp)
- [x] Improvements to lockdown to ensure that staff can talk
- [x] New moderation feature: Display of mutes, bans and kicks on listwarns (.userlog now)
- [x] New moderation feature: User notes
- [x] New moderation feature: Reaction removing features (thanks misson20000!)
- [x] New moderation feature: User nickname change
- [x] New self-moderation feature: .mywarns
- [x] Remove sh, remove risky stuff from eval

<details>
<summary>TODO for robocronp</summary>
<p>

[ ] Reduce code repetition on mod_timed.py
[ ] Allow non-hour values on timed bans

the following require me to rethink some of the lockdown code, which I don't feel like

[ ] lockdown in helper
[ ] timelock command
[ ] working cronjob for unlock

</p>
</details>

---

## Thanks to

- ReSwitched community, for being amazing
- ihaveamac/ihaveahax and f916253 for the original kurisu/robocop
- tomGER for working hard on rewriting the .err/.serr commands, those were a nightmare
- misson20000 for adding in reaction removal feature and putting up with my many BS requests on PR reviews

