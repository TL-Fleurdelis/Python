import pygame, sys, os, random
import pygame.mixer
from datetime import date, datetime

import pyttsx3
engine = pyttsx3.init()
engine.say("Hello guys, this is my game")
engine.say("Turn on music")
engine.runAndWait()
pygame.mixer.init()
pygame.mixer.music.load('./numb.mp3')
pygame.mixer.music.play(-1)        # Plays six times, not five!
# trả về danh sách các chuỗi lưới từ đầu (độc quyền) đến cuối (bao gồm) hoặc danh sách trống nếu không thể truy cập
# A*((0,0), (2,2), [], (3,3)) -> [(1,0),(1,1),(2,1),(2,2)]
def AStar(start,end,walls,size):
    # build entire grid. i.e. cells[(0,0)] holds its grid pos, parent cell, g cost (least moves found to it), h cost (guess distance to end), and if it's a wall.
    # xây dựng toàn bộ lưới. tức là các ô [(0,0)] chứa vị trí lưới của nó, ô mẹ, chi phí g (ít di chuyển nhất được tìm thấy đến nó), chi phí h (đoán khoảng cách đến cuối) và nếu đó là một bức tường.
    cells = {(x,y):{'pos':(x,y),'parent':None,'g':0,'h':max(abs(x-end[0]),abs(y-end[1])),'wall':(x,y) in walls} for y in range(size[1]) for x in range(size[0])}
    opened = [cells[start]]; closed = []; path = [] # opened search, closed search, path filled at end of search
    while opened: # tìm kiếm
        current = min(opened,key=lambda i: i['g']+i['h']); closed.append(current); opened.remove(current) # Lấy ô tốt nhất để tìm kiếm, đánh dấu là đã tìm kiếm
        if current['pos']==end: # kết thúc khi đã đạt được
            while current['parent']: path.append(current['pos']); current = current['parent'] # build path back to start (start doesn't have parent, so isn't added)
            return path[::-1] # return path (không bị đảo ngược)
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)): # kiểm tra các ô điều chỉnh để có thêm các tìm kiếm có sẵn
            x,y = current['pos'][0]+dx,current['pos'][1]+dy # vị trí lưới điều chỉnh
            if x<0 or y<0 or x>=size[0] or y>=size[1]: continue # bỏ qua nếu nằm ngoài lưới
            adj = cells[(x,y)] # dữ liệu ô
            if adj['wall'] or adj in closed: continue # bỏ qua nếu tường hoặc đã được tìm kiếm (các ô đã xếp hàng vẫn có thể được cập nhật)

            # Note: we're skipping searched cells, since it's very unlikely the search will need to backtrack through a path already found.
            # but if you want to, you put them back in the search queue so they can propagate that direction again, if necessary
            # and use new_cell = adj not in opened and adj not in closed (new_cell = not queued and not searched)

            new_cell = adj not in opened # not queued (and we know not searched) meaning we need to search this cell
            new_g = current['g']+1 # adj travel score. diagonals would use 1.4 to be geometrically accurate. (games can scale in other environmens. water/ice/hill)
            # also for diagonals, you'd might want to check no walls block it, to be physically accurate too. (can't pass through walls)

            if new_cell or new_g<adj['g']: adj['parent'] = current; adj['g'] = new_g # new or quicker route, update parent and travel score
            if new_cell: opened.append(adj) # ô mới có thể tìm kiếm
    return [] # no route


