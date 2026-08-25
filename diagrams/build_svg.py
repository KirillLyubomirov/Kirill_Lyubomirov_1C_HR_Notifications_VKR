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

# DFD: the repeated D3 and D4 stores in the lower panel denote the same data.
d=Diagram(1280,1450)
d.text(40,38,'Подготовка и передача',30,'start',True)
d.box(30,100,260,80,'Кадровик',fill='white')
d.box(890,82,360,118,'D2. Правила, группы\nи шаблоны',fill='white')
d.box(405,87,410,110,'1. Проверить документ\nи подготовить задания','process')
d.line([(290,140),(405,140)]);d.text(347,111,'изменение',22)
d.line([(890,140),(815,140)]);d.text(852,214,'настройки',22)
d.box(30,300,350,100,'D1. Сотрудники\nи кадровые события',fill='white')
d.box(485,300,350,100,'D3. Очередь\nуведомлений',fill='white')
d.line([(470,182),(355,240),(300,300)]);d.text(255,245,'событие',23)
d.line([(660,197),(660,300)]);d.text(740,257,'задания',24)
d.box(465,500,390,115,'2. Передать письмо\nи записать результат','process')
d.box(965,495,285,120,'Локальный\nSMTP-сервер',fill='white')
d.line([(605,400),(605,502)]);d.text(535,459,'задание',23)
d.line([(710,502),(710,400)]);d.text(771,459,'статус',23)
d.line([(852,540),(965,540)]);d.text(905,517,'письмо',23)
d.line([(965,585),(852,585)]);d.text(914,632,'ответ SMTP',22)
d.box(30,508,330,100,'D4. Попытки\nи решения',fill='white')
d.line([(465,558),(360,558)]);d.text(411,603,'попытка',23)
d.line([(30,680),(1250,680)],False)
d.text(40,731,'Разбор исключений и отчётность',30,'start',True)
d.box(30,820,330,100,'D3. Очередь\nуведомлений',fill='white')
d.box(462,820,402,100,'3. Разобрать\nисключение','process')
d.box(980,820,270,100,'Оператор',fill='white')
d.line([(360,846),(466,846)]);d.text(410,798,'исключение',23)
d.line([(466,896),(360,896)]);d.text(406,964,'повтор /\nпрекращение',22)
d.line([(980,867),(864,867)]);d.text(922,795,'основание\nрешения',22)
d.box(500,1035,330,95,'D4. Попытки\nи решения',fill='white')
d.line([(665,920),(665,1035)]);d.text(735,991,'решение',23)
d.box(30,1035,330,95,'D1. Сотрудники\nи кадровые события',fill='white')
d.box(965,1035,285,95,'D3. Очередь\nуведомлений',fill='white')
d.box(444,1250,440,110,'4. Сформировать отчёты','process',size=27)
d.line([(195,1130),(195,1305),(444,1305)]);d.text(310,1198,'кадровые\nфакты',24)
d.line([(665,1130),(665,1250)]);d.text(747,1188,'попытки\nи решения',24)
d.line([(1108,1130),(1108,1215),(850,1215),(850,1280)]);d.text(991,1188,'состояния',23)
d.box(980,1260,270,85,'Оператор',fill='white')
d.line([(884,1305),(980,1305)]);d.text(932,1353,'отчёт',23)
d.text(640,1418,'D1, D3 и D4 повторены для читаемости; состав данных един.',23)
d.save('dfd_tobe')

# State diagram: conditions are numbered in the accompanying transition table.
d=Diagram(1280,990)
d.parts.append('<circle cx="570" cy="30" r="9" fill="#475569"/>')
d.line([(570,40),(570,90)])
d.box(390,90,360,85,'Подготовлено','state')
d.box(390,280,360,85,'Отправляется','state',fill='#FFF4D6')
d.box(900,280,345,85,'Принято SMTP-сервером','state',fill='#E7F1EC',size=25)
d.rect(907,287,331,71,'none',8)
d.box(65,520,325,105,'Ожидает повтора','state')
d.box(465,520,360,105,'Результат\nнеизвестен','state',fill='#FFF4D6')
d.box(930,520,315,120,'Попытки исчерпаны /\nнеустранимая ошибка','state',fill='#FBE9E7',size=25)
d.box(460,870,390,85,'Обработка прекращена','state')
d.rect(467,877,376,71,'none',8)
d.line([(570,175),(570,280)]);d.text(597,236,'1')
d.line([(750,323),(900,323)]);d.text(824,302,'2')
d.line([(430,365),(270,455),(270,520)]);d.text(335,434,'3')
d.line([(145,520),(145,323),(390,323)]);d.text(172,414,'6')
d.line([(645,365),(645,520)]);d.text(670,447,'4')
d.line([(715,365),(1088,455),(1088,520)]);d.text(899,400,'5')
d.line([(465,572),(390,572)]);d.text(427,553,'7')
d.line([(1000,640),(1000,740),(225,740),(225,625)]);d.text(920,721,'8')
# The gap at the crossing distinguishes independent transitions.
d.parts.append('<path d="M645 725 L645 755" stroke="white" stroke-width="12"/>')
d.line([(645,625),(645,870)]);d.text(672,811,'10')
d.line([(1145,640),(1145,913),(850,913)]);d.text(1173,790,'10')
d.line([(390,131),(25,131),(25,913),(460,913)],dash=True);d.text(58,840,'9')
d.line([(325,625),(325,837),(500,837),(500,870)],dash=True);d.text(351,804,'9')
d.save('queue_states')

