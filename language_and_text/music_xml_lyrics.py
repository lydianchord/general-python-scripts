import sys
from lxml import etree

# ex: python music_xml_lyrics.py input/Ave_Maria.xml

if len(sys.argv) == 2:
    xml_file = sys.argv[1]
else:
    sys.exit('Usage: python music_xml_lyrics.py [xml_file]')
new_file = xml_file.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '_lyrics.txt'

lyrics_list = []
xml_tree = etree.parse(xml_file)
lyric_nodes = xml_tree.xpath("/score-partwise/part[@id='P1']/measure/note/lyric[@number='1']")
find_text = etree.XPath('text/text()', smart_strings=False)
find_syllabic = etree.XPath('syllabic/text()', smart_strings=False)
for node in lyric_nodes:
    lyrics_list.append(find_text(node)[0])
    syllabic = find_syllabic(node)[0]
    if syllabic != 'begin' and syllabic != 'middle':
        lyrics_list.append(' ')
lyrics = ''.join(lyrics_list).strip()

with open('output/' + new_file, 'w') as f:
    f.write(lyrics)
