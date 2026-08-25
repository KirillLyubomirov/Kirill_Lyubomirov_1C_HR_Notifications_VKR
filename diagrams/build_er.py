from pathlib import Path
from html import escape

BASE=Path(__file__).resolve().parent/'final'

class Diagram:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker></defs>',
        f'<rect width="{w}" height="{h}" fill="white"/>', '<g font-family="DejaVu Sans" fill="#172033">']
    def text(self,x,y,lines,size=28,anchor='middle',bold=False):
        lines=lines.split('\n')
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"'+(' font-weight="bold"' if bold else '')+'>')
        for i,line in enumerate(lines):self.parts.append(f'<tspan x="{x}" dy="{0 if i==0 else size*1.24}">{escape(line)}</tspan>')
        self.parts.append('</text>')
    def rect(self,x,y,w,h,fill='#F5F7FA',radius=0,stroke='#475569'):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2.3"/>')
    def box(self,x,y,w,h,lines,kind='box',fill='#F5F7FA',size=28):
        if lines.startswith(('D1.','D2.','D3.','D4.')):
            ident,lines=lines.split('. ',1)
            self.rect(x,y,w,h,fill)
            self.line([(x+58,y),(x+58,y+h)],False)
            self.text(x+29,y+h/2+8,ident,23)
            n=lines.count('\n')+1
            self.text(x+58+(w-58)/2,y+h/2-(n-1)*25*0.62+25*0.34,lines,25)
            return
        if kind=='process':self.parts.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="#475569" stroke-width="2.3"/>')
        else:self.rect(x,y,w,h,fill,12 if kind=='state' else 0)
        n=lines.count('\n')+1
        self.text(x+w/2,y+h/2-(n-1)*size*0.62+size*0.34,lines,size)
    def line(self,coords,arrow=True,dash=False):
        s=' '.join(f'{x},{y}' for x,y in coords)
        self.parts.append(f'<polyline points="{s}" fill="none" stroke="#475569" stroke-width="2.3"'+(' stroke-dasharray="9 6"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def save(self,name):
        self.parts.append('</g></svg>')
        result='\n'.join(self.parts)+'\n'
        for sub in ['source','svg']:(BASE/sub/(name+'.svg')).write_text(result)

d=Diagram(1200,1200)
d.box(65,70,435,105,'Сотрудник\nорганизация, отдел,\nдолжность','state',size=27)
d.box(700,70,435,105,'Исходный кадровый документ\nвид изменения, основание','state',size=26)
d.box(700,290,435,105,'VKRDocumentLinks\nисточник → событие','state',size=28)
d.box(65,290,435,125,'Кадровое изменение\nсотрудник, дата действия,\nзначения до и после','state',size=27)
d.box(700,480,435,105,'VKRSourceStates\nревизия и снимок события','state',size=27)
d.box(65,555,435,125,'Уведомление\nemail, тема, текст,\nподразделение','state',size=28)
d.box(65,810,435,105,'VKRQueue\nсостояние, попытки, захват','state',size=27)
d.box(700,810,435,105,'VKRAttempts\nначало, окончание, результат','state',size=26)
d.box(65,1050,435,105,'VKRNotificationKeys\nсобытие + ревизия + email','state',size=27)
d.box(700,1050,435,105,'VKROperatorDecisions\nоператор, время, основание','state',size=27)
d.line([(500,122),(700,122)]);d.text(600,102,'1 : N',26)
d.line([(918,175),(918,290)]);d.text(970,244,'1 : 1',26)
d.line([(700,342),(500,342)]);d.text(598,322,'1 : 1',26)
d.line([(500,385),(595,440),(595,532),(700,532)]);d.text(646,504,'1 : 1',26)
d.line([(280,415),(280,555)]);d.text(335,496,'1 : N',26)
d.line([(280,680),(280,810)]);d.text(335,755,'1 : 1',26)
d.line([(500,594),(648,650),(918,650),(918,810)]);d.text(970,748,'1 : N',26)
d.line([(500,643),(580,700),(580,1102),(700,1102)]);d.text(640,1082,'1 : N',26)
d.line([(65,618),(25,618),(25,1102),(65,1102)]);d.text(138,988,'1 : 1',26)
d.save('er_core')
