class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects!')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class GiantSpider(Enemy):
    def __init__(self):
        self.name = 'Giant Spider'
        self.hp = 10
        self.damage = 3


class Skeleton(Enemy):
    def __init__(self):
        self.name = 'Skeleton'
        self.hp = 30
        self.damage = 10


class BatColony(Enemy):
    def __init__(self):
        self.name = 'Colony of Bats'
        self.hp = 100
        self.damage = 2


class Gravedigger(Enemy):
    def __init__(self):
        self.name = 'Gravedigger'
        self.hp = 80
        self.damage = 15


class Priest(Enemy):
    def __init__(self):
        self.name = 'Priest'
        self.hp = 180
        self.damage = 20
        self.interact = 'Holy Water'
