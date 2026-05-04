import re
import time
from fractions import Fraction
from decimal import Decimal, ROUND_CEILING
from math import floor


async def mask_single_underscores(text):
    return re.sub(r'(?<!_)_(?!_)', '\\_', text)


async def calculate_end_time(total_attacks_needed, current_energy, current_player_number, count_afk_player, attack_energy_cost=5, energy_regen_rate=2, regen_interval=2):
    total_energy_needed = total_attacks_needed * attack_energy_cost
    energy_needed = int(total_energy_needed) - current_energy
    if energy_needed <= 0:
        return "ending soon", ""
    if current_player_number == count_afk_player:
        return "At least one player has to be active.", ""
    try:
        regen_time_needed = (energy_needed / (energy_regen_rate * (int(current_player_number) - int(count_afk_player))) * regen_interval)
    except ZeroDivisionError:
        return "lobby afk", ""
    remaining_minutes = max(0, regen_time_needed)
    if remaining_minutes < 5:
        return "ending soon", ""
    else:
        current_unix_time = int(time.time())
        additional_seconds = remaining_minutes * 60
        final_unix_time = f"[<t:{int(current_unix_time + additional_seconds)}:T>]"
        time_converted = await convert_to_hours_minutes(int(remaining_minutes))
        return time_converted, final_unix_time


async def calculate_end_time_including_afk(total_attacks_needed, current_energy, current_player_number, count_afk_player, attack_energy_cost=5, energy_regen_rate=2, regen_interval=2):
    if current_player_number == count_afk_player:
        return "please attack", ""
    total_energy_needed = total_attacks_needed * attack_energy_cost
    energy_needed = int(total_energy_needed) - current_energy
    if energy_needed <= 0:
        return "ending soon", ""
    regen_time_needed = (energy_needed / (energy_regen_rate * int(current_player_number)) * regen_interval)
    remaining_minutes = max(0, regen_time_needed)
    if remaining_minutes < 5:
        return "ending soon", ""
    else:
        current_unix_time = int(time.time())
        additional_seconds = remaining_minutes * 60
        final_unix_time = f"[<t:{int(current_unix_time + additional_seconds)}:T>]"
        time_converted = await convert_to_hours_minutes(int(remaining_minutes))
        return time_converted, final_unix_time


async def convert_to_hours_minutes(time_in_minutes):
    hours = time_in_minutes // 60
    minutes = time_in_minutes % 60
    return f"{hours} hour(s), {minutes} minutes"


