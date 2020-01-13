from data.classes.weapons import *
from pygame import quit

class AnimSeq:
    def __init__(self, seq, frame_time):
        self.frames = seq
        self.image = self.frames[0]
        self.frame_time = frame_time
        self.loop_flag = False
        self.current_time = 0
        self.current_frame = 0

    def reset(self):
        self.image = self.frames[0]
        self.current_time = 0
        self.current_frame = 0
        self.loop_flag = False

    def update(self, dt):
        self.current_time += dt
        if self.frame_time <= self.current_time:
            self.current_frame += 1
            if len(self.frames) - 1 <= self.current_frame:
                self.current_frame = 0
                self.loop_flag = True
            self.image = self.frames[self.current_frame]
            self.current_time -= self.frame_time


class PlayerBear:
    def __init__(self, sound_lib, sprite_lib):
        self.mask = None
        self.lib = dict()
        if self.load_data(sound_lib, sprite_lib):
            print('Class "PlayerBear" could not load data')
            quit()
        self.current_weapon = BearGuns(self.lib['bullet'][0], self.lib['arm'])
        self.current_animation = None
        self.image = None
        self.rotation = 0
        self.rect = None

    def load_sprite(self, lib, source, target, animdata=False):
        spr = lib.get(source, None)
        if spr:
            if animdata:
                self.lib[target] = AnimSeq(spr[0], spr[1])
                return 0
            else:
                self.lib[target] = spr
                return 0
        else:
            print('Cannot load', source)
            return 1

    def load_data(self, sound, spritelib):
        err = self.load_sprite(spritelib.seq_library, 'sprBearWalkUnarmed', 'walkUnarmed', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkUnarmedBack', 'walkUnarmedBack', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkBat', 'walkBat', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkChain', 'walkChain', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkClub', 'walkClub', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkKnife', 'walkKnife', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkPipe', 'walkPipe', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalk9mm', 'walk9mm', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkKalashnikov', 'walkKalashnikov', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkM16', 'walkM16', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkDoubleBarrel', 'walkDoubleBarrel', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkShotgun', 'walkShotgun', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkSilencer', 'walkSilencer', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkSpecial', 'walkSpecial')
        # err += self.load_sprite(spritelib.seq_library, 'sprBearTurnSpecial', 'turnSpecial', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkUzi', 'walkUzi', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearWalkPizza', 'walkPizza')
        err += self.load_sprite(spritelib.seq_library, 'sprBearArm', 'arm')
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackPunch', 'attackPunch', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackBat', 'attackBat', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackChain', 'attackChain', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackKnife', 'attackKnife', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackPipe', 'attackPipe', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackClub', 'attackClub', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttack9mm', 'attack9mm', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackDoubleBarrel1', 'attackDoubleBarrel2',
                                animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackKalashnikov', 'attackKalashnikov', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackM16', 'attackM16', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackShotgun', 'attackShotgun', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackUzi', 'attackUzi', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearAttackSilencer', 'attackSilencer', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearReloadWeapons', 'reloadWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearHolsterWeapons', 'holsterWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearTakeOutWeapons', 'takeOutWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearDeadMelee', 'deadMelee')
        err += self.load_sprite(spritelib.seq_library, 'sprBearDeadShot', 'deadShot')
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillChain', 'killChain', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillBat', 'killBat', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillClub', 'killClub', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillKnife', 'killKnife', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillPipe', 'killPipe', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearLegs', 'legs', animdata=True)
        err += self.load_sprite(spritelib.img_library, 'sprBulletLSD', 'bullet')
        return err

    def set_weapon(self, name):
        if name == 'BearGuns':
            self.current_animation = self.lib['takeOutWeapons']
            self.current_weapon = BearGuns(self.lib['bullet'][0], self.lib['arm'])

        else:
            print('Error: Unknown name of gun -' + name)

    def take_out_guns(self):
        self.current_animation = self.lib['takeOutWeapons']

    def update(self, mouse_pos, dt):
        if self.current_animation.loop_flag is False:
            if type(self.current_weapon) == 'BearGuns':
                self.current_weapon.update(self.rotation, self.rect, mouse_pos)
                self.image = self.lib['walkSpecial'][0][0]
            else:
                self.current_weapon.update(self.rotation)
        else:
            self.image =

    def move(self, vec):
        if type(self.current_weapon) != 'BearGuns':

