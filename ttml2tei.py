# -*- coding: utf-8 -*-

from lxml import etree

import click

ns = {
  'tt' : "http://www.w3.org/ns/ttml",
  'ttp' : "http://www.w3.org/1999/ttml#parameter",
  'tts' : "http://www.w3.org/1999/ttml#styling",
}
TT = "{%s}" % ns['tt']
TTP = "{%s}" % ns['ttp']
TTS = "{%s}" % ns['tts']

@click.command()
@click.argument('ttml', type=click.File('rb'))
def run(ttml):

  #
  # read in ttml
  #
  ttml_tree = etree.parse(ttml)
  tt_body = ttml_tree.getroot().find("./" + TT + "body")
  if tt_body is None:
    click.echo("No body element found. Aborting", err=True)
    sys.exit(1)

  #
  # create destination xml
  #
  tei_root = etree.Element("TEI")
  tei_header = etree.SubElement(tei_root, "teiHeader")
  text = etree.SubElement(tei_root, "text")
  body = etree.SubElement(text, "body")

  #
  # interpret ttml
  #

  #
  # select relevant paragraph attributes to carry over to tei
  relevant_par_atttrib = ["style", "begin", "end", "region"]

  #
  # add a div element to tei for each div element in ttml
  for tt_div in tt_body.findall("./" + TT + "div"):
    div = etree.SubElement(body, "div")
    div.set("style", tt_div.get("style", ""))
    
    #
    # iterate over tt_p in tt_div and create either hi or lb
    for tt_p in tt_div.findall("./" + TT + "p"):
      pb = etree.SubElement(div, "pb")
      for attrib in relevant_par_atttrib:
        pb.set(attrib, tt_p.get(attrib, ""))
      for child in tt_p:
        if child.tag == TT + "br":
          pb.append(etree.Element("lb"))
        elif child.tag == TT + "span":
          hi = etree.SubElement(pb, "hi")
          hi.text = child.text
          hi.set("style", child.get("style", ""))

  #
  # print destination xml
  #
  click.echo(etree.tostring(tei_root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
  
  

if __name__ == '__main__':
  run()
