import nextcord
from nextcord.ext import commands
import asyncio


TESTING_GUILD_ID =   # Replace with your testing guild id
REPORT_CHANNEL_ID =   # Replace with the channel ID where you want to send the reports

class ReportModal(nextcord.ui.Modal):
    report_count = 1
    def __init__(self, channel_id):
        super().__init__(
            title="Report A Player!",
            custom_id="persistent_modal:report",
            timeout=None,
        )

        self.channel_id = channel_id

        self.YUM = nextcord.ui.TextInput(
            label="What is Your In-Game Username?",
            placeholder="e.g. nintenmike3dsx.",
            required=True,
            max_length=100,
            style=nextcord.TextInputStyle.paragraph,
            custom_id="persistent_modal:yourUN",
        )
        self.add_item(self.YUM)

        self.TUM = nextcord.ui.TextInput(
            label="Reported Player In-Game Username?",
            placeholder="e.g meceka",
            required=True,
            max_length=100,
            custom_id="persistent_modal:theirUN",
        )
        self.add_item(self.TUM)

        self.WD = nextcord.ui.TextInput(
            label="What did the Player Do?",
            placeholder="e.g. Crashing/Blocking.",
            style=nextcord.TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:Do",
        )
        self.add_item(self.WD)

        self.room = nextcord.ui.TextInput(
            label="Region / Room Name",
            placeholder="e.g. USA East / tlsevent.",
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            max_length=100,
            custom_id="persistent_modal:roomServ",
        )
        self.add_item(self.room)

        self.report_number = ReportModal.report_count
        ReportModal.report_count += 1

    async def callback(self, interaction: nextcord.Interaction):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel is None:
            return await interaction.response.send_message("Could not find the report channel.")

        embed = nextcord.Embed(title=f"Player Report #{self.report_number}\n\n", color=0xFF0000)
        embed.add_field(name="By Discord User:\n", value=interaction.user.display_name, inline=False)
        embed.add_field(name="Region / Room Name:\n", value=self.room.value, inline=False)
        embed.add_field(name="Reported Player:\n", value=self.TUM.value, inline=False)
        embed.add_field(name="Report Sent By:\n", value=self.YUM.value, inline=False)
        embed.add_field(name="What the Player Did:\n", value=self.WD.value, inline=False)

        await channel.send(embed=embed)
        await interaction.response.send_message("Thank you for reporting! Please send any images/videos you have to https://discord.com/channels/1078749205495042198/1228136524084674642. You may also mention any online Community Moderator for assistance!", ephemeral=True)


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Report A Player!", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(ReportModal(REPORT_CHANNEL_ID))



bot = commands.Bot()

@bot.slash_command(name="report",
    description="Generates Player Reports!")
async def report(interaction):
    view = Confirm()
    await interaction.send("# Player Reporting!\n\n**Here you can report players that you encounter in game. Before making a report here, please report the player in-game using the Player List!**\n\n**What To Look For In Bad Players!**\n\nPlayers that are blocking roads, purposefully crashing, or have a inappropriate username are valid reasons to be reported. You can let us know any issues you encounter in multiplayer!\n\n**What Moderation Features We Offer!**\n\nWe give you moderation tools to help! Located in the player list you will find 3 options: Disable Collisions, Block, and Report. Disabling collisions will disable collisions with the selected player so that you can pass through them without damaging your truck and cargo. Additionally that player will not be able to hit you. Blocking will hide that player from the room entirely. Their truck, trailer, and name will completely disappear. Reporting will send a report to our moderation team!\n\n**Press the Report! Button Below to Get Started, Please Fill Out the Form as Much as You Can!**\n\n*Your Truck & Logistics Simulator Moderation Team\nMessage <@554832528238968883> For Help!*", view=view)

@bot.slash_command(
        name="about",
        description="Information About Bot!.",
        guild_ids=[TESTING_GUILD_ID],
)
async def about(interaction: nextcord.Interaction):
        about_message = (
            "## AutoAdmin here! I am a player report bot for Truck & Logistics Simulator!\n\n\n"
            "Is a player causing issues in your game?\n\n"
            "**Please go to https://discord.com/channels/1078749205495042198/1228410618151829585 for more instructions!**\n\n"
            "*Created and maintained by <@554832528238968883> DM for help!*\n\n"
        )
        await interaction.response.send_message(about_message)

bot.run('placetoken')