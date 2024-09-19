import discord
import logging
import os
from discord.ext import commands
from datetime import datetime

# Configurer le logging pour enregistrer dans un fichier
logging.basicConfig(filename='bot_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Récupérer le token du bot et le nom du salon textuel depuis les variables d'environnement
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_NAME = os.getenv('LOG_CHANNEL_NAME', 'log-channel')  # Par défaut 'log-channel' si la variable n'est pas définie

# Initialiser le bot avec les intents appropriés
intents = discord.Intents.default()
intents.members = True  # Pour suivre les membres
intents.voice_states = True  # Pour suivre les déplacements vocaux
intents.message = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Fonction pour envoyer et enregistrer les événements
async def log_event(event_type, member, before=None, after=None):
    log_channel = discord.utils.get(member.guild.text_channels, name=LOG_CHANNEL_NAME)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Construire le message du log
    if event_type == "join":
        message = f"🟢 {current_time} - {member} a rejoint le serveur."
    elif event_type == "leave":
        message = f"🔴 {current_time} - {member} a quitté le serveur."
    elif event_type == "move":
        message = (f"🔄 {current_time} - {member} s'est déplacé de "
                   f"{before.channel.name if before else 'inconnu'} à {after.channel.name}.")
    elif event_type == "join_voice":
        message = f"🟢 {current_time} - {member} a rejoint le salon vocal {after.channel.name}."
    elif event_type == "leave_voice":
        message = f"🔴 {current_time} - {member} a quitté le salon vocal {before.channel.name}."

    # Envoyer le message dans le salon texte et enregistrer dans un fichier
    if log_channel:
        await log_channel.send(message)
    logging.info(message)

# Traquer l'entrée des membres dans le serveur
@bot.event
async def on_member_join(member):
    await log_event("join", member)

# Traquer la sortie des membres du serveur
@bot.event
async def on_member_remove(member):
    await log_event("leave", member)

# Traquer les mouvements dans les salons vocaux
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        await log_event("join_voice", member, after=after)
    elif before.channel is not None and after.channel is None:
        await log_event("leave_voice", member, before=before)
    elif before.channel != after.channel:
        await log_event("move", member, before=before, after=after)

# Lancer le bot avec le token récupéré depuis la variable d'environnement
bot.run(DISCORD_TOKEN)
