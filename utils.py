async def role_reaction_emojis(key=None):
    emojis = {
        "VA": "<:VA:475837654404169728>",
        "Female": "<:female:475837654513090570>",
        "Male": "<:male:475837650398478338>",
        "Artist": "<:artist:475837648934535188>",
        "Editor": "<:editor:475837650386026497>",
        "Animator": "<:animator:475837647126790154>",
        "Writer": "<:writer:475837653208793088>",
        "Singer": "<:singer:475837654848634890>",
        "Composer": "<:composer:475837647378579477>",
        "Director": "<:director:475837653112061957>",
        "GameDev": "<:gamedev:475837647403745280>",
        "Rapper": "<:rapper:475837650452873216>",
        "Sound": "<:sound:475837637433753610>",
        "Member": "✅"
    }
    if key == None:
        return emojis
    else:
        key_list = list(emojis.keys())
        val_list = list(emojis.values())
        return key_list[val_list.index(key)]

async def role_reaction_roles(role):
    roles = {
        "VA": 326936877435453442,
        "Female": 318456346980777985,
        "Male": 318456349434314752, 
        "Artist": 326377189991907328,
        "Editor": 326377369696993281,
        "Animator": 326377428467449856,
        "Writer": 326377605060100096,
        "Singer": 326377783347642369,
        "Composer": 326377843879575552,
        "Director": 326936601915817986,
        "GameDev": 336220991447629826,
        "Rapper": 339907116460670996,
        "Sound": 326377524567343104,
        "Member": 700161690540441641,
        "Roleless": 335620228295950337
    }
    return roles.get(role, "error")