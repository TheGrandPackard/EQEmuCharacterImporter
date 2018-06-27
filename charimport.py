#! /usr/bin/env python

"""
Given a directory of *-Inventory.txt and *-Spellbook.txt, populate, move, and edit existing characters
"""

import time
import datetime
import logging
import sys
import subprocess
import MySQLdb
from os import listdir
from os.path import isfile, join

__author__ = "Indefinite and TheGrandPackard"
__version__ = "0.0.2"


def time_stamp():
    """Returns a neat little timestamp for things"""
    unixstamp = int(time.time())
    timestamp = datetime.datetime.fromtimestamp(int(unixstamp))\
        .strftime('%Y-%m-%d %H:%M:%S')
    return str(timestamp)


def log(message):
    """Effectively just for timestamping all log messages"""
    logging.info('[' + time_stamp() + ']: ' + str(message))


def usage():
    """Prints usage and exits"""
    print("python charimport.py ./path/to/directory")
    sys.exit(1)

def import_chars(file_location, given_account_name):
    chars = []
    data = []
    upload_dir = file_location
    processed_dir = "/var/www/import/characterfiles/read"
    
    slot_ref = {
        'Charm' : 0,
        'Ear1' : 1,
        'Head' : 2,
        'Face' : 3,
        'Ear2' : 4,
        'Neck' : 5,
        'Shoulders' : 6,
        'Arms' : 7,
        'Back' : 8,
        'Wrist1' : 9,
        'Wrist2' : 10,
        'Range' : 11,
        'Hands' : 12,
        'Primary' : 13,
        'Secondary' : 14,
        'Fingers1' : 15,
        'Fingers2' : 16,
        'Chest' : 17,
        'Legs' : 18,
        'Feet' : 19,
        'Waist' : 20,
        'Ammo' : 21,
        'General1' : 22,
        'General1-Slot1' : 251,
        'General1-Slot2' : 252,
        'General1-Slot3' : 253,
        'General1-Slot4' : 254,
        'General1-Slot5' : 255,
        'General1-Slot6' : 256,
        'General1-Slot7' : 257,
        'General1-Slot8' : 258,
        'General1-Slot9' : 259,
        'General1-Slot10' : 260,
        'General2' : 23,
        'General2-Slot1' : 261,
        'General2-Slot2' : 262,
        'General2-Slot3' : 263,
        'General2-Slot4' : 264,
        'General2-Slot5' : 265,
        'General2-Slot6' : 266,
        'General2-Slot7' : 267,
        'General2-Slot8' : 268,
        'General2-Slot9' : 269,
        'General2-Slot10' : 270,
        'General3' : 24,
        'General3-Slot1' : 271,
        'General3-Slot2' : 272,
        'General3-Slot3' : 273,
        'General3-Slot4' : 274,
        'General3-Slot5' : 275,
        'General3-Slot6' : 276,
        'General3-Slot7' : 277,
        'General3-Slot8' : 278,
        'General3-Slot9' : 279,
        'General3-Slot10' : 280,
        'General4' : 25,
        'General4-Slot1' : 281,
        'General4-Slot2' : 282,
        'General4-Slot3' : 283,
        'General4-Slot4' : 284,
        'General4-Slot5' : 285,
        'General4-Slot6' : 286,
        'General4-Slot7' : 287,
        'General4-Slot8' : 288,
        'General4-Slot9' : 289,
        'General4-Slot10' : 290,
        'General5' : 26,
        'General5-Slot1' : 291,
        'General5-Slot2' : 292,
        'General5-Slot3' : 293,
        'General5-Slot4' : 294,
        'General5-Slot5' : 295,
        'General5-Slot6' : 296,
        'General5-Slot7' : 297,
        'General5-Slot8' : 298,
        'General5-Slot9' : 299,
        'General5-Slot10' : 300,
        'General6' : 27,
        'General6-Slot1' : 301,
        'General6-Slot2' : 302,
        'General6-Slot3' : 303,
        'General6-Slot4' : 304,
        'General6-Slot5' : 305,
        'General6-Slot6' : 306,
        'General6-Slot7' : 307,
        'General6-Slot8' : 308,
        'General6-Slot9' : 309,
        'General6-Slot10' : 310,
        'General7' : 28,
        'General7-Slot1' : 311,
        'General7-Slot2' : 312,
        'General7-Slot3' : 313,
        'General7-Slot4' : 314,
        'General7-Slot5' : 315,
        'General7-Slot6' : 316,
        'General7-Slot7' : 317,
        'General7-Slot8' : 318,
        'General7-Slot9' : 319,
        'General7-Slot10' : 320,
        'General8' : 29,
        'General8-Slot1' : 321,
        'General8-Slot2' : 322,
        'General8-Slot3' : 323,
        'General8-Slot4' : 324,
        'General8-Slot5' : 325,
        'General8-Slot6' : 326,
        'General8-Slot7' : 327,
        'General8-Slot8' : 328,
        'General8-Slot9' : 329,
        'General8-Slot10' : 330,
	    'Held' : 30,
        'Held-Slot1' : 331,
        'Held-Slot2' : 332,
        'Held-Slot3' : 333,
        'Held-Slot4' : 334,
        'Held-Slot5' : 335,
        'Held-Slot6' : 336,
        'Held-Slot7' : 337,
        'Held-Slot8' : 338,
        'Held-Slot9' : 339,
        'Held-Slot10' : 340,
        'Bank1' : 2000,
        'Bank1-Slot1' :2031,
        'Bank1-Slot2' :2032,
        'Bank1-Slot3' :2033,
        'Bank1-Slot4' :2034,
        'Bank1-Slot5' :2035,
        'Bank1-Slot6' :2036,
        'Bank1-Slot7' :2037,
        'Bank1-Slot8' :2038,
        'Bank1-Slot9' :2039,
        'Bank1-Slot10' :2040,
        'Bank2' : 2001,
        'Bank2-Slot1' :2041,
        'Bank2-Slot2' :2042,
        'Bank2-Slot3' :2043,
        'Bank2-Slot4' :2044,
        'Bank2-Slot5' :2045,
        'Bank2-Slot6' :2046,
        'Bank2-Slot7' :2047,
        'Bank2-Slot8' :2048,
        'Bank2-Slot9' :2049,
        'Bank2-Slot10' :2050,
        'Bank3' : 2002,
        'Bank3-Slot1' :2051,
        'Bank3-Slot2' :2052,
        'Bank3-Slot3' :2053,
        'Bank3-Slot4' :2054,
        'Bank3-Slot5' :2055,
        'Bank3-Slot6' :2056,
        'Bank3-Slot7' :2057,
        'Bank3-Slot8' :2058,
        'Bank3-Slot9' :2059,
        'Bank3-Slot10' :2060,
        'Bank4' : 2003,
        'Bank4-Slot1' :2061,
        'Bank4-Slot2' :2062,
        'Bank4-Slot3' :2063,
        'Bank4-Slot4' :2064,
        'Bank4-Slot5' :2065,
        'Bank4-Slot6' :2066,
        'Bank4-Slot7' :2067,
        'Bank4-Slot8' :2068,
        'Bank4-Slot9' :2069,
        'Bank4-Slot10' :2070,
        'Bank5' : 2004,
        'Bank5-Slot1' :2071,
        'Bank5-Slot2' :2072,
        'Bank5-Slot3' :2073,
        'Bank5-Slot4' :2074,
        'Bank5-Slot5' :2075,
        'Bank5-Slot6' :2076,
        'Bank5-Slot7' :2077,
        'Bank5-Slot8' :2078,
        'Bank5-Slot9' :2079,
        'Bank5-Slot10' :2080,
        'Bank6' : 2005,
        'Bank6-Slot1' :2081,
        'Bank6-Slot2' :2082,
        'Bank6-Slot3' :2083,
        'Bank6-Slot4' :2084,
        'Bank6-Slot5' :2085,
        'Bank6-Slot6' :2086,
        'Bank6-Slot7' :2087,
        'Bank6-Slot8' :2088,
        'Bank6-Slot9' :2089,
        'Bank6-Slot10' :2090,
        'Bank7' : 2006,
        'Bank7-Slot1' :2091,
        'Bank7-Slot2' :2092,
        'Bank7-Slot3' :2093,
        'Bank7-Slot4' :2094,
        'Bank7-Slot5' :2095,
        'Bank7-Slot6' :2096,
        'Bank7-Slot7' :2097,
        'Bank7-Slot8' :2098,
        'Bank7-Slot9' :2099,
        'Bank7-Slot10' :2100,
        'Bank8' : 2007,
        'Bank8-Slot1' :2101,
        'Bank8-Slot2' :2102,
        'Bank8-Slot3' :2103,
        'Bank8-Slot4' :2104,
        'Bank8-Slot5' :2105,
        'Bank8-Slot6' :2106,
        'Bank8-Slot7' :2107,
        'Bank8-Slot8' :2108,
        'Bank8-Slot9' :2109,
        'Bank8-Slot10' :2110,
        'Bank9' : 2008,
        'Bank9-Slot1' :2111,
        'Bank9-Slot2' :2112,
        'Bank9-Slot3' :2113,
        'Bank9-Slot4' :2114,
        'Bank9-Slot5' :2115,
        'Bank9-Slot6' :2116,
        'Bank9-Slot7' :2117,
        'Bank9-Slot8' :2118,
        'Bank9-Slot9' :2119,
        'Bank9-Slot10' :2120,
        'Bank10' : 2009,
        'Bank10-Slot1' :2121,
        'Bank10-Slot2' :2122,
        'Bank10-Slot3' :2123,
        'Bank10-Slot4' :2124,
        'Bank10-Slot5' :2125,
        'Bank10-Slot6' :2126,
        'Bank10-Slot7' :2127,
        'Bank10-Slot8' :2128,
        'Bank10-Slot9' :2129,
        'Bank10-Slot10' :2130,
        'Bank11' : 2010,
        'Bank11-Slot1' :2131,
        'Bank11-Slot2' :2132,
        'Bank11-Slot3' :2133,
        'Bank11-Slot4' :2134,
        'Bank11-Slot5' :2135,
        'Bank11-Slot6' :2136,
        'Bank11-Slot7' :2137,
        'Bank11-Slot8' :2138,
        'Bank11-Slot9' :2139,
        'Bank11-Slot10' :2140,
        'Bank12' : 2011,
        'Bank12-Slot1' :2141,
        'Bank12-Slot2' :2142,
        'Bank12-Slot3' :2143,
        'Bank12-Slot4' :2144,
        'Bank12-Slot5' :2145,
        'Bank12-Slot6' :2146,
        'Bank12-Slot7' :2147,
        'Bank12-Slot8' :2148,
        'Bank12-Slot9' :2149,
        'Bank12-Slot10' :2150,
        'Bank13' : 2012,
        'Bank13-Slot1' :2151,
        'Bank13-Slot2' :2152,
        'Bank13-Slot3' :2153,
        'Bank13-Slot4' :2154,
        'Bank13-Slot5' :2155,
        'Bank13-Slot6' :2156,
        'Bank13-Slot7' :2157,
        'Bank13-Slot8' :2158,
        'Bank13-Slot9' :2159,
        'Bank13-Slot10' :2160,
        'Bank14' : 2013,
        'Bank14-Slot1' :2161,
        'Bank14-Slot2' :2162,
        'Bank14-Slot3' :2163,
        'Bank14-Slot4' :2164,
        'Bank14-Slot5' :2165,
        'Bank14-Slot6' :2166,
        'Bank14-Slot7' :2167,
        'Bank14-Slot8' :2168,
        'Bank14-Slot9' :2169,
        'Bank14-Slot10' :2170,
        'Bank15' : 2014,
        'Bank15-Slot1' :2171,
        'Bank15-Slot2' :2172,
        'Bank15-Slot3' :2173,
        'Bank15-Slot4' :2174,
        'Bank15-Slot5' :2175,
        'Bank15-Slot6' :2176,
        'Bank15-Slot7' :2177,
        'Bank15-Slot8' :2178,
        'Bank15-Slot9' :2179,
        'Bank15-Slot10' :2180,
        'Bank16' : 2015,
        'Bank16-Slot1' :2181,
        'Bank16-Slot2' :2182,
        'Bank16-Slot3' :2183,
        'Bank16-Slot4' :2184,
        'Bank16-Slot5' :2185,
        'Bank16-Slot6' :2186,
        'Bank16-Slot7' :2187,
        'Bank16-Slot8' :2188,
        'Bank16-Slot9' :2189,
        'Bank16-Slot10' :2190,
        'SharedBank1' : 2500,
        'SharedBank1-Slot1' : 2531,
        'SharedBank1-Slot2' : 2532,
        'SharedBank1-Slot3' : 2533,
        'SharedBank1-Slot4' : 2534,
        'SharedBank1-Slot5' : 2535,
        'SharedBank1-Slot6' : 2536,
        'SharedBank1-Slot7' : 2537,
        'SharedBank1-Slot8' : 2538,
        'SharedBank1-Slot9' : 2539,
        'SharedBank1-Slot10' : 2540,
        'SharedBank2' : 2501,
        'SharedBank2-Slot1' : 2541,
        'SharedBank2-Slot2' : 2542,
        'SharedBank2-Slot3' : 2543,
        'SharedBank2-Slot4' : 2544,
        'SharedBank2-Slot5' : 2545,
        'SharedBank2-Slot6' : 2546,
        'SharedBank2-Slot7' : 2547,
        'SharedBank2-Slot8' : 2548,
        'SharedBank2-Slot9' : 2549,
        'SharedBank2-Slot10' : 2550
    }


    # Enable Logging
    logging.basicConfig(filename='import.log', level=logging.DEBUG)
    log('Initializing...')

    # Scan directory for char files
    dirfiles = [ f for f in listdir(upload_dir)  if isfile(join(upload_dir, f)) ]
    for files in dirfiles:
        if ".txt" not in files and "-" not in files:
            continue
        charname, extra = files.split("-", 2)
        if extra == "Inventory.txt" or extra == "Spellbook.txt":
            if charname not in chars:
                log('Found data for player %s' % charname)
                chars.append(charname)

    # Connect to DB
    db = MySQLdb.connect(host="localhost", port=3306, user="eqemu", passwd="eqemu", db="eqemu")
    cursor = db.cursor()
    log('Connected to mysql')

    # For each char with files to import
    for char_name in chars:

        # Find account and character data
        char_name = char_name.strip()
        cursor.execute("""SELECT a.name, a.id, d.id, d.class FROM account as a, character_data as d WHERE a.id = d.account_id AND d.name LIKE '%s'""" % MySQLdb.escape_string(char_name))
        data = cursor.fetchone()
        if data == None:
            log('Account found for player %s' % char_name)
            continue
        account_name = data[0]
        if account_name.lower() != given_account_name.lower():
            log('Invalid account %s for player %s' % (account_name, char_name))
            continue
        account_id = data[1]
        char_id = data[2]
        char_class = data[3]
        log('Found account for player %s' % (char_name))

        # Process inventory
        if isfile('%s/%s-Inventory.txt' % (upload_dir, char_name)):
            inv_fd = open('%s/%s-Inventory.txt' % (upload_dir, char_name), 'r')
            double_equips = { 'Ear' : False, 'Wrist' : False, 'Fingers' : False }

            log('Processing inventory for %s' % char_name)
            line = inv_fd.readline() # Title
            line = inv_fd.readline() # Charm
            while line:
                line.rstrip()
                loc, item_name, item_id, charges, slots = line.split('\t', 5)
                
                #try:
                if loc == "Ear":
                    if not double_equips[loc]:
                        slot_id = slot_ref['Ear1']
                        double_equips[loc] = True
                    else:
                        slot_id = slot_ref['Ear2']
                elif loc == "Wrist":
                    if not double_equips[loc]:
                        slot_id = slot_ref['Wrist1']
                        double_equips[loc] = True
                    else:
                        slot_id = slot_ref['Wrist2']
                elif loc == "Fingers":
                    if not double_equips[loc]:
                        slot_id = slot_ref['Fingers1']
                        double_equips[loc] = True
                    else:
                        slot_id = slot_ref['Fingers2']
                else:
                    slot_id = slot_ref[loc]
                #except KeyError:
                 #   continue
    
                if item_id != "0":
                    cursor.execute("""SELECT color, stackable, maxcharges FROM items WHERE id = %s""" % MySQLdb.escape_string(item_id))
                    data = cursor.fetchone()

                    if data:
                        color = data[0]
                        stackable = data[1]
                        maxcharges = data[2]

                        if maxcharges == -1:
                            charges = 32767
                        elif stackable == 0:
                            charges = maxcharges                                         
    
                        log('Adding %s to %s\'s inventory' % (item_name, char_name))
                        cursor.execute("""REPLACE INTO inventory SET itemid = %s, charges = %s, color = %s, charid = %s, slotid = %s""" %
                              (MySQLdb.escape_string(item_id), charges, color, char_id, slot_id))
                    else:
                        log('Adding %s to %s\'s inventory' % (item_name, char_name))
                        log('item id %s for %s cannot be found in the database, reverting to name search' % (item_id, item_name))
                        cursor.execute("""SELECT id, color, stackable, maxcharges FROM items WHERE Name = '%s'""" % MySQLdb.escape_string(item_name))
                        data = cursor.fetchone()
                        if not data:
                            log('Cannot find item %s anywhere, giving up' % item_name)
                            line = inv_fd.readline()
                            continue
                        item_id = data[0]
                        color = data[1]
                        stackable = data[2]
                        maxcharges = data[3]

                        if maxcharges == -1:
                            charges = 32767
                        elif stackable == 0:
                            charges = maxcharges
 
                        log('Adding %s to %s\'s inventory' % (item_name, char_name))
                        cursor.execute("""REPLACE INTO inventory SET itemid = %s, charges = (SELECT maxcharges FROM items WHERE id = %s), color = %s, charid = %s, slotid = %s""" %
                            (item_id, item_id, color, char_id, slot_id))
                line = inv_fd.readline()
            inv_fd.close()
            subprocess.call(["mv %s/%s-Inventory.txt %s/%s-Inventory.txt" % (upload_dir, (MySQLdb.escape_string(char_name)), processed_dir, (MySQLdb.escape_string(char_name)))], shell=True)
            log('Finished processing inventory for %s' % char_name)


        # Process spellbook
        if isfile('%s/%s-Spellbook.txt' % (upload_dir, char_name)):
            spell_fd = open('%s/%s-Spellbook.txt' % (upload_dir, (MySQLdb.escape_string(char_name))), 'r')
            slot_count = 0
            log('Processing spellbook for %s' % char_name)
            line = spell_fd.readline()
            while line:
                line.rstrip()
                mystery_number, spell_name = line.split('\t', 2)
                spell_name = spell_name.rstrip()
                log('Looking up Spell: %s' % spell_name)
                cursor.execute("""SELECT id FROM spells_new WHERE name = '%s' AND classes%s < 61 LIMIT 1""" % (MySQLdb.escape_string(spell_name), char_class))
                data = cursor.fetchone()
                # If normal lookup worked, add spell
                if data:
                    spell_id = data[0]
                    log('Adding [%s] to %s\'s spellbook' % (spell_name, char_name))
                    cursor.execute("""REPLACE INTO character_spells SET id = %s, slot_id = %s, spell_id = %s""" % (char_id, slot_count, spell_id))
                # Otherwise check for apostrophe condition
                elif '`' in spell_name:
                    spell_name_altered = str.replace(spell_name, '`', '\'')
                    log('Unable to find Spell: [%s]! Trying [%s]' % (spell_name, spell_name_altered))
                    cursor.execute("""SELECT id FROM spells_new WHERE name = '%s' AND classes%s < 61 LIMIT 1""" % (MySQLdb.escape_string(spell_name_altered), char_class))
                    data = cursor.fetchone()
                    if data:
                        spell_id = data[0]
                        log('Adding [%s] to %s\'s spellbook' % (spell_name_altered, char_name))
                        cursor.execute("""REPLACE INTO character_spells SET id = %s, slot_id = %s, spell_id = %s""" % (char_id, slot_count, spell_id))
                    else:
                        log('Failed to find Spell: [%s]! ' % (spell_name))
                # Otherwise check for truncated condition
                else:           
                    log('Unable to find Spell: [%s]! Trying [%s]' % (spell_name, spell_name[:-1]))
                    cursor.execute("""SELECT id FROM spells_new WHERE name = '%s' AND classes%s < 61 LIMIT 1""" % (MySQLdb.escape_string(spell_name[:-1]), char_class))
                    data = cursor.fetchone()
                    if data:
                        spell_id = data[0]
                        log('Adding [%s] to %s\'s spellbook' % (spell_name_altered, char_name))
                        cursor.execute("""REPLACE INTO character_spells SET id = %s, slot_id = %s, spell_id = %s""" % (char_id, slot_count, spell_id))
                    else:
                        log('Failed to find Spell: [%s]' % (spell_name))

                slot_count = slot_count + 1
                line = spell_fd.readline()
            spell_fd.close()
            subprocess.call(["mv %s/%s-Spellbook.txt %s/%s-Spellbook.txt" % (upload_dir, (MySQLdb.escape_string(char_name)), processed_dir, (MySQLdb.escape_string(char_name)))], shell=True)
            log('Finished processing spellbook for %s' % char_name)
        
        # Modify player skills, level, location, guild, and bind point
        log('Updating %s\'s level and location' % char_name)
        cursor.execute("""UPDATE character_data SET zone_id = 202, zone_instance = 0, y = 374.11, x = 356.25, z = -125.87, heading = 157.0, level = 60, exp = 616137024 WHERE id = %s""" % char_id)
        log('Updating %s\'s skills' % char_name)
        cursor.execute("""REPLACE INTO character_skills SELECT %s, skill_caps.skillID, MAX(skill_caps.cap) FROM skill_caps WHERE class = %s GROUP BY skill_caps.skillID""" % (char_id, char_class))
        log('Updating %s\'s bind point' % char_name)
        cursor.execute("""UPDATE character_bind SET y = 374.11, x = 356.25, z = -125.87, heading = 157.0, zone_id = 202 WHERE id = %s""" % char_id)
        log('Updating %s\'s guild status' % char_name)
        cursor.execute("""REPLACE INTO guild_members SET char_id = %s, guild_id = 1, rank = 0, public_note = ''""" % char_id)
        log('Finished updating char data for %s' % char_name)

    # Exit
    db.commit()
    cursor.close()    
    db.close()
    log('Exiting.')
