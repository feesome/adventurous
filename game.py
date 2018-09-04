''' My first text adventure '''

from collections import OrderedDict
from player import Player
import world


def play():
    print('The Mansion.')
    world.parse_world_dsl()
    player = Player()

    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)  # which tile
        print(room.intro_text())
        room.modify_player(player)  # what the room does to the player
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!\n"
                  "YOU  ARE  DEAD.")


# Get the possible actions for the player, depending on what map_tile he's on,
# the status of his healf of the items in his inventory.

def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
    if player.inventory:  # same as: "if player.inventory != []" (is not empty)
        action_adder(actions, 'i', player.print_inventory, "Print inventory")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, (world.EnemyTile, world.BossTile)) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    # if isinstance(room, (world.InstantDeathTile, world.BossTile)):
    #     action_adder(actions, 'u', player.use_item, "Use item")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Go north")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go south")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go east")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go west")
    if player.hp < 100:
        action_adder(actions, 'h', player.heal, "Heal")

    return actions

# There’s a very important syntax difference here that is easy to miss:
# We do not write player.print_inventory(), we write player.print_inventory.
# As we’ve seen before, my_function() is the syntax to execute a function.
# If instead we just want to refer to the function, we use the function name
# without (). This is important because we don’t want to do the actions
# right now, we just want to store the possible actions in the dictionary.


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print('Invalid action!')


play()
