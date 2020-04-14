# src/models/TodoModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class TodoModel(db.Model):
    """
    Todo Model
    """

    __tablename__ = "MTGCards"

    # arena_id
    # mtgo_id
    # mtgo_foil_id
    # all_parts
    # card_faces - ARRAY of JSON
    # color_indicator
    # hand_modifier
    # life_modifier
    # loyalty
    # flavor_text
    # frame_effects
    # printed_name
    # printed_text
    # printed_type_line
    # promo_types
    # variation_of
    # watermark
    # preview.previewed_at
    # preview.source_uri
    # preview.source

    _id= db.Column(db.String(128)),
    
    scryfall_id= db.Column(db.String(128)),

    # CARDS CAN BE REPRINTED, THIS ID IS REPRESENTS THE REFERENCE FOR THE RULES
    oracle_id= db.Column(db.String(128)),
    # TODO: NEED TO RESEARCH WHAT THIS ACTUALLY IS
    multiverse_ids= db.Column(db.ARRAY(db.Integer)),
    # ID FROM TCG PLAYER - IT IS AN ONLINE STORe
    tcgplayer_id= db.Column(db.Integer),
    # GOTTA DO MAGIC TRIVIA=
    #     - longest name
    #     - character restriction
    name= db.Column(db.String(128)),
    # THESE WILL ALWAYS BE A LIMITED LIST
    lang= db.Column(db.String(128)),
    # TODO: CHECK - PRETTY SURE ITS A RELEASE DAYE
    released_at= db.Column(db.String(128)),
    # URI TO API VIEW OF CARD (named "uri")
    scryfall_uri= db.Column(db.String(256)),
    # URI TO WEB VIEW OF CARD (named "scryfall_uri")                
    scryfall_web_uri= db.Column(db.String(256)),
    # DIFFERENT CARDS ACROSS THE YEARS HAD HAD DIFFERENT CARD LAYOUT
    layout= db.Column(db.String(128)),
    # IN REFERENCE TO SCRYFALL
    highres_image= db.Column(db.Boolean),
    # JSON WITH URIS TO SCRYFALL'S CARD IMAGE DB
    #     {
    #     "small": "https://img.scryfall.com/cards/small/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "normal": "https://img.scryfall.com/cards/normal/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "large": "https://img.scryfall.com/cards/large/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "png": "https://img.scryfall.com/cards/png/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.png?1562910357",
    #     "art_crop": "https://img.scryfall.com/cards/art_crop/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357",
    #     "border_crop": "https://img.scryfall.com/cards/border_crop/front/4/1/41193ef1-1619-4448-9905-26b05079c79a.jpg?1562910357"
    #   }
    image_uris= db.Column(db.JSON), 
    # THE MANA COST REPRESENTED ON THE CARD
    mana_cost= db.Column(db.String(128)),
    # THE TOTAL NUMERIC BALUE OF MANA COST REQUIRE TO CAST THE CARD
    cmc= db.Column(db.Integer),
    # TYPE OF THE CARD
    type_line= db.Column(db.String(128)),
    # WHAT THE CARD ACTUALLY SAYS IT DOES
    oracle_text= db.Column(db.String(256)),
    # IF CREATURE OR RELATED - ATTACK POWER
    # this will mostly be used as interget but it can take "*" and other values
    power= db.Column(db.String(128)),  
    # IF CREATURE OR RELATED - DEFENSE
    # this will mostly be used as interget but it can take "*" and other value               
    toughness= db.Column(db.String(128)),
    # WWHAT COLORS APEAR IN THE MANA COST
    colors= db.Column(db.ARRAY(db.String(128))),
    # WHAT COLORS (BESIDES REMINDER TEXT) APPEAR IN THE CARD NAME AND ORACLE TEXT - RELEVANT FOR FORMAT COMMANDER, BRAWL, TINY LEADERS
    color_identity= db.Column(db.ARRAY(db.String(128))),
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
    legalities=  db.Column(db.JSON),   
    # EITHER PAPER, DIGITAL?                                    
    games= db.Column(db.ARRAY(db.String(128))),
    # IF IT BELONGS TO THE RESERVE LIST
    reserved= db.Column(db.Boolean),
    # IF A FOIL VERSION OF THIS CARD EXIST
    foil= db.Column(db.Boolean),
    # IF A NON-FOIL VERSION OF THIS CARD EXIST
    nonfoil= db.Column(db.Boolean),
    # IF AN OVERSIZE VERSON OD TIS CARD EXIST
    oversized= db.Column(db.Boolean),
    # IF A PROMO VERSION OF THIS CARD EXIST
    promo= db.Column(db.Boolean),
    # IF THE CARD IS A REPRINT
    reprint= db.Column(db.Boolean),
    #TODO: NEED TO CHECK
    variation= db.Column(db.Boolean),
    # scryfall calls it "set". WHAT SET DOES THE CARD BELONG TO, USUALLY HAS 3 LETTERS
    card_set= db.Column(db.String(128)),
    # SET'S NAME                                   
    set_name= db.Column(db.String(128)),
    # SET'S TYPE
    set_type= db.Column(db.String(128)),
    # SET'S SCRYFALL URI LOCATION
    set_uri= db.Column(db.String(256)),
    # TODO: CHECK
    set_search_uri= db.Column(db.String(256)),
    # TODO: CHECK
    scryfall_set_uri= db.Column(db.String(256)),
    # TODO: CHECK
    rulings_uri= db.Column(db.String(256)),
    # TODO: CHECK
    prints_search_uri= db.Column(db.String(256)),
    # TODO: CHECK
    collector_number= db.Column(db.String(128)),
    # TODO: CHECK
    digital= db.Column(db.Boolean),
    # WHAT IS THE RARITY OF THE CARD FROM A SET LIST
    rarity= db.Column(db.String(128)),
    # TODO: CHECK
    card_back_id= db.Column(db.String(128)),                          #GUID
    # TODO: CHECK.  PROBABLY THE NAME
    artist= db.Column(db.String(128)),
    # UNIQUE IDENTIFIERS IF MULTIPLE ARTIST
    artist_ids= db.Column(db.ARRAY(db.String(128))),                  #GUIDs need a separate table for artis
    # UNIQUE IDENTIFIER TO THE IMAGE # TODO: CHECK WHO ASSIGNS IT
    illustration_id= db.Column(db.ARRAY(db.String(128))),             #GUIDs need a separate table for artis
    # WHAT BORDER COLOR DOES IT HAVE FROM A SET LIST
    border_color= db.Column(db.String(128)),
    # HWAT TYPE OF FRAME THE CARD HAS (BECAME MORE RELEVANT IN RECENT YEARS)
    frame= db.Column(db.String(128)),
    # IF THERE IS A FULL ART VEERSION
    full_art= db.Column(db.Boolean),
    # IF THERE IS A TEXTLESS VERSION
    textless= db.Column(db.Boolean),
    # IF IT COMES OUT OF A BOOSTER PACK
    booster= db.Column(db.Boolean),
    # IDK WHERE THEY GET THIS INFO # TODO: CHECK
    story_spotlight= db.Column(db.Boolean),
    # TODO: CHECK
    edhrec_rank= db.Column(db.Integer),
    # CARD PRICES  FETCHED DAILY
    prices= db.Column(db.JSON),
    # LINK TO OTHER RESOURCES
    related_uris=  db.Column(db.JSON),
    # LINK TO SELLERS                   
    purchase_uris= db.Column(db.JSON),                    

    def __init__(self, data):

        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_cards(all_args):
    # if 'title' in all_args:
    #   return TodoModel.query.filter(TodoModel.title == all_args.get('title'))
        return TodoModel.query.all()

    @staticmethod
    def get_one_card(id):
        return TodoModel.query.get(id)

    def __repr__(self):
        return '{0},{1},{2}'.format(self.name, self.cardset, self.color)

class TodoSchema(Schema):
    """
    MTG Schema
    """
    
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