class Solver:
    def __init__(self,size):
        self.w,self.h = self.gs = size; self.taketo_cache = None; self.flipped = None
        self.d = [(x,y) for y in range(self.h) for x in range(self.w)]
        self.walls = [(x,y) for y in range(self.h-2) for x in range(self.w-2)]

    def add_moves(self,moves):
        for p in moves: self.c[self.c.index(p)] = self.o; self.o = p; yield p

    def goto(self,pos,walls=[]):
        for i in self.add_moves(AStar(self.o,pos,walls,self.gs)): yield i

    def get_target(self,start,end,walls=[]):
        x,y = start; X,Y = end; dx,dy = (0 if X==x else 1 if X>x else -1),(0 if Y==y else 1 if Y>y else -1)
        targets = ([(x+dx,y)] if dx else [])+([(x,y+dy)] if dy else [])
        for target in targets:
            if target in walls: targets.remove(target)
        return min(targets,key=lambda t:max(abs(self.o[0]-t[0]),abs(self.o[1]-t[1])))

    def taketo(self,c,d,walls=[]):
        self.taketo_cache = (c,self.d[d])
        while self.c[c]!=self.d[d]:
            pos = self.get_target(self.c[c],self.d[d],walls)
            for i in self.goto(pos,walls+[self.c[c]]): yield i
            for i in self.add_moves([self.c[c]]): yield i

    def impossible(self):
        c = list(self.c)
        while c[-1][0]!=self.w-1: x,y = c[-1]; c[-1],c[c.index((x+1,y))] = (x+1,y),c[-1]
        while c[-1][1]!=self.h-1: x,y = c[-1]; c[-1],c[c.index((x,y+1))] = (x,y+1),c[-1]
        order = [c.index(pos) for pos in self.d if pos!=c[-1]]
        inversions = sum(1 for i in range(self.w*self.h-2) for j in order[i+1:] if j<order[i])
        return inversions%2

    def get_moves(self,coords,target_coords=None):
        if coords==target_coords: yield False
        t = list(target_coords) if target_coords else list(self.d); self.last_moves = []

        path = AStar(t[-1],(self.w-1,self.h-1),[],self.gs)
        for pos in path: self.last_moves+=[t[-1]]; n = t.index(pos); t[n],t[-1] = t[-1],t[n]

        self.c = [coords[t.index(pos)] for pos in self.d]; self.o = self.c[-1]
        flat = 1 in self.gs

        if self.impossible():
            print('Impossible To Solve!')
            if not flat: self.flipped = t.index((self.w-1,self.h-2)),t.index((self.w-2,self.h-1))
        else: self.flipped = None

        if flat:
            for i in self.goto(target_coords[-1]): yield i
            yield False

        for i in range(len(self.walls)):
            n = self.d.index(self.walls[i])
            for pos in self.taketo(n,n,self.walls[:i]): yield pos

        for r1,r2,d1,s,r in ((1,2,self.w,self.w*(self.h-2),self.w-2),(self.w,self.w*2,1,self.w-2,self.h-2)):
            for x1 in range(r):
                x1 = s+x1*r1; x2 = x1+d1
                if self.c[x1]!=self.d[x1] or self.c[x2]!=self.d[x2]:
                    for i in self.taketo(x1,x1+r2,self.walls): yield i
                    for i in self.taketo(x2,x1,self.walls): yield i
                    for i in self.taketo(x1,x1+r1,[self.d[x1]]+self.walls): yield i
                    for i in self.goto(self.d[x2],[self.d[x1+r1]]+self.walls): yield i
                    for i in self.goto(self.d[x1+r1],[self.d[x2+r1]]+self.walls): yield i

        for i in self.taketo(-2-self.w,-2-self.w): yield i
        for i in self.add_moves((self.d[-1],)): yield i
        for i in self.add_moves(self.last_moves[::-1]): yield i
        self.taketo_cache = None
        yield False

GLOBAL_FONT = 'C:/Windows/Fonts/segoepr.ttf' # sử dụng none để làm mặc định

