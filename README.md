# robocop-ng

Next-gen rewrite of Kurisu/Robocop bot used on ReSwitched bot with discord.py rewrite. Very lightly maintained (as of ~2025).

Code is based on https://gitlab.com/a/dpybotbase and https://github.com/916253/Kurisu-Reswitched.

---

## How to run

- Copy `robocop_ng/config_template.py` to `robocop_ng/config.py`, configure all necessary parts to your server.
- Enable all privileged intents ([guide here](https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents#privileged-intents)) for the bot. You don't need to give Discord your passport as Robocop-NG is not designed to run in >1 guild at once, let alone >100.
- (obviously) Add the bot to your guild. There are many resources about this online.
- If you haven't already done this already, **move the bot's role above the roles it'll need to manage, or else it won't function properly**, this is especially important for verification as it doesn't work otherwise.
- If you're moving from Kurisu or Robocop: Follow `Tips for people moving from Kurisu/Robocop` below.

### Running with docker

- `docker build . -t robocopng`
- Assuming your robocop-ng repo is on `~/docker/`: `docker run --restart=unless-stopped -v ~/docker/robocop-ng:/usr/src/app --name robocop_ng robocopng:latest`

For updates I just `git pull; docker rm -f robocop_ng` then run the two commands above again.

### Running manually

- Install python3.9+ (tested up to 3.13).
- Install [uv](https://github.com/astral-sh/uv).
- Run `uv run python3 -m robocop_ng.__init__` in the same directory as your config files.

To keep the bot running, you might want to use pm2 or a systemd service.

---

## Tips for people moving from Kurisu/Robocop

If you're moving from Kurisu/Robocop, and want to preserve your data, you'll want to do the following steps:

- Copy your `data` folder over into the `robocop_ng` folder.
- Rename your `data/warnsv2.json` file to `data/userlog.json`.
- Edit `data/restrictions.json` and replace role names (`"Muted"` etc) with role IDs (`526500080879140874` etc). Make sure to have it as int, not as str (don't wrap role id with `"` or `'`).

---

## How to migrate from discord.py v1 to v2

As of 18.08.2022 this repo is based on discord.py v2.

Only changes needed are updating your cogs and ensuring that all privileged intents are enabled for your bot.

You can find the privileged intents guide here: https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents#privileged-intents

You can see the migration instructions for your cogs here: https://discordpy.readthedocs.io/en/latest/migrating.html

---

## Contributing

Contributions are welcome. If you're unsure if your PR would be merged or not, either open an issue, ask on ReSwitched off-topic pinging ave or DM ave.

You're expected to use [black](https://github.com/psf/black) for code formatting before sending a PR. Simply install it with pip (`pip3 install black`), and run it with `black .`.

---

## Credits

Robocop-NG was initially developed by @aveao and @tumGER. It is currently maintained by @aveao. Similarly, the official robocop-ng on reswitched discord guild is hosted by @aveao too.

I (ave) would like to thank the following, in no particular order:

- ReSwitched community, for being amazing
- ihaveamac/ihaveahax and f916253 for the original kurisu/robocop
- misson20000 for adding in reaction removal feature and putting up with my many BS requests on PR reviews
- linuxgemini for helping out with Yubico OTP revocation code (which is based on their work)
- Everyone who contributed to robocop-ng in any way (reporting a bug, sending a PR, forking and hosting their own at their own guild, etc).

