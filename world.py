''' The World we live in. '''

import random
import enemies
import npc
import player


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError('Create a subclass instead!')

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return '''
        As you awake, you find yourself lying in the dark.
        You realize, that you are inside of some box.
        As you push with your hands against the top part, the lid opens.
        You are inside a coffin, which is displayed in the center of a small
        room. Candles are burning in two corners.
        There is an iron door to the south.
        '''


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                "it's web in front of you!"
            self.dead_text = "The remains of a dead spider rot on the ground."
        elif r < 0.80:
            self.enemy = enemies.Skeleton()
            self.alive_text = "You hear the clattering of bones." \
                "A skeleton steps out of the dark, slowly moving towards you!"
            self.dead_text = "A pile of bones lies on the ground."
        elif r < 0.70:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking nois growing louder" \
                "...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        elif r < 0.98:
            self.enemy = enemies.Gravedigger()
            self.alive_text = "An angry looking gravedigger armed with a "\
                "shovel blocks your way!"
            self.dead_text = "A dead gravedigger reminds you of your triumph."

        super().__init__(x, y)

    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

    def modify_player(self, player):  # reduces the players hp
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print('{} does {} damage. You have {} HP remaining.'.
                  format(self.enemy.name, self.enemy.damage, player.hp))


class BossTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Priest()
        self.alive_text = '''
        You see the shape of a person standing on the opposite side of the room.
        As you move closer, you recognize him as a priest.
        He turns to look at you - his eyes as black as coal.
        '''
        self.dead_text = "The corpse of the dead priest, lies in his own blood."

        super().__init__(x, y)

    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

    def modify_player(self, player):  # reduces the players hp
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print('{} does {} damage. You have {} HP remaining.'.
                  format(self.enemy.name, self.enemy.damage, player.hp))


class FindGoldTile(MapTile):
    def __init__(self, x, y):  # only the first time u enter the tile
        self.gold = random.randint(1, 50)  # random amount of gold
        self.gold_claimed = False  # Boolean that verifies if it has been picked up
        super().__init__(x, y)

    def modify_player(self, player):  # adds gold to the player
        if not self.gold_claimed:
            self.gold_claimed = True  # next time you enter the tile
            player.gold = player.gold + self.gold
            print("+{} gold added.".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """Nothing special here."""
        else:
            return """ Someone dropped some gold. You pick it up."""


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print('{}. {} - {} Gold'.format(i, item.name, item.value))
        while True:
            user_input = input('Choose an item or press Q to exit: ')
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print('Invalid choice!')

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive.")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print('Trade complete.')

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Take a look at this fine selection: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's what's available to sell:")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")
    # Depending on the player’s choice, the player object is passed to trade()
    # as either the buyer or seller. Named parameters make it clear who is who.

    def intro_text(self):
        return """
        A frail not-quite-human, not-quite-creature squats in the corner,
        clicking his gold coins together.
        He looks willing to trade.
        """


class BoringTile1(MapTile):
    def intro_text(self):
        return '''
        This is a hallway. Nothing special here
        '''


class BoringTile2(MapTile):
    def intro_text(self):
        return '''
        A dark, narrow corridor winds from east to north.
        In the distance you see the fail gloom of light.
        You hear a strange clicking sound...
        '''


class InstantDeathTile(MapTile):

    def modify_player(self, player):  # reduces the players hp to 0 == death
        player.hp = 0

    def intro_text(self):
        return '''
        As you enter the room, you hear the door behind you shut and the sound
        of a key, being turned in the lock. Suddenly the ceiling starts moving
        downwards... there is no way, you can stop it.
        '''


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return '''
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        Victory is yours!
        '''


world_dsl = """
|TT|  |VT|BT|FG|
|B2|EN|  |  |EN|
|  |B1|FG|B1|FG|
|ID|  |B1|  |EN|
|FG|ST|EN|  |FG|
"""


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    # count the number of pipes in each row, and then make sure that
    # every row has the same number of pipes as the first row.
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True


tile_type_dict = {
    'VT': VictoryTile,
    'EN': EnemyTile,
    'ST': StartTile,
    'BT': BossTile,
    'B1': BoringTile1,
    'B2': BoringTile2,
    'FG': FindGoldTile,
    'TT': TraderTile,
    'ID': InstantDeathTile,
    '  ': None,
}

world_map = []
start_tile_location = None


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError('DSL is invalid!')

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]
    # Iterate over each line in the DSL.
    # Instead of i, the variable y is used cause we're working with an X-Y grid.
    for y, dsl_row in enumerate(dsl_lines):
        row = []  # Create an object to store the tiles
        dsl_cells = dsl_row.split('|')  # Split the line into abbreviations.

        # The split method includes the beginning and end of the line
        # so we need to remove those nonexistent cells
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            # Look up the abbreviation in the dictionary
            tile_type = tile_type_dict[dsl_cell]
            # If the dictionary returned a valid type, create
            # a new tile object, pass it the X-Y coordinates
            # as required by the tile __init__(), and add
            # it to the row object. If None was found in the
            # dictionary, we just add None.
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)
        # Add the whole row to the world_map
        world_map.append(row)


def tile_at(x, y):  # determines the current position / tile
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
