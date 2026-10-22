#!/usr/bin/env python3
"""Build an Orsay widget and optional multi-app installer catalog, using Python's standard library."""
import argparse
from pathlib import Path
import re
import struct
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import zipfile
import zlib

ROOT = Path(__file__).resolve().parent
FILES = ('index.html', 'app.js', 'style.css')
APP_ID = 'OrsayCinema'
VERSION = '0.001'

def chunk(kind, payload):
    return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff)

def icon(width, height):
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            px = (x + 0.5 - width / 2) * 256 / height + 128
            py = (y + 0.5) * 256 / height
            film = 48 <= px < 208 and 40 <= py < 216
            frame = 80 <= px < 176 and (56 <= py < 120 or 136 <= py < 200)
            holes = (56 <= px < 68 or 188 <= px < 200) and any(top <= py < top + 16 for top in (56, 88, 120, 152, 184))
            row.extend((86, 203, 187) if film and not frame and not holes else (17, 30, 40))
        rows.append(b'\0' + bytes(row))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b''.join(rows))) + chunk(b'IEND', b'')

def update_catalog(path, server_url, package):
    if path.exists():
        tree = ET.parse(path)
        root = tree.getroot()
        listing = root.find('list')
        if listing is None:
            raise ValueError('Existing widgetlist.xml has no list; refusing to overwrite it')
    else:
        root = ET.Element('rsp', {'stat': 'ok'})
        listing = ET.SubElement(root, 'list')
    widget = next((n for n in listing.findall('widget') if n.get('id') == APP_ID), None)
    if widget is None:
        widget = ET.SubElement(listing, 'widget')
    widget.clear()
    widget.set('id', APP_ID)
    ET.SubElement(widget, 'title').text = 'Orsay Cinema'
    ET.SubElement(widget, 'compression', {'size': str(package.stat().st_size), 'type': 'zip'})
    ET.SubElement(widget, 'description').text = 'Independent personal-media client for legacy Samsung TVs'
    ET.SubElement(widget, 'download').text = server_url.rstrip('/') + '/' + package.name
    path.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))

def build(output, server_url=None):
    output.mkdir(parents=True, exist_ok=True)
    payloads = {name: (ROOT / name).read_bytes() for name in FILES}
    # Samsung system scripts are references supplied by the TV, never redistributed.
    icons = [('ThumbIcon', 'thumb.png', 106, 86), ('BigThumbIcon', 'bigthumb.png', 115, 95), ('ListIcon', 'list.png', 85, 70), ('BigListIcon', 'biglist.png', 95, 78)]
    widget = ET.Element('widget')
    for tag, name, width, height in icons:
        ET.SubElement(widget, tag).text = name
        payloads[name] = icon(width, height)
    for tag, value in [('category','video'),('autoUpdate','n'),('ver',VERSION),('fullwidget','y'),('srcctl','y'),('ticker','n'),('childlock','n'),('audiomute','n'),('videomute','n'),('dcont','y'),('movie','y'),('widgetname','Orsay Cinema'),('description','Independent client compatible with Plex Media Server'),('mouse','n'),('width','1280'),('height','720')]:
        ET.SubElement(widget, tag).text = value
    ET.SubElement(ET.SubElement(widget, 'author'), 'name').text = 'Orsay Cinema contributors'
    payloads['config.xml'] = ET.tostring(widget, encoding='utf-8', xml_declaration=True)
    payloads['widget.info'] = b'Application Position = 0,0\nApplication Size = 1280x720\nScreen Number = 1\nScreen Resolution = 1280x720\nUse Alpha Blending? = Yes\n'
    package = output / (APP_ID + '_' + VERSION + '.zip')
    with zipfile.ZipFile(package, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in payloads.items():
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    if server_url:
        parsed = urlsplit(server_url)
        if parsed.scheme != 'http' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
            raise ValueError('Installer URL must be an HTTP origin without credentials, path, or query')
        update_catalog(output / 'widgetlist.xml', server_url, package)
    return package

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--server-url', help='Local HTTP installer origin; used only in the generated, untracked catalog')
    args = parser.parse_args()
    print(build(args.output, args.server_url))
