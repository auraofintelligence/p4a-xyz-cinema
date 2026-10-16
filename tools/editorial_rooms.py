"""Keep reviewed room structure separate from generic Twinkle scaffolding."""

def is_editorial_room(document):
    return 'data-editorial-room="aura"' in document