# Workflow is a sequence of five tasks. The decision is a completion condition,
# not an extra business-process task.
d=Diagram(1280,780)
d.rect(20,65,1240,245,'#FAFBFC',0,'#CBD5E1')
d.rect(20,330,1240,410,'#FAFBFC',0,'#CBD5E1')
d.text(48,107,'Кадровик',29,'start',True)
d.text(48,370,'Оператор уведомлений',29,'start',True)
d.parts.append('<circle cx="92" cy="211" r="9" fill="#475569"/>')
d.box(150,160,365,105,'1. Проверить\nкадровое изменение','state')
d.box(685,160,365,105,'2. Подготовить\nуведомления','state')
d.line([(103,211),(150,211)]);d.line([(515,212),(685,212)])
d.box(685,413,365,105,'3. Обработать очередь','state',size=27)
d.line([(867,265),(867,413)])
d.parts.append('<polygon points="495,405 635,465 495,525 355,465" fill="#FFF4D6" stroke="#475569" stroke-width="2.3"/>')
d.text(495,439,'Остались\nожидающие\nзадания?',22)
d.line([(685,465),(635,465)])
d.line([(495,525),(495,570),(1095,570),(1095,465),(1050,465)]);d.text(789,550,'да — продолжить обработку',24)
d.box(95,620,400,80,'4. Проверить результаты','state',size=27)
d.line([(355,465),(295,465),(295,620)]);d.text(327,580,'нет',24)
d.box(685,620,430,80,'5. Зафиксировать итог','state',size=27)
d.line([(495,660),(685,660)])
d.parts.append('<circle cx="1200" cy="660" r="16" fill="white" stroke="#475569" stroke-width="2.3"/><circle cx="1200" cy="660" r="10" fill="#475569"/>')
d.line([(1115,660),(1183,660)])
d.text(640,775,'Итог: подтверждение SMTP или прекращение обработки с основанием.',24)
d.save('workflow')

# IDEF0 decomposition: label intermediate outputs and connect control/mechanism
# branches explicitly. Existing context diagrams remain unchanged.
d=Diagram(1380,850)
d.text(690,37,'Декомпозиция A0: оформить изменение и уведомить участников',29)
d.text(690,87,'Правила оформления, согласования и контроля',26)
d.line([(315,108),(1245,108)],False)
blocks=[(75,175,'Проверить\nоснование'),(385,305,'Оформить\nизменение'),(695,435,'Подготовить\nи передать\nписьмо'),(1005,565,'Сверить итог\nи составить\nотчёт')]
for i,(x,y,t) in enumerate(blocks):
    d.box(x,y,265,115,t,size=25)
    d.text(x+238,y+99,'A'+str(i+1),19)
    d.line([(x+240,108),(x+240,y)])
    d.line([(x+68,755),(x+68,y+115)])
    if i<3:
        nx,ny,_=blocks[i+1]
        d.line([(x+265,y+57),(nx-20,y+57),(nx-20,ny+57),(nx,ny+57)])
        d.text(nx+10,y+66,['Проверенное\nоснование','Оформленные\nсведения','Сведения\nоб отправке'][i],23,'start')
d.line([(20,232),(75,232)]);d.text(24,150,'Основание',23,'start')
d.line([(1270,622),(1360,622)]);d.text(1315,704,'Сводка',23)
d.line([(143,755),(1073,755)],False)
d.text(690,818,'Кадровик • руководитель • оператор • почтовый клиент • ручной журнал',25)
d.save('idef0_asis_decomposition')

for name in ['dfd_tobe','queue_states','workflow']:
    (BASE/'source'/(name+'.dot')).unlink(missing_ok=True)
print('Updated four SVG source diagrams')
