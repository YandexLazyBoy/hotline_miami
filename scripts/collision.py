def rectcollide(rect, *group):
    return [r for r in group if rect.collide(r)]

