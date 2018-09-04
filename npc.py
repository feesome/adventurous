import items


class NonPlayableCharacters():
    def __init__(self):
        raise NotImplementedError('Do not create raw NPC objects.')

    def __str__(self):
        return self.name


class Trader(NonPlayableCharacters):
    def __init__(self):
        self.name = 'Trader'
        self.gold = 100
        self.inventory = [items.Herbs(),
                          items.Herbs(),
                          items.Herbs(),
                          items.Medipack(),
                          items.Medipack(),
                          items.HolyWater(),
                          ]