async def build_boss_hp_bar(current_boss_hp, max_boss_hp):
    missing_boss_hp = int(max_boss_hp) - int(current_boss_hp)
    if missing_boss_hp == 0:
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_r:1325526982938595489>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.9):
        boss_hp_emoji = ("<:hp_r_l:1325527025062117586><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.8):
        boss_hp_emoji = ("<:hp_y_l:1325527035044560907><:hp_y_m:1325527047405310022><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.7):
        boss_hp_emoji = ("<:hp_y_l:1325527035044560907><:hp_y_m:1325527047405310022><:hp_y_m:1325527047405310022>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.6):
        boss_hp_emoji = ("<:hp_y_l:1325527035044560907><:hp_y_m:1325527047405310022><:hp_y_m:1325527047405310022>"
                         "<:hp_y_m:1325527047405310022><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.5):
        boss_hp_emoji = ("<:hp_y_l:1325527035044560907><:hp_y_m:1325527047405310022><:hp_y_m:1325527047405310022>"
                         "<:hp_y_m:1325527047405310022><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.4):
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_b_m:1325526996612022322>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.3):
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.2):
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_b_m:1325526996612022322><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp > (int(max_boss_hp) * 0.1):
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_b_m:1325526996612022322>"
                         "<:hp_b_r:1325527015381663754>")
    elif missing_boss_hp < int(max_boss_hp):
        boss_hp_emoji = ("<:hp_g_l:1325526952462778368><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295><:hp_g_m:1325526971995787295>"
                         "<:hp_b_r:1325527015381663754>")
    return boss_hp_emoji


async def element_effectiveness(element_1, element_2):
    null = "<:Null:1329746549382582285>"
    if element_1 == "⚡":
        if element_2 == "⚡":
            status = 1
        elif element_2 == "⛰":
            status = -1
        elif element_2 == "🍃":
            status = 0
        elif element_2 == "🔥":
            status = 0
        elif element_2 == "💧":
            status = 2
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "⛰":
        if element_2 == "⚡":
            status = 2
        elif element_2 == "⛰":
            status = 1
        elif element_2 == "🍃":
            status = -1
        elif element_2 == "🔥":
            status = 0
        elif element_2 == "💧":
            status = 0
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "🍃":
        if element_2 == "⚡":
            status = 0
        elif element_2 == "⛰":
            status = 2
        elif element_2 == "🍃":
            status = 1
        elif element_2 == "🔥":
            status = -1
        elif element_2 == "💧":
            status = 0
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "🔥":
        if element_2 == "⚡":
            status = 0
        elif element_2 == "⛰":
            status = 0
        elif element_2 == "🍃":
            status = 2
        elif element_2 == "🔥":
            status = 1
        elif element_2 == "💧":
            status = -1
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "💧":
        if element_2 == "⚡":
            status = -1
        elif element_2 == "⛰":
            status = 0
        elif element_2 == "🍃":
            status = 0
        elif element_2 == "🔥":
            status = 2
        elif element_2 == "💧":
            status = 1
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "🌙":
        if element_2 == "⚡":
            status = 0
        elif element_2 == "⛰":
            status = 0
        elif element_2 == "🍃":
            status = 0
        elif element_2 == "🔥":
            status = 0
        elif element_2 == "💧":
            status = 0
        elif element_2 == "🌙":
            status = 2
        elif element_2 == "☀":
            status = -1
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "☀":
        if element_2 == "⚡":
            status = 0
        elif element_2 == "⛰":
            status = 0
        elif element_2 == "🍃":
            status = 0
        elif element_2 == "🔥":
            status = 0
        elif element_2 == "💧":
            status = 0
        elif element_2 == "🌙":
            status = -1
        elif element_2 == "☀":
            status = 2
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == "✨":
        if element_2 == "⚡":
            status = 0
        elif element_2 == "⛰":
            status = 0
        elif element_2 == "🍃":
            status = 0
        elif element_2 == "🔥":
            status = 0
        elif element_2 == "💧":
            status = 0
        elif element_2 == "🌙":
            status = 0
        elif element_2 == "☀":
            status = 0
        elif element_2 == "✨":
            status = 1
        elif element_2 == null:
            status = -0.5
    elif element_1 == null:
        status = 1
    return status


async def element_converter_from_database(card_element_name):
    null = "<:NULL:1338512039156645992>"
    card_element = ""
    if card_element_name == "Null":
        card_element = null
    elif card_element_name == "Neutral":
        card_element = ":sparkles:"
    elif card_element_name == "Electric":
        card_element = ":zap:"
    elif card_element_name == "Ground":
        card_element = ":mountain:"
    elif card_element_name == "Grass":
        card_element = ":leaves:"
    elif card_element_name == "Fire":
        card_element = ":fire:"
    elif card_element_name == "Water":
        card_element = ":droplet:"
    elif card_element_name == "Light":
        card_element = ":sunny:"
    elif card_element_name == "Dark":
        card_element = ":crescent_moon:"
    return card_element


async def skill_converter_from_database(card_skill_name):
    skill_name = ""
    if card_skill_name == "Lucky Coin":
        skill_name = "<:LUCKY_COIN:1335616797449125888>"
    elif card_skill_name == "Amplifier":
        skill_name = "<:AMPLIFIER:1335617081013440573>"
    elif card_skill_name == "Arcane Affinity":
        skill_name = "<:Arcane_Affinity:1335617073505636372>"
    elif card_skill_name == "Balancing Strike":
        skill_name = "<:Balancing_Strike:1335617062390992996>"
    elif card_skill_name == "Berserker":
        skill_name = "<:Berserker:1335617052987097189>"
    elif card_skill_name == "Blaze":
        skill_name = "<:Blaze:1335617044372000860>"
    elif card_skill_name == "Blood Surge":
        skill_name = "<:Blood_Surge:1335617034632953949>"
    elif card_skill_name == "Bloodthirster":
        skill_name = "<:Bloodthirster:1335617024134610944>"
    elif card_skill_name == "Breaker":
        skill_name = "<:Breaker:1335617008133214238>"
    elif card_skill_name == "Brutality":
        skill_name = "<:Brutality:1335616998968791041>"
    elif card_skill_name == "Celestial Blessing":
        skill_name = "<:Celestial_Blessing:1335616987967127684>"
    elif card_skill_name == "Celestial Influence":
        skill_name = "<:Celestial_Influence:1335616977707733084>"
    elif card_skill_name == "Cursed":
        skill_name = "<:Cursed:1335616960129531964>"
    elif card_skill_name == "Devour":
        skill_name = "<:Devour:1335616950264401993>"
    elif card_skill_name == "Dexterity Drive":
        skill_name = "<:Dexterity_Drive:1335616941380993105>"
    elif card_skill_name == "Divine Blessing":
        skill_name = "<:Divine_Blessing:1335616933323608125>"
    elif card_skill_name == "Dominance":
        skill_name = "<:Dominance:1335616923668451368>"
    elif card_skill_name == "Double-edged Strike":
        skill_name = "<:Double_edged_Strike:1335616913484677231>"
    elif card_skill_name == "Elemental Drain":
        skill_name = "<:Elemental_Drain:1335616903913275433>"
    elif card_skill_name == "Elemental Manipulation":
        skill_name = "<:Elemental_Manipulation:1335616891623837697>"
    elif card_skill_name == "Elemental Strike":
        skill_name = "<:Elemental_Strike:1335616878931873822>"
    elif card_skill_name == "Endurance":
        skill_name = "<:Endurance:1335616869138169856>"
    elif card_skill_name == "Executioner":
        skill_name = "<:Executioner:1335616849299378257>"
    elif card_skill_name == "Foul Play":
        skill_name = "<:Foul_Play:1335616838549110856>"
    elif card_skill_name == "Vengeance":
        skill_name = "<:Vengeance:1335616408347873283>"
    elif card_skill_name == "Yin Yang":
        skill_name = "<:Yin_Yang:1335616388567531661>"
    elif card_skill_name == "Offensive Stance":
        skill_name = "<:Offensive_Stance:1335616767300468846>"
    elif card_skill_name == "Overload":
        skill_name = "<:Overload:1335616751752450129>"
    elif card_skill_name == "Pain For Power":
        skill_name = "<:Pain_For_Power:1335616736866734222>"
    elif card_skill_name == "Paralysis":
        skill_name = "<:Paralysis:1335616727312109589>"
    elif card_skill_name == "Poison":
        skill_name = "<:Poison:1335616714322477177>"
    elif card_skill_name == "Precision":
        skill_name = "<:Precision:1335616702712381520>"
    elif card_skill_name == "Protector":
        skill_name = "<:Protector:1335616686140686469>"
    elif card_skill_name == "Recoil":
        skill_name = "<:Recoil:1335616675046752348>"
    elif card_skill_name == "Life Sap":
        skill_name = "<:Life_Sap:1335616663382528091>"
    elif card_skill_name == "Reflector":
        skill_name = "<:Reflector:1335616644092919879>"
    elif card_skill_name == "Regeneration":
        skill_name = "<:Regeneration:1335616631774249032>"
    elif card_skill_name == "Rejuvenation":
        skill_name = "<:Rejuvenation:1335616621724831876>"
    elif card_skill_name == "Restricted Instinct":
        skill_name = "<:Restricted_Instinct:1335616611045998705>"
    elif card_skill_name == "Reversion":
        skill_name = "<:Reversion:1335616600602316881>"
    elif card_skill_name == "Rising Resolve":
        skill_name = "<:Rising_Resolve:1335616590577926225>"
    elif card_skill_name == "Smokescreen":
        skill_name = "<:Smokescreen:1335616580318658592>"
    elif card_skill_name == "Soul Stealer":
        skill_name = "<:Soul_Stealer:1335616569694359603>"
    elif card_skill_name == "Temporal Rewind":
        skill_name = "<:Temporal_Rewind:1335616556058804255>"
    elif card_skill_name == "Time Attack":
        skill_name = "<:Time_Attack:1335616536542576671>"
    elif card_skill_name == "Time Bomb":
        skill_name = "<:Time_Bomb:1335616525352308839>"
    elif card_skill_name == "Trick Room":
        skill_name = "<:Trick_Room:1335616485900554321>"
    elif card_skill_name == "Transformation":
        skill_name = "<:Transformation:1335616512152567901>"
    elif card_skill_name == "Ultimate Combo":
        skill_name = "<:Ultimate_Combo:1335616472709333023>"
    elif card_skill_name == "Undying Will":
        skill_name = "<:Undying_Will:1335616441176555580>"
    elif card_skill_name == "Unlucky Coin":
        skill_name = "<:Unlucky_Coin:1335616425603235840>"
    elif card_skill_name == "Omniscient Hack":
        skill_name = "<:Omniscient_Hack:1336069861843144806>"
    elif card_skill_name == "Miracle Injection":
        skill_name = "<:Miracle_Injection:1335616777895284776>"
    elif card_skill_name == "Mana Reaver":
        skill_name = "<:Mana_Reaver:1335616788196753408>"
    elif card_skill_name == "Lethal Clarity":
        skill_name = "<:Lethal_Clarity:1335616806890504313>"
    elif card_skill_name == "Grievous Limiter":
        skill_name = "<:Grievous_Limiter:1335616818483691580>"
    elif card_skill_name == "Underdog":
        skill_name = "<:Underdog:1336428564739915837>"
    elif card_skill_name == "Freeze":
        skill_name = "<:Freeze:1335616828399026260>"
    elif card_skill_name == "Evasion":
        skill_name = "<:Evasion:1335616859592196149>"
    elif card_skill_name == "Atmospheric Acceleration":
        skill_name = "<:ATMOSPHERIC_ACCELERATION:1356654809842974770>"
    elif card_skill_name == "Aegis":
        skill_name = "<:Aegis:1453105739395764478>"
    elif card_skill_name == "Divine Fortune":
        skill_name = "<:DivineFortune:1483474576657616937>"
    return skill_name


async def calc_card_stats(card_hp, card_atk, card_def, card_spd, rarity, evolution, ascension, familiarity, clan_hp, clan_atk, clan_def, clan_spd):
    if rarity == "Base":
        rarity_scaling = 1.0
        card_level = 1
    elif rarity == "Common":
        rarity_scaling = 1.2
        card_level = 20
    elif rarity == "Uncommon":
        rarity_scaling = 1.4
        card_level = 30
    elif rarity == "Rare":
        rarity_scaling = 1.6
        card_level = 40
    elif rarity == "Super Rare":
        rarity_scaling = 1.8
        card_level = 50
    elif rarity == "Ultra Rare":
        rarity_scaling = 2.0
        card_level = 60
    else:
        rarity_scaling = 1.0
        card_level = 20
    calc_card_hp = floor(int(card_hp) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_hp / 100)))
    calc_card_atk = floor(int(card_atk) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_atk / 100)))
    calc_card_def = floor(int(card_def) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_def / 100)))
    calc_card_spd = floor(int(card_spd) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_spd / 100)))
    return calc_card_hp, calc_card_atk, calc_card_def, calc_card_spd

async def calc_card_stats_compare(card_hp, card_atk, card_def, card_spd, rarity, card_level, evolution, ascension, familiarity, clan_hp, clan_atk, clan_def, clan_spd):
    if rarity == "Base":
        rarity_scaling = 1.0
    elif rarity == "Common":
        rarity_scaling = 1.2
    elif rarity == "Uncommon":
        rarity_scaling = 1.4
    elif rarity == "Rare":
        rarity_scaling = 1.6
    elif rarity == "Super Rare":
        rarity_scaling = 1.8
    elif rarity == "Ultra Rare":
        rarity_scaling = 2.0
    else:
        rarity_scaling = 1.0
    calc_card_hp = floor(int(card_hp) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_hp / 100)))
    calc_card_atk = floor(int(card_atk) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_atk / 100)))
    calc_card_def = floor(int(card_def) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_def / 100)))
    calc_card_spd = floor(int(card_spd) * rarity_scaling * (1 + 0.005 * card_level) * (0.85 + (0.15 * evolution)) * (1 + (0.05 * ascension)) * (1 + (familiarity / 100)) * (1 + (clan_spd / 100)))
    return calc_card_hp, calc_card_atk, calc_card_def, calc_card_spd