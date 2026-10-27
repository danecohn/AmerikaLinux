"""Packaging metadata carries the VigilTech name, icon, copyright and licence (checked without building)."""
import configparser
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_desktop_entry_names_vigil_social_and_its_icon():
    parser = configparser.ConfigParser(interpolation=None, delimiters=('=',))
    parser.optionxform = str
    parser.read(ROOT / 'packaging/amerika-social.desktop', encoding='utf-8')
    entry = parser['Desktop Entry']
    assert entry['Name'] == 'Vigil Social' and entry['Type'] == 'Application'
    assert entry['Exec'] and entry['Icon'] and entry['Categories'].endswith(';')
    assert 'Makk' not in entry['Name'] + entry['Comment'] + entry['GenericName']


def test_metainfo_declares_vigiltech_and_gpl():
    root = ET.parse(ROOT / 'packaging/amerika-social.metainfo.xml').getroot()
    assert root.findtext('name') == 'Vigil Social'
    assert root.findtext('project_license') == 'GPL-3.0-only'
    assert root.find('developer/name').text == 'VigilTech'
    assert root.find('launchable').text == 'amerika-social.desktop'


def test_every_hicolor_size_the_installer_copies_exists():
    for size in (16, 32, 48, 64, 128, 256, 512):
        assert (ROOT / f'assets/vigiltech/icons/social-{size}.png').is_file()
    script = (ROOT / 'packaging/install-linux.sh').read_text()
    assert 'vigiltech/icons/social-$size.png' in script


def test_build_script_sets_names_and_copyright():
    build = (ROOT / 'build.py').read_text()
    assert "CFBundleName='Vigil Social'" in build and 'VigilTech' in build
    assert 'Makk' not in build.replace('MakkSocial', '')
