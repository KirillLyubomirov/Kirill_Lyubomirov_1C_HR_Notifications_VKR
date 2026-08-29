import fs from 'node:fs/promises';
import path from 'node:path';
import {instance} from '@viz-js/viz';
import sharp from 'sharp';
const root=process.argv[2];
if(!root)throw new Error('Pass the directory containing source/, svg/, png/');
const viz=await instance();
for(const file of await fs.readdir(path.join(root,'source'))){
 const ext=path.extname(file);
 if(!['.dot','.svg'].includes(ext))continue;
 const input=await fs.readFile(path.join(root,'source',file),'utf8');
 const svg=ext==='.dot'?viz.renderString(input,{format:'svg',engine:'dot'}):input;
 const name=path.basename(file,ext);
 await fs.writeFile(path.join(root,'svg',name+'.svg'),svg);
 await sharp(Buffer.from(svg),{density:220}).resize({width:3000,height:3000,fit:'inside'}).png().toFile(path.join(root,'png',name+'.png'));
 console.log(name);
}
