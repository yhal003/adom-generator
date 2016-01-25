MALE = "Male"
FEMALE = "Female"

def pick_sex(s):
    sexes = {"Male":"m", "Female":"f"}
    return sexes[s]


CL_FIGHTER =  "Fighter"
CL_PALADIN = "Paladin"
CL_RANGER = "Ranger"
CL_THIEF  = "Thief"
CL_ASSASSIN  = "Assassin"
CL_WIZARD = "Wizard"
CL_PRIEST= "Priest"
CL_BARD= "Bard"
CL_MONK= "Monk"
CL_HEALER= "Healer"
CL_WEAPONSMITH= "Weaponsmith"
CL_ARCHER= "Archer"
CL_MERCHANT= "Merchant"
CL_FARMER= "Farmer"
CL_MINDCRAFTER = "Mindcrafter"
CL_BARBARIAN  = "Barbarian"
CL_DRUID = "Druid"
CL_NECROMANCER = "Necromancer"
CL_ELEMENTALIST = "Elementalist"
CL_BEASTFIGHTER = "Beastfighter"
CL_CHAOS_KNIGHT = "Chaos Knight"
CL_DUELIST = "Duelist"


def pick_class(c):
    classes = {"Fighter":"a",
               "Paladin":"b",
               "Ranger":"c",
               "Thief":"d",
               "Assassin":"e",
               "Wizard":"f",                                                                      
               "Priest":"g",
               "Bard":"h",
               "Monk":"i",
               "Healer":"j",
               "Weaponsmith":"k",
               "Archer":"l",
               "Merchant":"m",
               "Farmer":"n",
               "Mindcrafter":"o",                                                                 
               "Barbarian":"p",
               "Druid":"q",
               "Necromancer":"r",                                                                 
               "Elementalist":"s",
               "Beastfighter":"b",
               "Chaos Knight":"u",                                                                
               "Duelist":"v"
           }
    
    return classes[c]

R_HUMAN     = "Human"
R_TROLL     = "Troll"
R_HIGH_ELF  = "High Elf"
R_GRAY_ELF  = "Gray Elf"
R_DARK_ELF  = "Dark Elf"
R_DWARF     = "Dwarf"
R_GNOME     = "Gnome"
R_HURTLING  = "Hurtling"
R_ORC       = "Orc"
R_DRAKELING = "Drakeling"
R_MIST_ELF  = "Mist Elf"
R_RATLING   = "Ratling"


def pick_race(r):
    races = {"Human":"a", 
             "Troll":"b",
             "High Elf":"c",
             "Gray Elf":"d",
             "Dark Elf":"e",
             "Dwarf":"f",
             "Gnome":"g",
             "Hurtling":"h",
             "Orc":"i",
             "Drakeling":"j",
             "Mist Elf":"k",
             "Ratling":"l"
    }
    return races[r]


# corruptions 

