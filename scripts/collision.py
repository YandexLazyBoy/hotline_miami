class ColGeom:
    def __init__(self, mask, position):
        self.mask = mask
        self.rect = mask.get_bounding_rects()[0]
        self.move(position)

    def move(self, pos):
        self.rect = self.rect.move(pos[0], pos[1])
        self.center = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2


def rectcollide(rect, *group):
    return [r for r in group if rect.collide(r)]


def maskcollide(left, right):
    xoffset = right.rect[0] - left.rect[0]
    yoffset = right.rect[1] - left.rect[1]
    leftmask = left.mask
    rightmask = right.mask
    return leftmask.overlap_mask(rightmask, (xoffset, yoffset))


def zerodiv(v1, v2, clear=False):
    if clear:
        return v1 // v2 if v2 else 0
    else:
        return v1 / v2 if v2 else 0
