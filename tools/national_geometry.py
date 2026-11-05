"""Read exact GeoJSON delivery with memory bounded by the largest feature.

No coordinate transformation or sampling. Every decoded byte is hashed and
compared, and every feature is parsed. Uses only the standard library.
"""
from contextlib import ExitStack
import gzip
import hashlib
import json
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def open_decoded(path):
    path = Path(path)
    return gzip.open(path, 'rb') if path.suffix == '.gz' else path.open('rb')


def delivery_digest(path, copies=()):
    """Hash original decoded bytes and compare all lossless deliveries in chunks."""
    digest = hashlib.sha256()
    size = 0
    matches = [True] * len(copies)
    with ExitStack() as stack:
        original = stack.enter_context(open_decoded(path))
        streams = [stack.enter_context(open_decoded(p)) for p in copies]
        while True:
            chunk = original.read(CHUNK_SIZE)
            for index, stream in enumerate(streams):
                if stream.read(CHUNK_SIZE) != chunk:
                    matches[index] = False
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size, matches


class _JSONStream:
    def __init__(self, stream, chunk_size):
        self.stream = stream
        self.chunk_size = chunk_size
        self.buffer = ''
        self.position = 0
        self.eof = False
        self.decoder = json.JSONDecoder()

    def fill(self, amount=None):
        self.buffer = self.buffer[self.position:]
        self.position = 0
        chunk = self.stream.read(amount or self.chunk_size)
        self.eof = not chunk
        self.buffer += chunk

    def peek(self):
        while True:
            while self.position < len(self.buffer) and self.buffer[self.position] in ' \t\r\n':
                self.position += 1
            if self.position < len(self.buffer):
                return self.buffer[self.position]
            if self.eof:
                return ''
            self.fill()

    def expect(self, token):
        if self.peek() != token:
            raise ValueError('Invalid GeoJSON: expected ' + repr(token))
        self.position += 1

    def value(self):
        self.peek()
        amount = self.chunk_size
        while True:
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.position)
                if end < len(self.buffer) and self.buffer[end] in ' \t\r\n,]}:':
                    self.position = end
                    return value
                if self.eof and end == len(self.buffer):
                    self.position = end
                    return value
                if self.eof:
                    raise ValueError('Invalid GeoJSON value boundary')
            except json.JSONDecodeError:
                if self.eof:
                    raise
            self.fill(amount)
            amount *= 2  # Avoid quadratic reparsing of a very large feature.


def iter_features(path, chunk_size=CHUNK_SIZE):
    """Parse the entire FeatureCollection, releasing coordinates after each row."""
    import io
    with open_decoded(path) as raw, io.TextIOWrapper(raw, encoding='utf-8-sig') as stream:
        reader = _JSONStream(stream, chunk_size)
        reader.expect('{')
        keys = set()
        collection_type = None
        if reader.peek() != '}':
            while True:
                key = reader.value()
                if not isinstance(key, str) or key in keys:
                    raise ValueError('Invalid GeoJSON: duplicate/non-string collection key')
                keys.add(key)
                reader.expect(':')
                if key == 'features':
                    reader.expect('[')
                    if reader.peek() != ']':
                        while True:
                            feature = reader.value()
                            if not isinstance(feature, dict):
                                raise ValueError('Invalid GeoJSON feature')
                            yield feature
                            del feature
                            if reader.peek() == ']':
                                break
                            reader.expect(',')
                    reader.expect(']')
                else:
                    value = reader.value()
                    if key == 'type':
                        collection_type = value
                if reader.peek() == '}':
                    break
                reader.expect(',')
        reader.expect('}')
        if reader.peek():
            raise ValueError('Invalid GeoJSON: trailing content')
        if collection_type != 'FeatureCollection' or 'features' not in keys:
            raise ValueError('Not a GeoJSON FeatureCollection with features')
