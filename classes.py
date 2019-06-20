import pygame as pg
import varbs

pg.font.init()
font = pg.font.SysFont("comicsansms", 72)




def checkIndex(index):
    return index[1]>=0 and index[1]<8 and index[0]>=0 and index[0]<8

class Timer(pg.sprite.Sprite):
    def __init__(self,startTime,toprightPos):
        pg.sprite.Sprite.__init__(self)
        self.time = startTime
        self.top,self.right = toprightPos[0],toprightPos[1]
        string = "{0:0>2.0f}:{1:0>2.0f}".format(self.time//60,self.time%60)
        self.image = font.render(string,
                                 False,
                                 (0,0,0),
                                 (250,250,250))
        self.rect = self.image.get_rect()
        self.rect.top,self.rect.right = self.top,self.right
        
    def update(self,dt):
        self.time -= dt/1000
        string = "{0:0>2.0f}:{1:0>2.0f}".format(self.time//60,self.time%60)
        self.image = font.render(string,
                                 False,
                                 (0,0,0),
                                 (250,250,250))
        self.rect = self.image.get_rect()
        self.rect.top,self.rect.right = self.top,self.right

class Square(pg.sprite.Sprite):
    def __init__(self,index,occupant):
        pg.sprite.Sprite.__init__(self)
        self.index = index
        self.image = pg.image.load("data/possible.png")
        self.rect = self.image.get_rect()
        self.rect.center = varbs.index_to_centerpixel(*index)
        self.occupant = occupant

class Piece(pg.sprite.Sprite):
    def __init__(self,loc,blacks=False):
        pg.sprite.Sprite.__init__(self)
        self.loc = loc
        self.index = varbs.pixel_to_index(*loc)
        self.indexOld = 1*self.index
        self.blacks=blacks
        self.unmoved = True
        
    def update(self,pos):
        self.rect.center = pos
        
    def place(self,pos):
        #Must be valid location
        try:
            new = varbs.pixel_to_index(*pos)
        except AssertionError:
            return False
        #Must move the piece
        if self.index==new:
            return False
        #Move
        else:
            self.indexOld = 1*self.index
            self.index = 1*new
            self.rect.center = varbs.index_to_centerpixel(*self.index)
            self.unmoved = False
            return True
        
    
class Pawn(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "P"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
    
    def genPossible(self,allP,pActive):
        theirP = [s for s in allP if self.blacks!=s.blacks]
        pos = []
        #Advance
        for dIndex in [[0,(2*self.blacks-1)]]:
            nIndex = self.index[0]+dIndex[0],self.index[1]+dIndex[1]
            # Enforce Board
            if checkIndex(nIndex):
                occ = [s for s in allP if s.index[0]==nIndex[0]\
                                            and s.index[1]==nIndex[1]]
                if len(occ)==0:
                    pos += [[nIndex,[]]]
                    if self.unmoved:
                        nIndex = self.index[0]+dIndex[0],self.index[1]+2*dIndex[1]
                        occ = [s for s in allP if s.index[0]==nIndex[0]\
                                            and s.index[1]==nIndex[1]]
                        if len(occ)==0:
                            pos += [[nIndex,[]]]
        #Capture-able
        for dIndex in [[1,(2*self.blacks-1)],[-1,(2*self.blacks-1)]]:
            nIndex = self.index[0]+dIndex[0],self.index[1]+dIndex[1]
            # Enforce Board
            if checkIndex(nIndex):
                occ = [s for s in theirP if s.index[0]==nIndex[0]\
                                and s.index[1]==nIndex[1]]
                if len(occ)==1:
                    pos += [[nIndex,[occ[0]]]]
        #En Passant
        if self.index[1]==3+self.blacks:
            if pActive.sprite.k == "P" and abs(pActive.sprite.index[1]-pActive.sprite.indexOld[1])==2:
                pos += [[(pActive.sprite.index[0],pActive.sprite.index[1]-(1-2*self.blacks)),[pActive.sprite]]]
        return pos
        
class Rook(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "R"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        
    def genPossible(self,allP,pActive):
        pos = []
        #Advance
        for dIndex in [[0,1],[0,-1],[1,0],[-1,0]]:
            loop = True
            i=1
            while loop:
                nIndex = self.index[0]+i*dIndex[0],self.index[1]+i*dIndex[1]
                # Enforce Board
                if checkIndex(nIndex):
                    occ = [s for s in allP if s.index[0]==nIndex[0]\
                                                and s.index[1]==nIndex[1]]
                    if len(occ)==0:
                        pos += [[nIndex,[]]]
                    elif occ[0].blacks==self.blacks:
                        loop=False
                    else:
                        pos += [[nIndex,[occ[0]]]]
                        loop=False
                else:
                    loop = False
                i+=1
        return pos
        
class Knight(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "N"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
    
    def genPossible(self,allP,pActive):
        pos = []
        #Advance
        for dIndex in [[1,2],[2,1],[-1,2],[-2,1],
                       [1,-2],[2,-1],[-1,-2],[-2,-1]]:
            nIndex = self.index[0]+dIndex[0],self.index[1]+dIndex[1]
            # Enforce Board
            if checkIndex(nIndex):
                occ = [s for s in allP if s.index[0]==nIndex[0]\
                                            and s.index[1]==nIndex[1]]
                if len(occ)==0:
                    pos += [[nIndex,[]]]
                elif occ[0].blacks!=self.blacks:
                    pos += [[nIndex,[occ[0]]]]
        return pos
        
class Bishop(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "B"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        
    def genPossible(self,allP,pActive):
        pos = []
        #Advance
        for dIndex in [[1,1],[1,-1],[-1,1],[-1,-1]]:
            loop = True
            i=1
            while loop:
                nIndex = self.index[0]+i*dIndex[0],self.index[1]+i*dIndex[1]
                # Enforce Board
                if checkIndex(nIndex):
                    occ = [s for s in allP if s.index[0]==nIndex[0]\
                                                and s.index[1]==nIndex[1]]
                    if len(occ)==0:
                        pos += [[nIndex,[]]]
                    elif occ[0].blacks==self.blacks:
                        loop=False
                    else:
                        pos += [[nIndex,[occ[0]]]]
                        loop=False
                else:
                    loop = False
                i+=1
        return pos
        
class Queen(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "Q"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
    def genPossible(self,allP,pActive):
        pos = []
        #Advance
        for dIndex in [[0,1],[0,-1],[1,0],[-1,0],
                       [1,1],[1,-1],[-1,1],[-1,-1]]:
            loop = True
            i=1
            while loop:
                nIndex = self.index[0]+i*dIndex[0],self.index[1]+i*dIndex[1]
                # Enforce Board
                if checkIndex(nIndex):
                    occ = [s for s in allP if s.index[0]==nIndex[0]\
                                                and s.index[1]==nIndex[1]]
                    if len(occ)==0:
                        pos += [[nIndex,[]]]
                    elif occ[0].blacks==self.blacks:
                        loop=False
                    else:
                        pos += [[nIndex,[occ[0]]]]
                        loop=False
                else:
                    loop = False
                i+=1
        return pos
        
class King(Piece):
    def __init__(self,loc,blacks=False):
        Piece.__init__(self,loc,blacks)
        self.k = "K"
        self.image = pg.image.load("data/"+varbs.piece[self.k]+["W","B"][blacks]+".png")
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.startIndex = 1*self.index
        
    def genPossible(self,allP,pActive):
        pos = []
        #Advance
        for dIndex in [[0,1],[0,-1],[1,0],[-1,0],
                       [1,1],[1,-1],[-1,1],[-1,-1]]:
            nIndex = self.index[0]+dIndex[0],self.index[1]+dIndex[1]
            # Enforce Board
            if checkIndex(nIndex):
                occ = [s for s in allP if s.index[0]==nIndex[0]\
                                            and s.index[1]==nIndex[1]]
                if len(occ)==0:
                    pos += [[nIndex,[]]]
                elif occ[0].blacks!=self.blacks:
                    pos += [[nIndex,[occ[0]]]]
        # Castling
        if self.unmoved:
            myRooks = [s for s in allP if s.blacks==self.blacks and s.k=="R" and s.unmoved]
#            print(myRooks)
            for sR in myRooks:
                dx = sR.index[0]-self.index[0]
#                print(dx)
                dX,n = abs(dx)//dx,abs(dx)
                valid = True
                for di in range(1,n):
                    valid = valid and len([s for s in allP if s.index[0]==self.index[0]+di*dX and s.index[1]==self.index[1]])==0
                if valid:
                    pos += [[(self.index[0]+2*dX,self.index[1]),[sR]]]
        return pos
    
promote = {"N":Knight,
            "R":Rook,
            "B":Bishop,
            "Q":Queen}