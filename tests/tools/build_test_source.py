"""Create a native acceptance-only copy. The original source is never edited."""
from pathlib import Path
import argparse, shutil, re, uuid

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=args.source.resolve();output=args.output.resolve()
    if output.exists():parser.error('Output must be a new directory')
    if not (source/'Configuration.xml').is_file():parser.error('Configuration.xml is missing')
    if output.is_relative_to(source):parser.error('Do not create the test copy inside production source')
    shutil.copytree(source,output)
    (output/'ConfigDumpInfo.xml').unlink(missing_ok=True)
    config=output/'Configuration.xml';text=config.read_text(encoding='utf-8-sig')
