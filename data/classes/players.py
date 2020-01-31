from data.classes.weapons import *


class AnimSeq:
    def __init__(self, seq, frame_time):
        self.frames = seq
        self.image = self.frames[0]
        self.frame_time = frame_time
        self.loop_flag = False
        self.current_time = 0
        self.current_frame = 0
        self.rotation = 0

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
            self.current_time -= self.frame_time

        self.image = self.frames[self.current_frame]
        if self.rotation:
            self.image = pygame.transform.rotate(self.image, 360 - self.rotation)


class PlayerBear:
    def __init__(self, sound_lib, sprite_lib, spawn, rotation, err_func):
        self.lib = dict()
        self.s_lib = dict()
        if self.load_data(sound_lib, sprite_lib):
            print('Class "PlayerBear" could not load data')
            err_func()
        self.mask = pygame.mask.from_surface(self.lib['mask'][0])
        self.shoot = print
        self.current_weapon = BearGuns(self.lib['bullet'][0], self.lib['arm'], self.lib['detailsSpecial'])
        self.current_animation = AnimSeq([1], 0.01)
        self.current_animation.loop_flag = True
        self.legs = self.lib['legs']
        self.image = pygame.transform.rotate(self.legs.image, 90 - rotation)
        self.rotation = rotation
        self.center = spawn
        self.o_rect = self.image.get_rect()
        self.rect = self.mask.get_bounding_rects()[0]
        self.current_flag = 'Rifle'

    def set_animation(self, name):
        an = self.lib.get(name, None)
        if an:
            self.current_animation = an
            self.current_animation.reset()
        else:
            print(name, 'animation cannot be loaded')

    def setup_shooting(self, shoot_func):
        self.shoot = shoot_func
        self.current_weapon.shoot = self.shoot

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

    def load_sound(self, lib, name):
        snd = lib.get(name, None)
        if snd:
            self.s_lib[name] = snd
            return 0
        else:
            print('Cannot load', name)
            return 1

    def update_rect(self):
        self.o_rect = self.image.get_rect()
        self.o_rect.move_ip(self.center[0] - self.o_rect.width // 2, self.center[1] - self.o_rect.height // 2)
        self.rect = self.mask.get_bounding_rects()[0]
        self.rect.move_ip(self.center[0] - self.rect.width // 2, self.center[1] - self.rect.height // 2)

    def load_data(self, soundlib, spritelib):
        err = self.load_sprite(spritelib.seq_library, 'sprPlayerBearWalkUnarmed', 'walkUnarmed', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkUnarmedBack', 'walkUnarmedBack', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkBat', 'walkBat', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkChain', 'walkChain', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkClub', 'walkClub', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearWalkKnife', 'walkKnife', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearPipe', 'walkPipe', animdata=True)
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
        err += self.load_sprite(spritelib.img_library, 'sprBearArm', 'arm')
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
        err += self.load_sprite(spritelib.seq_library, 'sprPlayerBearReloadWeapons', 'reloadWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearHolsterWeapons', 'holsterWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprPlayerBearTakeOutWeapons', 'takeOutWeapons', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprBearDeadMelee', 'deadMelee')
        err += self.load_sprite(spritelib.seq_library, 'sprBearDeadShot', 'deadShot')
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillChain', 'killChain', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillBat', 'killBat', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillClub', 'killClub', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillKnife', 'killKnife', animdata=True)
        # err += self.load_sprite(spritelib.seq_library, 'sprBearKillPipe', 'killPipe', animdata=True)
        err += self.load_sprite(spritelib.seq_library, 'sprPlayerBearLegs', 'legs', animdata=True)
        err += self.load_sprite(spritelib.img_library, 'sprBulletLSD', 'bullet')
        err += self.load_sprite(spritelib.img_library, 'sprPlayerBearCollisionMask', 'mask')
        err += self.load_sprite(spritelib.seq_library, 'sprPlayerBearDetailsSpecial', 'detailsSpecial')
        err += self.load_sound(soundlib.sound_library, 'sndUzi')
        return err

    def holster_weapons(self):
        self.current_animation = self.lib['holsterWeapons']
        self.current_flag = 'holster'

    def teleport(self, pos):
        self.center = self.center[0] + pos[0], self.center[1] + pos[1]

    def weapon_init(self):
        self.current_weapon.shoot = self.shoot
        self.current_weapon.launch_anim = self.set_animation
        self.current_weapon.holster = self.holster_weapons
        self.current_weapon.load_sounds(self.s_lib)

    def set_weapon(self, name):
        if name == 'BearGuns':
            self.current_weapon = BearGuns(self.lib['bullet'][0], self.lib['arm'], self.lib['detailsSpecial'])
        else:
            print('Error: Unknown name of gun -', name)
        self.weapon_init()

    def take_out_guns(self):
        self.current_animation = self.lib['takeOutWeapons']  # 0 - тело, 1 - вся фигура
        self.current_weapon = BearGuns(self.lib['bullet'][0], self.lib['arm'], self.lib['detailsSpecial'])
        self.weapon_init()

    def update(self, mouse_pos, dt, v_pos, devl, dbc):
        if self.current_animation.loop_flag is True and self.current_flag != 'unarmed':
            if self.current_flag == 'holster':
                self.current_animation = self.lib['walkUnarmed']
                self.current_flag = 'unarmed'
                return None
            self.current_weapon.update(self.rotation, self.center, mouse_pos, dt,
                                       self.current_animation.loop_flag, v_pos, devl, dbc)

            r1 = self.current_weapon.image.get_rect()
            r2 = self.legs.image.get_rect()
            rect = r1.union(r2)
            self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

            if devl in (0, 1):
                self.image.blit(self.legs.image, ((rect.width - r2.width) // 2, (rect.height - r2.height) // 2))
                self.image.blit(self.current_weapon.image,
                                ((rect.width - r1.width) // 2, (rect.height - r1.height) // 2))
            elif devl in (2, 3):
                self.image = self.lib['mask'][0]
            else:
                self.image.blit(self.current_weapon.image,
                                ((rect.width - r1.width) // 2, (rect.height - r1.height) // 2))

                r2.move_ip((rect.w - r2.w) // 2, (rect.h - r2.h) // 2)
                pygame.draw.rect(self.image, dbc, r2, 1)
        else:
            self.current_animation.rotation = self.rotation
            self.current_animation.update(dt)
            r1 = self.current_animation.image.get_rect()
            r2 = self.legs.image.get_rect()
            rect = r1.union(r2)
            self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            if devl in (0, 1):
                self.image.blit(self.legs.image, ((rect.width - r2.width) // 2, (rect.height - r2.height) // 2))
                self.image.blit(self.current_animation.image, ((rect.width - r1.width) // 2,
                                                               (rect.height - r1.height) // 2))
            elif devl in (2, 3):
                self.image = self.lib['mask'][0]
            else:
                r1.move_ip((rect.w - r1.w) // 2, (rect.h - r1.h) // 2)
                pygame.draw.rect(self.image, dbc, r1, 1)
                r2.move_ip((rect.w - r2.w) // 2, (rect.h - r2.h) // 2)
                pygame.draw.rect(self.image, dbc, r2, 1)
        self.update_rect()

    def move(self, vec, dt):
        self.center = self.center[0] + PLAYER_SPEED * vec[0] * dt, self.center[1] + PLAYER_SPEED * vec[1] * dt
        if self.current_flag == 'unarmed':
            self.current_animation.update(dt)
        if vec == [0, 0]:
            self.legs.reset()
            if self.current_flag == 'unarmed':
                self.current_animation.reset()
        elif vec == [0, 1]:
            self.legs.rotation = 90
        elif vec == [1, 1]:
            self.legs.rotation = 45
        elif vec == [1, 0]:
            self.legs.rotation = 0
        elif vec == [-1, 1]:
            self.legs.rotation = 135
        elif vec == [-1, 0]:
            self.legs.rotation = 180
        elif vec == [-1, -1]:
            self.legs.rotation = 225
        elif vec == [0, -1]:
            self.legs.rotation = 270
        elif vec == [1, -1]:
            self.legs.rotation = 315
        self.legs.update(dt)


PLAYERS_DB = [PlayerBear]
