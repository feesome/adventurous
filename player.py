import items
import world


class Player:
    def __init__(self):
        self.inventory = [items.Brick(),
                          items.Knife(),
                          items.Sword(),
                          items.Medipack(),
                          items.Herbs(),
                          ]

        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print('Inventory:')
        for item in self.inventory:
            print('- ' + str(item))
        print('Gold: {}'.format(self.gold))

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:  # same as: if consumables == []
            print("You don't have any items to heal you!")
            return

        for i, item in enumerate(consumables, 1):
            #print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))

        valid = False
        while not valid:
            print("Choose an item to use to heal: ")
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Current HP: {}".format(self.hp))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again!")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        # if isinstance(room, world.BossTile):
        #     best_weapon = items.HolyWater()
        #     best_weapon.damage = 50
        #     print('The bottle of Holy Water is glowing bright blue.')

        print('You use {} against {}!'.format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print('You killed the {}!'.format(enemy.name))
        else:
            print('{} HP is {}.'.format(enemy.name, enemy.hp))

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)

    # def use_item(self):
    #     room = world.tile_at(self.x, self.y)
    #     tools = [item for item in self.inventory
    #              if isinstance(item, items.Tool)]
    #     if not tools:
    #         print("You don't carry anything you could use right now.")
    #         return
    #
    #     for i, item in enumerate(tools, 1):
    #         print('{}. {}'.format(i, item))
    #
    #     valid = False
    #     while not valid:
    #         print("Choose an item to use: ")
    #         choice = input("")
    #         try:
    #             to_use = tools[int(choice) - 1]  # coz py-list starts at 0
    #             print(to_use)
    #             if isinstance(room, world.BossTile) and to_use == 'HolyWater':
    #                 use_on = room.enemy
    #                 to_use.damage = 50
    #                 return
    #             elif isinstance(room, world.InstantDeathTile) and to_use == 'Lockpick':
    #                 print("You use the {} to unlock the door.".format(item))
    #             valid = True
    #         except (ValueError, IndexError):
    #             print("You can't use this right now!")
