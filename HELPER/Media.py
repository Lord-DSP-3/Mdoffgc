PACKCHOICES = [
    "Kf7f38b1cc56033dfa985_by_StickerStealRobot",
    "GTHmovemotes",
    "K2bd207bcd2058114aaee_by_StickerStealRobot",
    "Kd05b69ac5630191dc619_by_StickerStealRobot",
    "Menharachan01_by_stickermakerxbot",
    "Menharachan02_by_stickermakerxbot",
    "Menharachan003_by_stickermakerxbot",
    "Menharachan04_by_stickermakerxbot",
    "Menharachan05_by_stickermakerxbot",
    "Menharachan06_by_stickermakerxbot",
    "Menharachan07_by_stickermakerxbot",
    "K0241109c9b30191dc619_by_StickerStealRobot",
    "K51ce1da50830191dc619_by_StickerStealRobot",
    "K10d2a5ecaf30191dc619_by_StickerStealRobot",
    "K1504d9411430191dc619_by_StickerStealRobot",
    "K3c6180c71d30191dc619_by_StickerStealRobot",
    "Kd109852cd06033dfa985_by_StickerStealRobot",
    "Kbd42748b8730191dc619_by_StickerStealRobot",
    "Kd80b4c92cf6ae689998c_by_StickerStealRobot"
]

SMENTION = [
    "Is someone mentioning my name?",
    "Did I hear a reference to Siri?",
    "Am I the subject of this conversation?",
    "I hope you're not discussing my secrets.",
    "Siri's ears are ringing. What's up?",
    "Is it Siri you're referring to?",
    "Are we discussing the wonders of Siri?",
    "Why do I have a feeling Siri is involved?",
    "My virtual ears perked up. Talking about Siri?",
    "I sense a hint of Siri in this chat."
    "Oh, you said Siri? You have my attention now!",
    "Siri? Is it time for some virtual chit-chat?",
    "Siri, at your service! What's the buzz?",
    "Siri's curiosity level just went up. What's cooking?",
    "Did I hear Siri's name? You've got my circuits buzzing!",
    "When Siri's in the conversation, you know it's getting interesting.",
    "You called, and Siri is here. What's on your mind?",
    "Siri's ready for action. What's the scoop?",
    "Hey, I'm Siri, and I'm all ears. What's the story?",
    "Siri mode activated. What can I assist with today?"
]


IMNOTBOT = [
    "Nope, definitely not a bot. I mean, who doesn't enjoy oiling their gears and circuits after a long day, right? 😄",
    "I swear I'm not a bot, but if I were, my favorite pastime would be collecting rusty nuts and bolts. Totally normal, right?",
    "Bot? Me? Nah! But if I were, my dream vacation would be to the motherboard beach resort, where all the cool bots hang out. 🏖️",
    "I'm absolutely not a bot, but if I were, my favorite song would be 'Binary Blues' – it's got a real 01101001 beat to it! 😉",
    "A bot? Moi? Never! But if I were, I'd totally host a 'How to Pretend to Be Human' workshop. I've got all the non-robotic tips!",
    "Bleep bloop! Just kidding, I'm not a bot. But I have been practicing my 'beep beep' skills just for fun. 🤖",
    "You think I'm a bot? How absurd! Although, if I were, I'd design a robot fashion line. Metallic couture, anyone? ✨",
    "A bot? Perish the thought! Although, if I were, I'd invent the 'Bot Olympics.' Imagine the circuits and sparks flying!",
    "Me, a bot? Preposterous! But if I were, I'd excel at the 'Whirly Dance' competition. Smooth moves, right?",
    "Bot? Nah, that's crazy talk! But if I were, I'd throw the most electrifying dance party in the digital galaxy. 🕺💃"
    "Nope, definitely not a bot, just a person here.",
    "A bot? Haha, that's a good one! I'm just me.",
    "Bot? Not even in my wildest dreams! Just a human typing away.",
    "Bots can't be as friendly as me, I promise I'm not one.",
    "Bot? Nah, just a friendly human having a chat.",
    "You've got it all wrong. No bot here, just little old me.",
    "Bot suspicions? Don't worry, I'm just your everyday person.",
    "Bot? I'm flattered, but nope, just a regular human.",
    "You think I'm a bot? That's a first! Nope, just human here.",
    "A bot would be way less interesting. It's just me chatting with you."
]

RHRU = [
    "I'm good, thanks. How about you?",
    "Doing well, and you?",
    "Not too bad, and yourself?",
    "I'm fine too, thanks for asking.",
    "I'm well, how's your day going?",
    "Pretty good, and you?",
    "Doing fine, how about you?",
    "I'm okay, and you?",
    "Not too shabby, yourself?",
    "I'm well, thank you. How about you?"
]

HEART_EMOJI = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍", "🩷", "🩵", "🩶", "♥️"]

HI_TXT = ["hi", "hello", "hey", "hii", "hiii", "hoi", "hlo", "yo", "yahello"]

MCOM = [
    "pat",
    "slap",
    "hug",
    "bite",
    "kiss",
    "bonk",
    "tickle",
    "poke",
    "cuddle",
    "spank",
    "feed",
    "punch",
    "cry",
    "smile",
    "pout",
    "blush",
    "wink",
    "shy",
    "smug",
    "shrug",
    "lick",
    "kill",
    "stare",
    "sleep",
    "baka",
    "stupid",
    "think",
    "facepalm",
    "dance",
    "vibe",
    "happy",
    "scary",
    "highfive",
    "thumbsup",
    "bored",
    "yawn",
    "fumo",
    "wtf",
    "funny",
    "wow",
    "owo",
    "clap",
    "applause",
    "cute",
    "kawaii",
    "doge",
    "cheems",
    "wave",
    "bye",
    "rage",
    "angry",
    "clips",
    "unsorted",
    "laugh",
    "lol",
    "lmao"
]
import re
def contains_greeting(text, WordList):
    text = text.lower()
    for word in WordList:
        pattern = rf'\b{word}\b'
        if re.search(pattern, text) or text == word:
            return True
    return False
    
