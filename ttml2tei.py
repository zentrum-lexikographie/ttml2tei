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
  click.echo("RUN")

if __name__ == '__main__':
  run()