COR_POISON_HANDS = "Poison drips from your hands"
COR_MANA_BATTERY = "You are a living mana battery"
COR_UNHOLY_AURA  = "You are surrounded by an unholy aura"
COR_EXHALE_SULFUR = "You exhale sulphur"
COR_THIN_NIMBLE = "You have become extremely thin and nimble"
COR_VERY_LIGHT = "You have become very light"
COR_BULGING_CRANIUM = "You have grown a bulging cranium"
COR_EXTRA_EYES = "You have grown 10 extra eyes"
COR_GROWN_HORNS = "You have grown horns"
COR_GROWN_THORNS = "You have grown thorns"
COR_SOMEWHAT_APISH = "You look somewhat apish"
COR_YOU_RAGE = "You rage"
COR_GROWN_ANTENNAE = "Your antennae explore the details of your environment" 
COR_ASTRAL_SPACE = "Your close attunement to corrupted astral space allows teleportation"
COR_CORRUPTED_TISSUE = "Your corrupted tissue seems to heal much faster"
COR_FEET_HOOVES = "Your feet have been transformed into hooves"
COR_STIFF_MUSCLES = "Your muscles have stiffened slowing you down"
COR_TOUGH_SCALES = "Your skin is covered by tough scales"
COR_CHAOS_WHISPERS = "The voice of ChAoS whispers disturbing secrets into your thoughts"
COR_ATTACHED_CHAOS = "You are attached to ChAoS corrupting your foes"
COR_BLOT_SUN = "You hate the sun and try to blot it"
COR_BABBLING_MOUTH = "You sport a babbling mouth on your forehead that rants and raves dark secrets"
COR_GROWN_GILLS = "You sport gills"
COR_SWEAT_BLOOD = "You sweat blood"
COR_ORDER_FLESH = "You thrive on the flesh of Order"
COR_DECAY_TISSUES = "Your bodily tissues seem to be in a state of decay requiring a lot of will  to stay up"
COR_COLD_BLOOD = "Your blood is freezing cold"
COR_ACID_BLOOD = "Your blood turned to acid"
COR_BRONZE_BONES = "Your bones are made from bronze"
COR_CHAOS_MIST = "Your eyes are shrouded by the mists of ChAoS"
COR_MERGE_EYES = "Your frontal eyes have merged to form one larger eye"
COR_BLACK_EYES = "Your eye(s) turned black"
COR_DISEASE_MAGGOTS = "Your flesh continually spouts disease-ridden maggots"
COR_FRAGILE_STILTS = "Your legs have stretched into long, fragile stilts"
COR_TENTACLE_MOUTH = "Your mouth has turned into a writhing mass of prehensile tentacles"

CORRUPTIONS = [COR_POISON_HANDS,COR_MANA_BATTERY,COR_UNHOLY_AURA,COR_EXHALE_SULFUR,
               COR_THIN_NIMBLE,COR_VERY_LIGHT,COR_BULGING_CRANIUM,COR_EXTRA_EYES,COR_GROWN_HORNS,
               COR_GROWN_THORNS,COR_SOMEWHAT_APISH,COR_YOU_RAGE,COR_GROWN_ANTENNAE, COR_ASTRAL_SPACE,
               COR_CORRUPTED_TISSUE,COR_FEET_HOOVES,COR_STIFF_MUSCLES,COR_TOUGH_SCALES,
               COR_CHAOS_WHISPERS,COR_ATTACHED_CHAOS,COR_BLOT_SUN,COR_BABBLING_MOUTH ,
               COR_GROWN_GILLS,COR_SWEAT_BLOOD,COR_ORDER_FLESH,COR_DECAY_TISSUES ,
               COR_COLD_BLOOD,COR_ACID_BLOOD,COR_BRONZE_BONES,COR_CHAOS_MIST,
               COR_MERGE_EYES,COR_BLACK_EYES,COR_DISEASE_MAGGOTS,COR_FRAGILE_STILTS,COR_TENTACLE_MOUTH
]


# talents

T_ALERT = "Alert"
T_MISER = "Miser"
T_TREASURE_HUNTER = "Treasure Hunter"
T_BOON_TO_FAMILY = "Boon to the Family"
T_CHARMING = "Charming"
T_HEIR = "Heir"
T_HARDY = "Hardy"
T_TOUGH_SKIN = "Tough Skin"
T_WEALTHY = "Wealthy"
T_VERY_WEALTHY = "Very Wealthy"
T_FILTHY_RICH = "Filthy Rich"
T_SIX_SENSE = "Six Sense"


# items
# ',(}/]{=\!?"%$*
ITEM_AMULET = "'"
ITEM_WEAPON = "("
ITEM_MISSLE_WEAPON = "{"
ITEM_ARMOR = "["
ITEM_TOOL = "]"
ITEM_RING = "="
ITEM_BOOK = "\""
ITEM_FOOD = "%"
ITEM_POTION = "!"
ITEM_SCROLL = "?"
ITEM_WAND = "\\"



