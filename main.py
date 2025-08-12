import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))  # ID เซิร์ฟเวอร์ของคุณ
CHANNEL_NAME_PREFIX = "In Voice: "    # ข้อความนำหน้า

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

VOICE_TRACKER_CHANNEL_ID = None  # เก็บ ID ของช่องที่แสดงจำนวนคนใน voice


@client.event
async def on_ready():
    global VOICE_TRACKER_CHANNEL_ID
    print(f'Logged in as {client.user}')

    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("ไม่พบ Guild (ตรวจสอบ GUILD_ID)")
        return

    # ค้นหาช่อง voice ที่ชื่อขึ้นต้นด้วย CHANNEL_NAME_PREFIX
    for channel in guild.voice_channels:
        if channel.name.startswith(CHANNEL_NAME_PREFIX):
            VOICE_TRACKER_CHANNEL_ID = channel.id
            break

    # ถ้ายังไม่มี ให้สร้างใหม่
    if VOICE_TRACKER_CHANNEL_ID is None:
        created_channel = await guild.create_voice_channel(CHANNEL_NAME_PREFIX + "0")
        VOICE_TRACKER_CHANNEL_ID = created_channel.id
        print(f"สร้างช่อง Voice Tracker ใหม่: {created_channel.name}")
    else:
        print(f"ใช้ช่อง Voice Tracker เดิม: {CHANNEL_NAME_PREFIX}")

    # อัปเดตชื่อช่องครั้งแรก
    await update_voice_count()


async def update_voice_count():
    guild = client.get_guild(GUILD_ID)
    if not guild:
        return

    count = 0
    for vc in guild.voice_channels:
        if vc.id == VOICE_TRACKER_CHANNEL_ID:
            continue  # ข้ามห้องตัวเอง
        count += len(vc.members)

    # อัปเดตชื่อช่อง
    tracker_channel = guild.get_channel(VOICE_TRACKER_CHANNEL_ID)
    await tracker_channel.edit(name=f"{CHANNEL_NAME_PREFIX}{count}")


@client.event
async def on_voice_state_update(member, before, after):
    # อัปเดตทุกครั้งที่มีคนเข้า/ออก/ย้ายห้อง
    await update_voice_count()


client.run(TOKEN)
