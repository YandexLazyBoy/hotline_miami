class ColGeom:
    def __init__(self, mask, position):
        self.mask = mask
        self.rect = mask.get_rect
        self.rect.move_ip(position[0], position[1])


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
        return v1 // v2 if v1 and v2 else 0
    else:
        return v1 / v2 if v1 and v2 else 0
