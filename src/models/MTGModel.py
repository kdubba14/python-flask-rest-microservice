# src/models/MTGModel.py
from . import db
import datetime
import threading
import json
import os
import uuid
# from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

session_count = 0

def new_session_scope():
    global session_count
    session_count += 1
    return f'{session_count}'


class MTGModel(db.Model):
    """
    MTG Model
    """
    __tablename__ = "mtg_cards"

    mtg_id = db.Column(db.String(128), primary_key=True)
    scryfall_id = db.Column(db.String(128))
    # CARDS CAN BE REPRINTED, THIS ID IS REPRESENTS THE REFERENCE FOR THE RULES
    oracle_id = db.Column(db.String(128))
    # TODO: NEED TO RESEARCH WHAT THIS ACTUALLY IS
    multiverse_ids = db.Column(db.ARRAY(db.Integer))
    # NOT ALWAYS PRESENT
    arena_id = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    mtgo_id = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    mtgo_foil_id = db.Column(db.String(128))
    # ID FROM TCG PLAYER - IT IS AN ONLINE STORe
    tcgplayer_id = db.Column(db.String(128))
    # GOTTA DO MAGIC TRIVIA=
    #     - longest name
    #     - character restriction
    name = db.Column(db.String(128))
    # THESE WILL ALWAYS BE A LIMITED LIST
    lang = db.Column(db.String(128))
    # TODO: CHECK - PRETTY SURE ITS A RELEASE DAYE
    released_at = db.Column(db.String(128))
    # URI TO API VIEW OF CARD (named "uri")
    scryfall_api_uri = db.Column(db.String(256))
    # URI TO WEB VIEW OF CARD (named "scryfall_uri")                
    scryfall_web_uri = db.Column(db.String(256))
    # DIFFERENT CARDS ACROSS THE YEARS HAD HAD DIFFERENT CARD LAYOUT
    layout = db.Column(db.String(128))
    # IN REFERENCE TO SCRYFALL
    highres_image = db.Column(db.Boolean)
    # JSON WITH URIS TO SCRYFALL'S CARD IMAGE DB
    #     {
    #     "small": "https://img.scryfall.com/cards/small/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "normal": "https://img.scryfall.com/cards/normal/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "large": "https://img.scryfall.com/cards/large/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "png": "https://img.scryfall.com/cards/png/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.png?1562910357",
    #     "art_crop": "https://img.scryfall.com/cards/art_crop/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "border_crop": "https://img.scryfall.com/cards/border_crop/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357"
    #   }
    image_uris = db.Column(db.JSON)
    # THE MANA COST REPRESENTED ON THE CARD
    mana_cost = db.Column(db.String(128))
    # THE TOTAL NUMERIC BALUE OF MANA COST REQUIRE TO CAST THE CARD
    cmc= db.Column(db.Integer)
    # TYPE OF THE CARD
    type_line= db.Column(db.String(128))
    # WHAT THE CARD ACTUALLY SAYS IT DOES
    oracle_text= db.Column(db.String(256))
    # IF CREATURE OR RELATED - ATTACK POWER
    # this will mostly be used as interget but it can take "*" and other values
    power= db.Column(db.String(128))
    # IF CREATURE OR RELATED - DEFENSE
    # this will mostly be used as interget but it can take "*" and other value               
    toughness= db.Column(db.String(128))
    # WWHAT COLORS APEAR IN THE MANA COST
    colors = db.Column(db.ARRAY(db.String(128)))
    # WWHAT COLORS APEAR IN THE MANA COST
    color_indicator = db.Column(db.ARRAY(db.String(128)))
    # WHAT COLORS (BESIDES REMINDER TEXT) APPEAR IN THE CARD NAME AND ORACLE TEXT - RELEVANT FOR FORMAT COMMANDER, BRAWL, TINY LEADERS
    color_identity= db.Column(db.ARRAY(db.String(128)))
    # WHAT FORMATS THE CARD CAN BE PLAYED
    # OBJECT WITH LEGALITIES
    # {
    #   "standard": "not_legal",
    #   "future": "not_legal",
    #   "historic": "not_legal",
    #   "pioneer": "legal",
    #   "modern": "legal",
    #   "legacy": "legal",
    #   "pauper": "not_legal",
    #   "vintage": "legal",
    #   "penny": "not_legal",
    #   "commander": "legal",
    #   "brawl": "not_legal",
    #   "duel": "legal",
    #   "oldschool": "not_legal"
    # }
    legalities=  db.Column(db.JSON)
    # NOT ALWAYS PRESENT
    all_parts =  db.Column(db.JSON)
    # NOT ALWAYS PRESENT
    card_faces =  db.Column(db.JSON)
    # NOT ALWAYS PRESENT
    flavor_text = db.Column(db.String(512))
    # NOT ALWAYS PRESENT
    frame_effects = db.Column(db.ARRAY(db.String(128)))
    # NOT ALWAYS PRESENT
    promo_types = db.Column(db.ARRAY(db.String(128)))
    # NOT ALWAYS PRESENT
    watermark = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    preview = db.Column(db.JSON)
    # NOT ALWAYS PRESENT
    hand_modifier = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    life_modifier = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    loyalty = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    printed_name = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    printed_text = db.Column(db.String(256))
    # NOT ALWAYS PRESENT
    printed_type_line = db.Column(db.String(128))
    # NOT ALWAYS PRESENT
    variation_of = db.Column(db.String(128))
    # EITHER PAPER, DIGITAL?                                    
    games = db.Column(db.ARRAY(db.String(128)))
    # IF IT BELONGS TO THE RESERVE LIST
    reserved = db.Column(db.Boolean)
    # IF A FOIL VERSION OF THIS CARD EXIST
    foil = db.Column(db.Boolean)
    # IF A NON-FOIL VERSION OF THIS CARD EXIST
    nonfoil = db.Column(db.Boolean)
    # IF AN OVERSIZE VERSON OD TIS CARD EXIST
    oversized = db.Column(db.Boolean)
    # IF A PROMO VERSION OF THIS CARD EXIST
    promo = db.Column(db.Boolean)
    # IF THE CARD IS A REPRINT
    reprint = db.Column(db.Boolean)
    #TODO: NEED TO CHECK
    variation = db.Column(db.Boolean)
    # scryfall calls it "set". WHAT SET DOES THE CARD BELONG TO, USUALLY HAS 3 LETTERS
    card_set = db.Column(db.String(128))
    # SET'S NAME                                   
    set_name = db.Column(db.String(128))
    # SET'S TYPE
    set_type = db.Column(db.String(128))
    # SET'S SCRYFALL URI LOCATION
    set_uri = db.Column(db.String(256))
    # TODO: CHECK
    set_search_uri = db.Column(db.String(256))
    # TODO: CHECK
    scryfall_set_uri = db.Column(db.String(256))
    # TODO: CHECK
    rulings_uri = db.Column(db.String(256))
    # TODO: CHECK
    prints_search_uri = db.Column(db.String(256))
    # TODO: CHECK
    collector_number = db.Column(db.String(128))
    # TODO: CHECK
    digital = db.Column(db.Boolean)
    # WHAT IS THE RARITY OF THE CARD FROM A SET LIST
    rarity = db.Column(db.String(128))
    # TODO: CHECK
    card_back_id = db.Column(db.String(128))                           #GUID
    # TODO: CHECK.  PROBABLY THE NAME
    artist = db.Column(db.String(128))
    # UNIQUE IDENTIFIERS IF MULTIPLE ARTIST
    artist_ids = db.Column(db.ARRAY(db.String(128)))                   #GUIDs need a separate table for artis
    # UNIQUE IDENTIFIER TO THE IMAGE # TODO: CHECK WHO ASSIGNS IT
    illustration_id = db.Column(db.ARRAY(db.String(128)))              #GUIDs need a separate table for artis // THIS SHOULD BE A STRING NOT STRING[]
    # WHAT BORDER COLOR DOES IT HAVE FROM A SET LIST
    border_color = db.Column(db.String(128))
    # HWAT TYPE OF FRAME THE CARD HAS (BECAME MORE RELEVANT IN RECENT YEARS)
    frame = db.Column(db.String(128))
    # IF THERE IS A FULL ART VEERSION
    full_art = db.Column(db.Boolean)
    # IF THERE IS A TEXTLESS VERSION
    textless = db.Column(db.Boolean)
    # IF IT COMES OUT OF A BOOSTER PACK
    booster = db.Column(db.Boolean)
    # IDK WHERE THEY GET THIS INFO # TODO: CHECK
    story_spotlight = db.Column(db.Boolean)
    # TODO: CHECK
    edhrec_rank = db.Column(db.Integer)
    # CARD PRICES  FETCHED DAILY
    prices = db.Column(db.JSON)
    # LINK TO OTHER RESOURCES
    related_uris =  db.Column(db.JSON)
    # LINK TO SELLERS                   
    purchase_uris = db.Column(db.JSON)                 

    def __init__(self, data):
        self.mtg_id = data.get('mtg_id')
        self.scryfall_id = data.get('scryfall_id')
        self.oracle_id = data.get('oracle_id')
        self.multiverse_ids = data.get('multiverse_ids')
        self.arena_id = data.get('arena_id')
        self.mtgo_id = data.get('mtgo_id')
        self.mtgo_foil_id = data.get('mtgo_foil_id')
        self.tcgplayer_id = data.get('tcgplayer_id')
        self.name = data.get('name')
        self.lang = data.get('lang')
        self.released_at = data.get('released_at')
        self.scryfall_api_uri = data.get('scryfall_api_uri')
        self.scryfall_web_uri = data.get('scryfall_web_uri')
        self.layout = data.get('layout')
        self.highres_image = data.get('highres_image')
        self.image_uris = data.get('image_uris')
        self.mana_cost = data.get('mana_cost')
        self.cmc = data.get('cmc')
        self.type_line = data.get('type_line')
        self.oracle_text = data.get('oracle_text')
        self.power = data.get('power')
        self.toughness = data.get('toughness')
        self.colors = data.get('colors')
        self.color_indicator = data.get('color_indicator')
        self.color_identity = data.get('color_identity')
        self.legalities = data.get('legalities')
        self.all_parts = data.get('all_parts')
        self.card_faces = data.get('card_faces')
        self.flavor_text = data.get('flavor_text')
        self.frame_effects = data.get('frame_effects')
        self.promo_types = data.get('promo_types')
        self.watermark = data.get('watermark')
        self.preview = data.get('preview')
        self.hand_modifier = data.get('hand_modifier')
        self.life_modifier = data.get('life_modifier')
        self.loyalty = data.get('loyalty')
        self.printed_name = data.get('printed_name')
        self.printed_text = data.get('printed_text')
        self.printed_type_line = data.get('printed_type_line')
        self.variation_of = data.get('variation_of')
        self.games = data.get('games')
        self.reserved = data.get('reserved')
        self.foil = data.get('foil')
        self.nonfoil = data.get('nonfoil')
        self.oversized = data.get('oversized')
        self.promo = data.get('promo')
        self.reprint = data.get('reprint')
        self.variation = data.get('variation')
        self.card_set = data.get('card_set')
        self.set_name = data.get('set_name')
        self.set_type = data.get('set_type')
        self.set_uri = data.get('set_uri')
        self.set_search_uri = data.get('set_search_uri')
        self.scryfall_set_uri = data.get('scryfall_set_uri')
        self.rulings_uri = data.get('rulings_uri')
        self.prints_search_uri = data.get('prints_search_uri')
        self.collector_number = data.get('collector_number')
        self.digital = data.get('digital')
        self.rarity = data.get('rarity')
        self.card_back_id = data.get('card_back_id')
        self.artist = data.get('artist')
        self.artist_ids = data.get('artist_ids')
        self.illustration_id = data.get('illustration_id').join('')
        self.border_color = data.get('border_color')
        self.frame = data.get('frame')
        self.full_art = data.get('full_art')
        self.textless = data.get('textless')
        self.booster = data.get('booster')
        self.story_spotlight = data.get('story_spotlight')
        self.edhrec_rank = data.get('edhrec_rank')
        self.prices = data.get('prices')
        self.related_uris = data.get('related_uris')
        self.purchase_uris = data.get('purchase_uris')

        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def serialize(self):
        mtg_schema = MTGSchema()
        dumped_value = mtg_schema.dump(self)
        dumped_value['illustration_id'] = ''.join(dumped_value['illustration_id'])
        return dumped_value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def create(self, data):
        total_cards = [[]]
        for card_info in data['cards']:
            new_card = MTGModel({
                'mtg_id': str(uuid.uuid4()),
                'scryfall_id': card_info.get('id'),
                'oracle_id': card_info.get('oracle_id'),
                'multiverse_ids': card_info.get('multiverse_ids'),
                'arena_id': card_info.get('arena_id'),
                'mtgo_id': card_info.get('mtgo_id'),
                'mtgo_foil_id': card_info.get('mtgo_foil_id'),
                'tcgplayer_id': card_info.get('tcgplayer_id'),
                'name': card_info.get('name'),
                'lang': card_info.get('lang'),
                'released_at': card_info.get('released_at'),
                'scryfall_api_uri': card_info.get('uri'),
                'scryfall_web_uri': card_info.get('scryfall_uri'),
                'layout': card_info.get('layout'),
                'highres_image': card_info.get('highres_image'),
                'image_uris': card_info.get('image_uris'),
                'mana_cost': card_info.get('mana_cost'),
                'cmc': card_info.get('cmc'),
                'type_line': card_info.get('type_line'),
                'oracle_text': card_info.get('oracle_text'),
                'power': card_info.get('power'),
                'toughness': card_info.get('toughness'),
                'colors': card_info.get('colors'),
                'color_indicator': card_info.get('color_indicator'),
                'color_identity': card_info.get('color_identity'),
                'legalities': card_info.get('legalities'),
                'all_parts': card_info.get('all_parts'),
                'card_faces': card_info.get('card_faces'),
                'flavor_text': card_info.get('flavor_text'),
                'frame_effects': card_info.get('frame_effects'),
                'promo_types': card_info.get('promo_types'),
                'watermark': card_info.get('watermark'),
                'preview': card_info.get('preview'),
                'hand_modifier': card_info.get('hand_modifier'),
                'life_modifier': card_info.get('life_modifier'),
                'loyalty': card_info.get('loyalty'),
                'printed_name': card_info.get('printed_name'),
                'printed_text': card_info.get('printed_text'),
                'printed_type_line': card_info.get('printed_type_line'),
                'variation_of': card_info.get('variation_of'),
                'games': card_info.get('games'),
                'reserved': card_info.get('reserved'),
                'foil': card_info.get('foil'),
                'nonfoil': card_info.get('nonfoil'),
                'oversized': card_info.get('oversized'),
                'promo': card_info.get('promo'),
                'reprint': card_info.get('reprint'),
                'variation': card_info.get('variation'),
                'card_set': card_info.get('set'),
                'set_name': card_info.get('set_name'),
                'set_type': card_info.get('set_type'),
                'set_uri': card_info.get('set_uri'),
                'set_search_uri': card_info.get('set_search_uri'),
                'scryfall_set_uri': card_info.get('scryfall_set_uri'),
                'rulings_uri': card_info.get('rulings_uri'),
                'prints_search_uri': card_info.get('prints_search_uri'),
                'collector_number': card_info.get('collector_number'),
                'digital': card_info.get('digital'),
                'rarity': card_info.get('rarity'),
                'card_back_id': card_info.get('card_back_id'),
                'artist': card_info.get('artist'),
                'artist_ids': card_info.get('artist_ids'),
                'illustration_id': card_info.get('illustration_id'),
                'border_color': card_info.get('border_color'),
                'frame': card_info.get('frame'),
                'full_art': card_info.get('full_art'),
                'textless': card_info.get('textless'),
                'booster': card_info.get('booster'),
                'story_spotlight': card_info.get('story_spotlight'),
                'edhrec_rank': card_info.get('edhrec_rank'),
                'prices': card_info.get('prices'),
                'related_uris': card_info.get('related_uris'),
                'purchase_uris': card_info.get('purchase_uris'),
            })
            
            
            if len(total_cards[-1]) >= 50:
                total_cards.append([])
            total_cards[-1].append(new_card)

        print(data['cards'][0])
        groups = [total_cards[x:x+10] for x in range(0, len(total_cards), 10)]
        print('+++++++++++++++++ There are', len(groups), 'groups of 10 chunks to be processed.... +++++++++++++++++\n')

        # def add_chunk(chunk):
        #     print(chunk)
        #     try:
        #         new_session = db.create_scoped_session({'scopeFunc': new_session_scope})
        #         print(1)
        #         new_session.add_all(chunk)
        #         print(2)
        #         new_session.commit()
        #         print(3)
        #         new_session.remove()
        #         print(f'ADDED CHUNK TO DB')
        #     except:
        #         print('========AN ERROR OCCURRED======')
        #         os._exit(1)

        for i in range(len(groups)):
            for idx in range(len(groups[i])):
                if i > 395:
                    try:
                        db.session.add_all(groups[i][idx])
                        print(f'ADDED CHUNK {idx+1} OF {len(groups[i])} TO DB')
                    except:
                        print('========AN ERROR OCCURRED======')
                        os._exit(1)
                    db.session.commit()

            print(f'ADDED {i+1} GROUPS OUT OF {len(groups)}')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_cards(all_args):
        all_cards = [z.serialize() for z in MTGModel.query.limit(50).all()]
        return all_cards

    @staticmethod
    def get_one_card(id):
        return MTGModel.query.get(id)

    def __repr__(self):
        return '{0}'.format(self.name)

    def __iter__(self):
        return vars(self)

class MTGSchema(SQLAlchemyAutoSchema):
    """
    MTG Schema
    """
    class Meta:
        model = MTGModel
        include_relationships = True
        load_instance = True
