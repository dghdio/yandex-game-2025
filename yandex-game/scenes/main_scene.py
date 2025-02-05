

from pygame import event, mouse
from pygame.sprite import Group
from pygame.locals import *

from third_party.tiledtmxloader import helperspygame, tmxreader

from scenes.scene import Scene
from objects.decor import Furniture
from objects.player import Player
from objects.enemy import Enemy, BossEnemy
from objects.teleport import Teleport
from objects.health import HealthPoint
from utils.camera import Camera
from utils.data_displayer import DataDisplayer
from utils.config import *

maps = ['library_map_2.tmx', 'untitled.tmx']
class MainScene(Scene):
    """Главная игровая сцена."""

    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0))
        self.walls = []
        self.enemy_spawn_positions = []
        self.hp_spawn_positions = []
        self.furniture = Group()
        self.enemies = Group()
        self.plasmas = Group()
        self.traps = Group()
        self.teleports = Group()
        self.healthpoints = Group()
        self.animations = Group()
        self.camera = Camera(TOTAL_LEVEL_SIZE)
        self.create_map('library_map_2.tmx')
        self.player = Player(*self._player_coords)
        self.stats = DataDisplayer()
        self.delta_time = 10
        self.wave = 0

    def create_map(self, filename):
        world_map = tmxreader.TileMapParser().parse_decode("resources/{}".format(filename))
        resources = helperspygame.ResourceLoaderPygame()
        resources.load(world_map)
        layers = helperspygame.get_layers_from_map(resources)
        self.bg_layer = layers[0].scale(layers[0], UNIT_SCALE, UNIT_SCALE)
        obj_layer = layers[1]
        for obj in obj_layer.objects:
            obj_type = obj.properties['type']
            x = rscaled(obj.x)
            y = rscaled(obj.y)
            width = rscaled(obj.width)
            height = rscaled(obj.height)
            if obj_type == 'player':
                self._player_coords = (x, y - WALL_HEIGHT)
            elif obj_type == 'wall':
                self.walls.append(Rect(x, y, width, height))
            elif obj_type == 'teleport':
                s_id = obj.properties['id']
                tgt_id = obj.properties['tgt_id']
                self.teleports.add(Teleport(x, y - WALL_HEIGHT, s_id, tgt_id))
            elif obj_type == 'gspawn':
                self.enemy_spawn_positions.append((x, y - WALL_HEIGHT))
            elif obj_type == 'hspawn':
                self.hp_spawn_positions.append((x, y - WALL_HEIGHT))
            elif obj_type == 'sofa':
                self.furniture.add(Furniture.create('sofa', x, y))
            elif obj_type == 'flower':
                self.furniture.add(Furniture.create('flower', x, y - WALL_HEIGHT))
        self.renderer = helperspygame.RendererPygame()
        HealthPoint.random_spawn(self.hp_spawn_positions, self.healthpoints, HEALTHPOINT_NUMBER)

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.return_code = 'tomenu'
                elif e.key == K_SPACE:
                    self.player.handle_trap(self.traps, self.wave)
                else:
                    self.player.set_direction(e.key, True)
            elif e.type == KEYUP:
                self.player.set_direction(e.key, False)
            elif e.type == MOUSEBUTTONDOWN:
                self.player.shoot(self.camera.apply(self.player.rect), mouse.get_pos(), self.plasmas)

        if not self.player.is_alive:
            self.return_code = 'gameover'
            return
        if len(self.enemies) == 0:
            self.wave += 1
            for trap in self.traps:
                trap.delete(self.traps)
            if self.wave % BOSS_ENEMY_SPAWN_DELAY == 0:
                boss_amount = self.wave // BOSS_ENEMY_SPAWN_DELAY
                BossEnemy.random_spawn(self.enemy_spawn_positions, self.enemies, boss_amount)
                Enemy.random_spawn(self.enemy_spawn_positions, self.enemies, self.wave - boss_amount)
            else:
                Enemy.random_spawn(self.enemy_spawn_positions, self.enemies, self.wave)

    def update_objects(self):
        self.delta_time = self.clock.get_time()
        self.furniture.update(self)
        self.player.update(self)
        self.enemies.update(self)
        self.plasmas.update(self)
        self.traps.update(self)
        self.teleports.update(self)
        self.healthpoints.update(self)
        self.animations.update(self)
        self.camera.update(self.player)
        ctr_offset = self.camera.reverse(CENTER_OF_SCREEN)
        self.renderer.set_camera_position_and_size(ctr_offset[0], ctr_offset[1],
                                                   *SCREEN_SIZE, "center")
        self.stats.update(self)

    def draw_objects(self):
        self.screen.fill((0, 0, 0))
        self.renderer.render_layer(self.screen, self.bg_layer)
        self.draw_group(self.furniture)
        self.draw_group(self.teleports)
        self.draw_group(self.healthpoints)
        self.draw_group(self.traps)
        self.draw_group(self.plasmas)
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        self.draw_group(self.enemies)
        self.draw_group(self.animations)
        for e in self.enemies:
            e.draw_hp_if_need(self)
        self.stats.draw(self.screen)

    def draw_group(self, group):
        for obj in group:
            self.screen.blit(obj.image, self.camera.apply(obj.rect))

    def restart(self):
        self.enemies.empty()
        self.plasmas.empty()
        self.traps.empty()
        self.animations.empty()
        self.player.reborn(*self._player_coords)

        for furn in self.furniture:
            furn.reset()
        while len(Furniture.pool) != 0:
            self.furniture.add(Furniture.create())

        self.wave = 0
