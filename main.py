import discord
from discord.ext import commands
import os
import json
import datetime

# ---------------------------------------------------------------------------------------------------------------------------
# Inicializamos el bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Cargamos la configuracion desde el archivo JSON

config_file_path = "C:\\Users\\flami\\Downloads\\White Bot\\config.json"
if os.path.exists(config_file_path):
    with open(config_file_path, "r") as file:
        config_data = json.load(file)

else:
    config_data = {} # En caso de que no se encuentre el archivo, iniciamos config_data como un archivo vacio

# ---------------------------------------------------------------------------------------------------------------------------
# Comando /config
@bot.tree.command(
    name="config",
    description="Configura qué roles pueden usar el bot y cuáles no."
)
async def config(interaction: discord.Integration, role: discord.Role, allow: bool):
    global config_data

    # Actualizamos la configuración
    config_data[str(role.id)] = allow

    # Guardamos la configuración en el archivo JSON
    with open(config_file_path, 'w') as file:
        json.dump(config_data, file)

    await interaction.response.send_message(f"La configuración para el rol '{role.name}' se ha actualizado. Puede {'usar' if allow else 'no usar'} el bot.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

# ---------------------------------------------------------------------------------------------------------------------------
# Comando /say, el bot reenvia un mensaje o una imagen.

@bot.tree.command(
    name="say",
    description="Haz que el bot diga algo",
)
async def say(interaction: discord.Interaction, message: str = None, media: discord.Attachment = None):
    global config_data

    server = bot.get_guild(interaction.guild_id)

    user = server.get_member(interaction.user.id)

    # Verificar si el rol del usuario tiene permiso
    if not user:
        await interaction.response.send_message(content="No se pudo encontrar el usuario.", ephemeral=True)
        return

    role_id = None
    if user.top_role:
        role_id = user.top_role.id

    if role_id and str(role_id) in config_data and config_data[str(role_id)]:
        await interaction.response.send_message(content="Su mensaje ha sido enviado.", ephemeral=True)

        # Verifica si se proporcionó una imagen
        if media:
            await interaction.channel.send(content=message, file=await media.to_file())
        else:
            await interaction.channel.send(content=message)
    else:
        await interaction.response.send_message(content="No tienes permiso para usar este comando.", ephemeral=True)

# ---------------------------------------------------------------------------------------------------------------------------
# Este comando toma un tiempo y luego le suma 2hs y 23m

@bot.tree.command(
    name="timers",
    description="Suma 2 horas y 23 minutos al tiempo proporcionado y devuelve el resultado en formato 24 horas."
)
async def timers(interaction: discord.Interaction, time_hub: str, location: discord.Attachment):
    try:
        # Convertir el tiempo proporcionado a un objeto datetime
        input_time = datetime.datetime.strptime(time_hub, '%H:%M')

        # Sumar 2 horas y 23 minutos
        new_time = input_time + datetime.timedelta(hours=2, minutes=23)

        # Convertir el resultado a una cadena en formato de 24 horas
        result_time = new_time.strftime('%H:%M')

        # Enviar el resultado al canal específico
        channel = bot.get_channel(1168739630921810012)  # Reemplaza con tu ID de canal
        await channel.send(content=f"Se podra volver a robar: {result_time} **Hora HUB**")

        # Verificar si se proporcionó una imagen
        if location:
            await channel.send(content="En esta ubicación:", file=await location.to_file())
            
        # Enviar un mensaje efímero para indicar que se ha procesado el comando
        await interaction.response.send_message(content="El resultado se ha enviado al canal <#1168739630921810012>.", ephemeral=True)

    except ValueError:
        await interaction.response.send_message(content="El formato del tiempo no es válido. Por favor, usa HH:MM (24 horas).", ephemeral=True)

# ---------------------------------------------------------------------------------------------------------------------------
# Comando /load_say te permite enviar un mensaje desde un txt.

@bot.tree.command(
    name="load_say",
    description="Carga y envía un mensaje desde un archivo de texto."
)
async def load_say(interaction: discord.Interaction, file_path: str):
    global config_data

    # Obtener el servidor desde la interacción
    server = bot.get_guild(interaction.guild_id)

    # Obtener el miembro que interactuó con el comando
    user = server.get_member(interaction.user.id)

    # Verificar si el rol del usuario tiene permiso
    if not user:
        await interaction.response.send_message(content="No se pudo encontrar el usuario.", ephemeral=True)
        return

    role_id = None
    if user.top_role:
        role_id = user.top_role.id

    if role_id and str(role_id) in config_data and config_data[str(role_id)]:
        try:
            # Combinamos la carpeta y el nombre del archivo para obtener la ruta completa
            full_path = os.path.join("C:\\Users\\flami\\Downloads\\White Bot\\info", file_path)

            with open(full_path, 'r', encoding='utf-8') as file:  # Especificamos utf-8 como la codificación
                message = file.read()
                await interaction.channel.send(content=message)
        except FileNotFoundError:
            await interaction.response.send_message(content="El archivo no fue encontrado.", ephemeral=True)
    else:
        await interaction.response.send_message(content="No tienes permiso para usar este comando.", ephemeral=True)


# ---------------------------------------------------------------------------------------------------------------------------
# Administrar roles

@bot.tree.command(
    name="mod-roles",
    description="Añade o quita un rol a un usuario por su mención o ID."
)
async def mod_roles(interaction: discord.Interaction, user: discord.Member, action: str, role: discord.Role):
    try:
        server = bot.get_guild(interaction.guild_id)
        user = server.get_member(interaction.user.id)

        if not user:
            await interaction.response.send_message(content="No se pudo encontrar el usuario.", ephemeral=True)
            return

        role_id = None
        if user.top_role:
            role_id = user.top_role.id

        if role_id and str(role_id) in config_data and config_data[str(role_id)]:
            # Tu lógica para añadir o quitar roles aquí
            await interaction.response.send_message(content="Rol modificado con éxito.", ephemeral=True)
        else:
            await interaction.response.send_message(content="No tienes permiso para usar este comando.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(content=f"Ocurrió un error: {e}", ephemeral=True)


# ---------------------------------------------------------------------------------------------------------------------------
# Se utiliza para hacer ping y sincronizar el bot.

@bot.command()
async def ping(ctx):
    await bot.tree.sync()
    await ctx.send("pong")

bot.run('MTE2ODk0NjkyMTU1NDA1OTI2NQ.GFByz8.7kXPAARZl0dqVmjLAURjcOpMX-Xx1i2zCOL1eA')
