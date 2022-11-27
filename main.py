# Import required modules
import datetime
import discord
import pymongo
import json

# Initialise bot and database
bot = discord.Bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix="/", intents=intents)
mongoDB = pymongo.MongoClient("mongodb+srv://eillesj:Jeilles310706-@userid.27w8qi7.mongodb.net/?retryWrites=true&w=majority")
db = mongoDB["RequestedUsers"]
col = db["UserReqID"]

# Notify when bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord and is ready to use.")

# Command to request verification
@bot.slash_command(name = "verify", description = "Verify yourself to get access to the server.")
async def verify(ctx, link: discord.Option(str, "Link", required=True)): # This is the slash command
    if ctx.channel.id == 1044384110711406703: # If the channel is the verification channel

        modChannel = bot.get_channel(1044615945370488843) # Get the mod channel

        # Add the user to the database
        userInfo = {
            "userID": ctx.author.id,
            "link": link,
            "date": datetime.datetime.utcnow(),
        }
        col.insert_one(userInfo)

        await modChannel.send(f"@{ctx.author} (ID: {ctx.author.id}) has requested verification. Their profile link is {link}.") # Send the message to the mod channel

        await ctx.respond(f"Your link has been sent to the moderators to be reviewed.") # Respond to the user



        

    else:
        await ctx.send(f"This command can only be run in #verification.", ephemeral=True) # If the command is not run in the verification channel, tell the user

# Command to accept a user
@bot.slash_command(name = "accept", description = "Accept a user's verification request.")
async def verify(ctx, userid: discord.Option(str, "UserID", required=True)):
    ## Placeholder to connect to MongoDB to check if the UserID is in the database
    if ctx.channel.id == 1044615945370488843:
        x = col.find_one({}, {"userID": userid})
        if x is None:
            await ctx.respond(f"User not found. Please check the UserID and try again.")
        else:
            await ctx.respond(f"User found.")
            print(x)
            user = bot.get_user(userid)
            verifiedRole = discord.utils.get(ctx.guild.roles, name="Community Member")
            awaitingVerif = discord.utils.get(ctx.guild.roles, name="Awaiting Verification...")
            await user.add_roles(verifiedRole)
            await user.remove_roles(awaitingVerif)
            await ctx.respond(f"User has been verified.")
    else:
        await ctx.respond("This command can only be run by moderators.", ephemeral=True)

# Token
bot.run("MTA0NDM2NzM0NTg2MDIxODkxMQ.GzrbwC.DlId6Y7QiBRPsBbpjvk4eGjZnp61ZTOIJzkc_M")