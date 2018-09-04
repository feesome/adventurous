import enemies


class Weapon:
    def __init__(self):
        raise NotImplementedError('Do not create raw Weapon objects.')

    def __str__(self):
        return self.name


class Consumable:
    def __init__(self):
        raise NotImplementedError('Do not create raw Consumable objects.')

    def __str__(self):
        return '{} (+{} HP)'.format(self.name, self.healing_value)


class Tool:
    def __init__(self):
        raise NotImplementedError('Do not create raw Tool objects.')

    def __str__(self):
        return self.name


class Lockpick(Tool):
    def __init__(self):
        self.name = 'Lockpick'
        self.description = 'A tool to open small locks.'
        self.use = 'Lock'
        self.value = 10
        # Spezielle eigensch. an speziellem ort?


class HolyWater(Consumable):
    def __init__(self):
        self.name = 'Holy Water'
        self.description = 'A small bottle of Holy Water.'
        self.damage = 50
        self.healing_value = 10
        self.value = 60


class Brick(Weapon):
    def __init__(self):
        self.name = 'Brick'
        self.description = 'A clay brick, suitable for bludgeoning.'
        self.damage = 5
        self.value = 1


class Knife(Weapon):
    def __init__(self):
        self.name = 'Knife'
        self.description = 'A sharp combat knife.'\
            'Somewhat better than a rock.'
        self.damage = 10
        self.value = 20


class Sword(Weapon):
    def __init__(self):
        self.name = 'Sword'
        self.description = 'This Sword has been displayed as a wall decorator.'\
            'It still has some fight in it though.'
        self.damage = 20
        self.value = 100


class Medipack(Consumable):
    def __init__(self):
        self.name = 'Medipack'
        self.description = 'A first-aid kit to treat your wounds.'
        self.healing_value = 40
        self.value = 60


class Herbs(Consumable):
    def __init__(self):
        self.name = 'Herbs'
        self.description = 'Medicine herbs to restore your health.'
        self.healing_value = 10
        self.value = 12
