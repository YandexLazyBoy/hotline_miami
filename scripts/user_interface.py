from scripts.map import *


class Font:
    def __init__(self, name):
        self.chars = dict()
        self.spacing = 1
        self.name = 'no name'
        self.load_chars(name)

    def load_chars(self, name):
        tree = ET.parse(os.path.join('data/fonts', name))
        root = tree.getroot()
        pages = list()
        self.name = root.find('info').attrib['face']
        self.spacing = int(root.find('info').attrib['spacing'].split(',')[0])
        scale = (2, 2)
        for spr in root.find('pages'):
            pages.append(pygame.image.load(os.path.join('data/fonts', spr.attrib['file'])))
            pages[-1].set_colorkey((0, 0, 0))
        for char in root.find('chars'):
            c = pygame.Surface((int(char.attrib['width']), int(char.attrib['height'])), pygame.SRCALPHA)
            c.blit(pages[int(char.attrib['page'])], (- int(char.attrib['x']), - int(char.attrib['y'])))
            self.chars[int(char.attrib['id'])] = pygame.transform.scale(c, (int(scale[0] * int(char.attrib['width'])),
                                                                            int(scale[1] * int(char.attrib['height']))))

    def get_surface(self, string, alpha=True):
        fs = ''
        size = [0, 0]
        t = 0
        for ch in list(string):
            c = self.chars.get(ord(ch), None)
            if self.chars:
                fs += ch
                size[0] += c.get_width() + self.spacing
                t = c.get_height() if t < c.get_height() else t
            else:
                print(ch, 'not found in', self.name)

        size[1] = t
        cur = 0
        fsur = pygame.Surface(size, pygame.SRCALPHA) if alpha else pygame.Surface(size)

        for ch in list(fs):
            c = self.chars[ord(ch)]
            fsur.blit(c, (cur, t - c.get_height()))
            cur += c.get_width() + self.spacing
        return fsur