class SlidePuzzle:
    previus = None
    moves = None
    speed = 20
    autoSpeed = 8 # tốc độ 

    def __init__(self,screen,gs,ts,ms):
        self.gs,self.ts,self.ms = gs,ts,ms; self.s = int(ts*0.15); self.s2 = self.s//2
        self.w,self.h = self.gs; self.tile_center = (ts//2,ts//2); self.len_tiles = self.w*self.h-1
        self.solved_coords = [(x,y) for y in range(self.h) for x in range(self.w)]
        self.solver = Solver(gs)

        self.rect = pygame.Rect(0,0,self.w*(ts+ms)+ms,self.h*(ts+ms)+ms)
        self.target = {(x,y):[x*(ts+ms)+ms,y*(ts+ms)+ms] for y in range(self.h) for x in range(self.w)}
        self.reset()
        self.gen_images(self.coords)

    def gen_images(self,coords=None):
        if not coords: coords = self.solved_coords
        gs,ts,ms = self.gs,self.ts,self.ms
        font_dir = GLOBAL_FONT; image_dir = "image.jpg" #hình ảnh của câu đố ,có thể muốn triển khai tỷ lệ cắt trên bảng, thay vì kéo dài hình ảnh)
        font_max = 200; font_percent = 0.75; factor = ts*font_percent*font_max

        font = pygame.font.Font(font_dir,font_max)
        self.image = pygame.transform.smoothscale(pygame.image.load(image_dir),self.rect.size); self.images = []

        for i in range(len(coords)):
            x,y = coords[i]; number = str(i+1); tile_image = self.image.subsurface(x*(ts+ms)+ms,y*(ts+ms)+ms,ts,ts)
            #Hiển thị số trong trường hợp không muốn insert ảnh 
            #text = pygame.font.Font(font_dir,int(factor/max(font.size(number)))).render(number,2,(40,180,240)) # text color. may want to change for given image
            #tile_image.blit(text,text.get_rect(center=self.tile_center));
            self.images+=[tile_image]

    def reset(self):
        self.stop()
        ts = self.ts; ms = self.ms
        self.tilepos = [[x*(ts+ms)+ms,y*(ts+ms)+ms] for y in range(self.h) for x in range(self.w)]
        self.coords = [(x,y) for y in range(self.h) for x in range(self.w)]

    def getBlank(self): return self.coords[-1]
    def setBlank(self,pos): self.coords[-1] = pos
    opentile = property(getBlank,setBlank)

    def switch(self,pos,solving=False):
        number = self.coords.index(pos)
        self.coords[number],self.opentile,self.previus = self.opentile,self.coords[number],self.opentile
        if not solving: self.stop()

    def adjacent(self,x,y): return tuple((X,Y) for X,Y in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if self.in_grid(X,Y))
    def in_grid(self,x,y): return x>=0 and x<self.w and y>=0 and y<self.h

    def randomize(self,amount=1):
        for loop in range(amount):
            if self.w==1 or self.h==1: self.previus = None
            adjacent = self.adjacent(*self.opentile); adj = tuple(i for i in adjacent if i!=self.previus)
            if adj: self.switch(random.choice(adj))

    def moveable(self):
        for i in range(self.len_tiles):
            if self.tilepos[i]!=self.target[self.coords[i]]: return False
        return True

    def slidetiles(self):
        for i in range(self.len_tiles):
            a,b = self.tilepos[i],self.target[self.coords[i]]
            if a==b: continue
            for j in range(2): a[j] = b[j] if abs(a[j]-b[j])<self.speed else a[j]+self.speed if a[j]<b[j] else a[j]-self.speed

    def teleport(self):
        for i in range(self.len_tiles): self.tilepos[i] = list(self.target[self.coords[i]])

    def set_target(self,coords=None): self.solved_coords = list(coords) if coords else list(self.coords)

    def solve(self): self.play(self.solver.get_moves(self.coords,self.solved_coords))
    def play(self,moves): self.moves = moves
    def stop(self): self.moves = None; self.time = 0; self.solving = False

    def events(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: self.reset()
            elif event.key == pygame.K_l: self.randomize(2000)
            elif event.key == pygame.K_o: self.set_target()
            elif event.key == pygame.K_p: self.gen_images(self.coords)
            elif event.key == pygame.K_RETURN: self.stop() if self.moves else self.solve()
            else:
                for key,dx,dy in ((pygame.K_a,-1,0),(pygame.K_d,1,0),(pygame.K_w,0,-1),(pygame.K_s,0,1)):
                    if event.key==key:
                        self.stop()
                        if not self.moveable(): break
                        x,y = self.opentile[0]+dx,self.opentile[1]+dy
                        if self.in_grid(x,y): self.switch((x,y))
                        break

    def update(self,dt,key,mouse,mpos):
##        if key[pygame.K_UP]:    self.rect.y-=self.speed
##        if key[pygame.K_DOWN]:  self.rect.y+=self.speed
##        if key[pygame.K_LEFT]:  self.rect.x-=self.speed
##        if key[pygame.K_RIGHT]: self.rect.x+=self.speed
        if key[pygame.K_SPACE]: self.randomize(2)

        moveable = self.moveable()

        if not moveable: self.slidetiles()

        elif mouse[0]:
            s = self.ts+self.ms; x,y = mpos[0]-self.rect.x,mpos[1]-self.rect.y
            if x%s>self.ms and y%s>self.ms:
                tile = x//s,y//s
                if self.in_grid(*tile):
                    for i in range(2):
                        while tile[i]==self.opentile[i] and self.opentile[i-1]!=tile[i-1]:
                            self.switch(tuple((self.opentile[d]+(0 if i==d else 1 if tile[d]>self.opentile[d] else -1)) for d in (0,1)))

        elif mouse[2]:
            s = self.ts+self.ms; x,y = mpos[0]-self.rect.x,mpos[1]-self.rect.y
            if x%s>self.ms and y%s>self.ms:
                tile = x//s,y//s
                if self.in_grid(*tile): self.switch(tile)

        if self.moves:
            self.time+=dt*self.autoSpeed; n = 0
            while self.time>=1: self.time-=1; n+=1

            for i in range(n):
                pos = next(self.moves)
                if pos: self.switch(pos,True); self.solving=True
                else: self.stop(); break

    def draw_tile(self,screen,pos,color,t=0): pygame.draw.rect(screen,color,(self.rect.x+pos[0],self.rect.y+pos[1],self.ts,self.ts),t)

    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.rect)
        for i in range(self.len_tiles): x,y = self.tilepos[i]; screen.blit(self.images[i],(self.rect.x+x,self.rect.y+y))

        if self.solving:
            cache = self.solver.taketo_cache
            if cache:
                self.draw_tile(screen,self.target[cache[1]],(255,0,0),4)
                self.draw_tile(screen,self.tilepos[self.coords.index(self.solver.c[cache[0]])],(0,255,0),4)

            if self.solver.flipped:
                for i in (0,1): self.draw_tile(screen,self.tilepos[self.solver.flipped[i]],((255,255,0),(0,255,255))[i],4)


def CreateText(text,size,color=(0,0,0),bgcolor=(0,0,0,0),font=None):
    s = 200; factor = s*max(size)*0.85; f = pygame.font.Font(font,s); center = (size[0]//2,size[1]//2)
    image = pygame.Surface(size).convert_alpha(); image.fill(bgcolor)
    text = pygame.font.Font(font,int(factor/max(f.size(text)))).render(text,2,color)
    image.blit(text,text.get_rect(center=center)); return image


class Button:
    def __init__(self,pos,size,functions,text):
        self.x,self.y = pos; self.w,self.h = size
        self.functions = functions if hasattr(functions,'__iter__') else (functions,)
        self.right,self.bottom = self.x+self.w,self.y+self.h
        self.image = CreateText(text,size,color=(0,255,0),font=GLOBAL_FONT)

    def __call__(self,*args):
        for function in self.functions: function(*args)

    def collide(self,pos): return pos[0]>=self.x and pos[0]<self.right and pos[1]>=self.y and pos[1]<self.bottom

    def draw(self,screen,color=(40,180,240)):
        rect = (self.x,self.y,self.w,self.h)
        if not self.collide(pygame.mouse.get_pos()): color = (0,0,0)
        pygame.draw.rect(screen,color,rect)
        screen.blit(self.image,rect)
        pygame.draw.rect(screen,(40,100,180),rect,4)


class AStarGridTest:
    def __init__(self,gs,ts,ms,fs):
        self.gs,self.ts,self.ms = gs,ts,ms; self.tm = tm = ts+ms; self.ts2 = ts//2
        self.tilepos = {(x,y):[x*tm+ms,y*tm+ms] for y in range(gs[1]) for x in range(gs[0])}
        self.reset()
        
        self.font = pygame.font.Font('C:/Windows/Fonts/Arial.ttf',fs)

        self.speed = 10
        self.x,self.y = 1200-400-50,100
        self.image = pygame.Surface((gs[0]*tm+ms,gs[1]*tm+ms),pygame.SRCALPHA)
        for x,y in self.tilepos: x,y = self.tilepos[(x,y)]; pygame.draw.rect(self.image,(255,255,255),(x,y,ts,ts))

    def reset(self):
        self.start,self.end = (0,0),(self.gs[0]-1,self.gs[1]-1)
        self.tiles = []

    def events(self,event):
        pass
##        if event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_BACKSPACE: self.tiles = []
##            elif event.key == pygame.K_RETURN: self.x,self.y = 0,0
##            elif event.key == pygame.K_p: print(self.tiles)

    def get_tile(self,pos):
        tx,mx = divmod(pos[0]-self.x,self.tm); ty,my = divmod(pos[1]-self.y,self.tm)
        if mx>self.ms and my>self.ms and tx>=0 and tx<self.gs[0] and ty>=0 and ty<self.gs[1]: return tx,ty

    def update(self,key,mouse,mpos):
##        if key[pygame.K_w]: self.y-=self.speed
##        if key[pygame.K_s]: self.y+=self.speed
##        if key[pygame.K_a]: self.x-=self.speed
##        if key[pygame.K_d]: self.x+=self.speed

        if key[pygame.K_1]:
            tile = self.get_tile(mpos)
            if tile: self.start = tile

        if key[pygame.K_2]:
            tile = self.get_tile(mpos)
            if tile: self.end = tile

        if mouse[0] and not mouse[2]:
            tile = self.get_tile(mpos)
            if tile and tile not in self.tiles: self.tiles.append(tile)
        elif mouse[2] and not mouse[0]:
            tile = self.get_tile(mpos)
            if tile and tile in self.tiles: self.tiles.remove(tile)

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

        for x,y in self.tiles: x,y = self.tilepos[(x,y)]; pygame.draw.rect(screen,(0,0,255),(self.x+x,self.y+y,self.ts,self.ts))

        path = AStar(self.start,self.end,self.tiles,self.gs)
        for i in range(len(path)-1):
            x,y = self.tilepos[path[i]]; pygame.draw.rect(screen,(255,255,0),(self.x+x,self.y+y,self.ts,self.ts))
            text = self.font.render(str(i+1),2,(0,0,0)); w,h = text.get_size(); t = self.ts2
            screen.blit(text,(self.x+x+t-w//2,self.y+y+t-h//2))

        for i in (0,1):
            x,y = self.tilepos[(self.start,self.end)[i]]; pygame.draw.rect(screen,(255,0,0) if i else (0,255,0),(self.x+x,self.y+y,self.ts,self.ts))
            text = self.font.render('AB'[i],2,(0,0,0)); w,h = text.get_size(); t = self.ts2
            screen.blit(text,(self.x+x+t-w//2,self.y+y+t-h//2))


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    w,h = 1200,600; cx,cy = w//2,h//2
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption('Puzzle Game')
    fpsclock = pygame.time.Clock(); fps = 60
    puzzle = SlidePuzzle(screen,(4,4),120,2)
    puzzle.rect.center = 300,cy

    AstarTEST = AStarGridTest((10,10),40,1,32) # grid size, tile size, margin size, font size

    x,y = 600,70; size = 100,100
    buttons = {}
    buttons['solve']     = Button((x,y),     size, puzzle.solve,                          'Cheat')
    buttons['stop']      = Button((x,y),     size, puzzle.stop,                           'Stop')
    buttons['scrammble'] = Button((x,y+120), size, puzzle.randomize,                      'Random')
    buttons['target']    = Button((x,y+240), size, (puzzle.set_target,puzzle.gen_images), 'Set Target')
    buttons['reset']     = Button((x,y+360), size, AstarTEST.reset,                       'Reset A*')

    bg = pygame.image.load("background.jpg")
    bg_w,bg_h = bg.get_size()

    while True:
        dt = fpsclock.tick(fps)/1000
        pygame.display.set_caption('%s - FPS %.2f'%('Slide Puzzle',fpsclock.get_fps()))
        key = pygame.key.get_pressed(); mouse = pygame.mouse.get_pressed(); mpos = pygame.mouse.get_pos()

        solve = buttons['stop' if puzzle.solving else 'solve']
        collide = None
        for b in (solve,buttons['target'],buttons['scrammble'],buttons['reset']):
            if b.collide(mpos): collide = b; break

        for y in range(0,h,bg_h):
            for x in range(0,w,bg_w): screen.blit(bg,(x,y))

        puzzle.draw(screen)
        solve.draw(screen,(180,0,0) if puzzle.solving else (0,180,0))
        buttons['scrammble'].draw(screen,(60,70,160))
        buttons['target'].draw(screen,(120,60,180))
        buttons['reset'].draw(screen,(70,120,110))

        AstarTEST.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and key[pygame.K_LALT]: pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if collide:
                    if collide is buttons['scrammble']: collide(1000)
                    else: collide()
            puzzle.events(event)
            AstarTEST.events(event)

        puzzle.update(dt,key,mouse,mpos)
        AstarTEST.update(key,mouse,mpos)


if __name__ == '__main__':
    main()



