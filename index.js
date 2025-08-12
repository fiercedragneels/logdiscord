const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildPresences
    ]
});

const TOKEN = process.env.BOT_TOKEN;
const CHANNEL_NAME = "🎙️ คนใน Voice:"; // ชื่อช่องที่จะให้บอทสร้าง

client.on('ready', async () => {
    console.log(`✅ Logged in as ${client.user.tag}`);

    const guild = client.guilds.cache.first();
    if (!guild) return console.error("บอทไม่ได้อยู่ในเซิร์ฟเวอร์ใด");

    // สร้างหรือหา Channel สำหรับ Counter
    let counterChannel = guild.channels.cache.find(c => c.name.startsWith(CHANNEL_NAME));
    if (!counterChannel) {
        counterChannel = await guild.channels.create({
            name: `${CHANNEL_NAME} 0`,
            type: 2, // Voice Channel
        });
    }

    updateCounter(counterChannel, guild);
});

client.on('voiceStateUpdate', async () => {
    const guild = client.guilds.cache.first();
    const counterChannel = guild.channels.cache.find(c => c.name.startsWith(CHANNEL_NAME));
    if (counterChannel) updateCounter(counterChannel, guild);
});

function updateCounter(channel, guild) {
    const voiceCount = guild.channels.cache
        .filter(ch => ch.type === 2) // Voice only
        .map(ch => ch.members.size)
        .reduce((a, b) => a + b, 0);

    channel.setName(`${CHANNEL_NAME} ${voiceCount}`);
}

client.login(TOKEN);
