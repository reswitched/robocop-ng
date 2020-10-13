from discord.ext.commands import Cog
import re
import config
import secrets
import asyncio


class YubicoOTP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.otp_re = re.compile("((cc|vv)[cbdefghijklnrtuv]{42})$")
        self.api_servers = [
            "https://api.yubico.com",
            "https://api2.yubico.com",
            "https://api3.yubico.com",
            "https://api4.yubico.com",
            "https://api5.yubico.com",
        ]
        self.reuse_responses = ["BAD_OTP", "REPLAYED_OTP"]
        self.bad_responses = [
            "MISSING_PARAMETER",
            "NO_SUCH_CLIENT",
            "OPERATION_NOT_ALLOWED",
        ]
        self.modhex_to_hex_conversion_map = {
            "c": "0",
            "b": "1",
            "d": "2",
            "e": "3",
            "f": "4",
            "g": "5",
            "h": "6",
            "i": "7",
            "j": "8",
            "k": "9",
            "l": "a",
            "n": "b",
            "r": "c",
            "t": "d",
            "u": "e",
            "v": "f",
        }

    def get_serial(self, otp):
        """Get OTP from serial, based on code by linuxgemini"""
        if otp[:2] != "cc":
            return False

        hexconv = []

        for modhexletter in otp[0:12]:
            hexconv.append(self.modhex_to_hex_conversion_map[modhexletter])

        return int("".join(hexconv), 16)

    async def validate_yubico_otp(self, otp):
        nonce = secrets.token_hex(15)  # Random number in the valid range
        for api_server in self.api_servers:
            url = f"{api_server}/wsapi/2.0/verify?id={config.yubico_otp_client_id}&otp={otp}&nonce={nonce}"
            try:
                resp = await self.bot.aiosession.get(url)
                assert resp.status == 200
            except Exception as ex:
                self.bot.log.warning(
                    f"Got {repr(ex)} on {api_server} with otp {otp}."
                )
                continue
            resptext = await resp.text()

            # Turn the fields to a python dict for easier parsing
            datafields = resptext.strip().split("\r\n")
            datafields = {line.split("=")[0]: line.split("=")[1] for line in datafields}

            datafields["nonce"] != nonce
            # If we got a success, then return True
            if datafields["status"] == "OK":
                return True
            elif datafields["status"] in self.reuse_responses:
                return False

            # If status isn't an expected one, log it
            self.bot.log.warning(
                f"Got {repr(datafields)} on {api_server} with otp {otp} and nonce {nonce}"
            )

            # If we fucked up in a way we can't recover from, just return None
            if datafields["status"] in self.bad_responses:
                return None

        # Return None if we fail to get responses from any server
        return None

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        otps = self.otp_re.findall(message.content.strip())
        for otp_entry in otps:
            otp = otp_entry[0]
            # Validate OTP
            validation_result = await self.validate_yubico_otp(otp)
            if validation_result is not True:
                return

            # Derive serial and a string to use it
            serial = self.get_serial(otp)
            serial_str = f" (serial: `{serial}`)" if serial else ""

            # If the message content is _just_ the OTP code, delete it toos
            if message.content.strip() == otp:
                await message.delete()

            # If OTP is valid, tell user that it was revoked
            msg = await message.channel.send(
                f"{message.author.mention}: Ate Yubico OTP `{otp}`{serial_str}"
                ". This message will self destruct in 5 seconds."
            )
            # and delete message after 5s to help SNR
            await asyncio.sleep(5)
            await msg.delete()


def setup(bot):
    bot.add_cog(YubicoOTP(bot))
