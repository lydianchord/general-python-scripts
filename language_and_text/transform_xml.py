from lxml import etree
import sys

# ex: python transform_xml.py input/Ave_Maria.xml input/music_xml_lyrics.xsl html

arguments = sys.argv[1:]
if len(arguments) == 3:
    xml_file, xsl_file, new_ext = arguments
else:
    sys.exit('Usage: python transform_xml.py [xml_file] [xsl_file] [new_ext]')
new_file = xml_file.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '_transformed.' + new_ext

xml_tree = etree.parse(xml_file)
xslt_tree = etree.parse(xsl_file)
transform = etree.XSLT(xslt_tree)
new_xml_tree = transform(xml_tree)
result = etree.tostring(new_xml_tree, pretty_print=True)

with open('output/' + new_file, 'w') as f:
    f.write(result)
