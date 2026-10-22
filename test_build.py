import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
import build

class PackageTests(unittest.TestCase):
    def test_self_contained_reproducible_widget(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            package=build.build(out)
            first=hashlib.sha256(package.read_bytes()).hexdigest()
            self.assertEqual(first,hashlib.sha256(build.build(out).read_bytes()).hexdigest())
            with zipfile.ZipFile(package) as archive:
                self.assertIsNone(archive.testzip())
                self.assertTrue(set(build.FILES).issubset(archive.namelist()))
                self.assertNotIn(b'http://',archive.read('index.html'))
                self.assertNotIn(b'https://',archive.read('index.html'))
                config=ET.fromstring(archive.read('config.xml'))
                for tag,wh in [('ThumbIcon',(106,86)),('BigThumbIcon',(115,95)),('ListIcon',(85,70)),('BigListIcon',(95,78))]:
                    self.assertEqual(struct.unpack('>II',archive.read(config.findtext(tag))[16:24]),wh)
    def test_preserves_other_apps(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);catalog=out/'widgetlist.xml'
            catalog.write_text('<rsp stat="ok"><list><widget id="OtherApp"><title>Other app</title><download>http://installer.example.test/other.zip</download></widget></list></rsp>')
            build.build(out,'http://installer.example.test');build.build(out,'http://installer.example.test')
            self.assertEqual([e.get('id') for e in ET.parse(catalog).findall('.//widget')],['OtherApp',build.APP_ID])
    def test_rejects_installer_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):build.build(Path(directory),'http://user:password@installer.example.test')
if __name__=='__main__':unittest.main()
