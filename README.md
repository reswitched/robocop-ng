# Robocop-ng

Next-gen rewrite of Kurisu/Robocop bot used on ReSwitched bot with discord.py rewrite, designed to be relatively clean, consistent and un-bloated.

Code is based on https://gitlab.com/ao/dpybotbase and https://github.com/916253/Kurisu-Reswitched.


---

## How to run

- Copy `config.py.template` to `config.py`, configure all necessary parts to your server.
- (obviously) Add the bot to your guild. Many resources about this online.
- If you haven't already done this already, **move the bot's role above the roles it'll need to manage, or else it won't function properly**, this is especially important for verification as it doesn't work otherwise.
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

The main goal of this project, to get Robocop functionality done, is complete.

Secondary goal is adding new features:

- [ ] Purge: On purge, send logs in form of txt file to server logs
- [ ] New feature: Modmail
- [ ] New feature: Submiterr (relies on modmail)
- [ ] Feature creep: Shortlink completion (gl/ao/etc)
- [ ] New moderation feature: timelock (channel lockdown with time, relies on robocronp)

<details>
<summary>Completed features</summary>
<p>

- [x] Better security, better checks and better guild whitelisting
- [x] Feature creep: Reminds
- [x] A system for running jobs in background with an interval (will be called robocronp)
- [x] Commands to list said jobs and remove them
- [x] New moderation feature: timemute (mute with time, relies on robocronp)
- [x] New moderation feature: timeban (ban with expiry, relies on robocronp)
- [x] Improvements to lockdown to ensure that staff can talk
- [x] New moderation feature: Display of mutes, bans and kicks on listwarns (.userlog now)
- [x] New moderation feature: User notes
- [x] New moderation feature: Reaction removing features (thanks misson20000!)
- [x] New moderation feature: User nickname change
- [x] New moderation feature: watch-unwatch
- [x] New moderation feature: tracking suspicious keywords
- [x] New moderation feature: tracking invites posted
- [x] New self-moderation feature: .mywarns
- [x] New feature: Highlights (problematic words automatically get posted to modmail channel, relies on modmail)

</p>
</details>

<details>
<summary>TODO for robocronp</summary>
<p>

- [ ] Reduce code repetition on mod_timed.py
- [x] Allow non-hour values on timed bans

the following require me to rethink some of the lockdown code, which I don't feel like

- [ ] lockdown in helper
- [ ] timelock command
- [ ] working cronjob for unlock

</p>
</details>

---

## Credits

Robocop-NG is currently developed and maintained by @aveao and @tumGER. The official bot is hosted by @yuukieve.

I (ave) would like to thank the following, in no particular order:

- ReSwitched community, for being amazing
- ihaveamac/ihaveahax and f916253 for the original kurisu/robocop
- misson20000 for adding in reaction removal feature and putting up with my many BS requests on PR reviews
- Everyone who contributed to robocop-ng in any way (reporting a bug, sending a PR, forking and hosting their own at their own guild, etc).

