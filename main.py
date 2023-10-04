# Import required modules
import datetime
import discord
import pymongo

# Initialise bot and database
bot = discord.Bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix="/", intents=intents)
mongoDB = pymongo.MongoClient(
    "mongodb+srv://eillesj:QFGfAJhKTQEcZ20W@spcverif.hgmrqcg.mongodb.net/?retryWrites=true&w=majority")
db = mongoDB["RequestedUsers"]
col = db["UserReqID"]

# Notify when bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord and is ready to use.")


# Command to request verification
@bot.slash_command(name="verify", description="Verify yourself to get access to the server.")
async def verify(ctx, link: discord.Option(str, "Link", required=True)):  # This is the slash command
    # Check if the command is used in the correct channel
    if ctx.channel.id == 1044384110711406703:

        # Add the user to the database
        dbinfo = {"_id": ctx.author.id,
                  "link": link,
                  "verified": False,
                  "deny": False,
                  "date": datetime.datetime.utcnow()
                  }
        col.insert_one(dbinfo)

        # Send a message to the user
        await ctx.respond(f"Thank you for requesting verification, {ctx.author.mention}. "
                          f"You will be notified when you have been verified.")

        # Send a message to the mod channel
        await bot.get_channel(1044615945370488843).send(f"@SPC Staff | {ctx.author.mention} (ID: {ctx.author.id} has "
                                                        f"requested verification. Please verify them.")

    else:
        await ctx.send(f"This command can only be run in #verification.",
                       ephemeral=True)  # If the command is not run in the verification channel, tell the user


# Command to accept a user
@bot.slash_command(name="accept", description="Accept a user's verification request.")
async def verify(ctx, userid: discord.Option(str, "UserID", required=True)):  # This is the slash command
    # Check if the command is used in the correct channel (mod channel)
    if ctx.channel.id == 1044615945370488843:

        # Check if the user is a moderator
        if ctx.author.guild_permissions.manage_roles:

            # Check if the user is already verified
            userid = int(userid)
            if col.find_one({"_id": userid})["verified"] == True:
                await ctx.respond(f"{ctx.author.mention}, this user is already verified.")
                return

            elif col.find_one({"_id": userid})["verified"] == False:
                # Update the database

                member = ctx.message.server.get_member(userid)

                addrole = discord.utils.get(ctx.guild.roles, name="Community Member", id=1045091981283573811)
                removerole = discord.utils.get(ctx.guild.roles, name="Awaiting Verification...", id=1045091897456214076)

                # Add the verified role to the user
                await member.add_roles(addrole)

                # Remove the unverified role from the user
                await member.remove_roles(removerole)

                col.update_one({"_id": userid}, {"$set": {"verified": True}})

                # Send a message to the mod channel
                await bot.get_channel(1044615945370488843).send(f"{userid} has been verified.")

                # Send the user a DM to notify them
                await bot.get_user(userid).send(
                    f"Your verification request for the Small Producer Community has been accepted! You can now "
                    f"access the server.")
            else:
                await ctx.respond(f"{ctx.author.mention}, this user could not be found in the database.")
                return
        else:
            await ctx.send(f"You do not have the required permissions to use this command. How are you even in "
                           f"here?", ephemeral=True)
    else:
        await ctx.send(f"This command can not be run in this channel.",
                       ephemeral=True)


@bot.slash_command(name="deny", description="Deny a user's verification request.")
async def verify(ctx, userid: discord.Option(str, "UserID", required=True)):  # This is the slash command
    # Check if the command is used in the correct channel (mod channel)
    if ctx.channel.id == 1044615945370488843:

        # Check if the user is a moderator
        if ctx.author.guild_permissions.manage_roles:

            # Check if the user is already verified
            userid = int(userid)
            if col.find_one({"_id": userid})["verified"] == True and col.find_one({"_id": userid})["deny"] == False:
                await ctx.respond(f"{ctx.author.mention}, this user is already verified.")
                return

            elif col.find_one({"_id": userid})["verified"] == False and col.find_one({"_id": userid})["deny"] == False:

                # Update the database
                col.update_one({"_id": userid}, {"$set": {"verified": False}})

                # Send a message to the mod channel
                await bot.get_channel(1044615945370488843).send(f"{userid} has been denied verification.")

                # Send the user a DM to notify them
                await bot.get_user(userid).send(
                    f"Your verification request for the Small Producer Community has been denied. "
                    f"Please try again.")


            else:
                await ctx.respond(f"{ctx.author.mention}, this user could not be found in the database.")
                return
        else:
            await ctx.send(f"You do not have the required permissions to use this command. How are you even in "
                           f"here?", ephemeral=True)


# Token
bot.run("redacted")
