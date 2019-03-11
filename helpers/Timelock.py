import SqlManagment


def is_locked(channel_id : int = 0, guild_id : int = 0):
  """Returns a boolean value of True or False depends on the state of the channel lock, If it is or isn't"""
  if(channel_id == 0):
    print("Channel ID is not provided!")
    return
  if(guild_id == 0):
    print("Guild ID is not provided!")
    return
  row = SqlManagment.select(True,"lc_"+str(guild_id),"lockedChannels",str(channel_id))
  if(row[0][1] == 0): # If channel is not locked!
    return False
  elif(row[0][1] == 1): # If channel is locked!
    return True
  
def createTable(guild : discord.Guild = None):
  """Creates a database file and a table for the server, and add the channels to the db"""
  if(guild == None):
    print("Guild is not provided!")
    return
  sql_statement = '''CREATE TABLE IF NOT EXISTS `lockedChannels` (
                    `id` int(18) NOT NULL,
                    `locked` numeric(9,2),
                    PRIMARY KEY( `id` )
                  );'''
  SqlManagment.create_table("lc_"+str(guild.id),sql_statement)
  print("Created database for " + str(guild.id) + " for locked channels")
  sql_s = '''INSERT INTO lockedChannels(id,locked) VALUES(?,?)'''
  for channel in guild.channels:
    SqlManagment.add("lc_"+str(guild.id),"lockedChannels",sql_s,(guild.id,0))
  
def lockChannel(guild_id : int = 0, channel_id : int = 0,state : bool = False):
  """Locks a channel according to the state, False unlocks, True locks"""
  if(channel_id == 0):
    print("Channel ID is not provided!")
    return
  if(guild_id == 0):
    print("Guild ID is not provided!")
    return
  if(state == True):
    SqlManagment.change("lc_"+str(guild_id),"lockedChannels","locked",1,channel_id)
    print("Locked " + str(channel_id))
  elif(state == False):
    SqlManagment.change("lc_"+str(guild_id),"lockedChannels","locked",0,channel_id)
    print("Unlocked " + str(channel_id))
    
