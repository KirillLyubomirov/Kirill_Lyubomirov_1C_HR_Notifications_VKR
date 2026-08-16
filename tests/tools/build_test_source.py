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
    marker='<CommonModule>VKRJobs</CommonModule>'
    if text.count(marker)!=1:raise ValueError('Expected one VKRJobs entry')
    text=text.replace(marker,marker+'\n\t\t\t<CommonModule>VKRTestDriver</CommonModule>')
    config.write_text(text,encoding='utf-8-sig')
    module=(output/'CommonModules/VKRJobs.xml').read_text(encoding='utf-8-sig')
    identifier=str(uuid.uuid5(uuid.UUID('81cfd233-18bb-4e74-bb34-727b03ce25e0'),'Test.VKRTestDriver'))
    module,n=re.subn(r'(<CommonModule uuid=")[^"]+',lambda m:m.group(1)+identifier,module,count=1)
    if n!=1:raise ValueError('CommonModule UUID was not found')
    module=module.replace('VKRJobs','VKRTestDriver')
    (output/'CommonModules/VKRTestDriver.xml').write_text(module,encoding='utf-8-sig')
    target=output/'CommonModules/VKRTestDriver/Ext/Module.bsl';target.parent.mkdir(parents=True)
    shutil.copy2(Path(__file__).with_name('VKRTestDriver.bsl'),target)
    shutil.copy2(Path(__file__).with_name('ManagedApplicationTest.bsl'),output/'Ext/ManagedApplicationModule.bsl')
    print(output)

if __name__=='__main__':main()
