#%%

totalTime = 20#minutes

boardxoffset = 100+50
boardyoffset = 30
boardW = 360
boardH = 360
boxoffset = 20
box = 40

screenW = boardW+boardxoffset+4*40
screenH = boardH+2*boardyoffset

fps=30

piece = {"P":"pawn",
         "R":"rook",
         "N":"knight",
         "B":"bishop",
         "R":"rook",
         "Q":"queen",
         "K":"king"}

def pixel_to_index(px,py):
    px2,py2 = px-(boardxoffset+boxoffset),py-(boardyoffset+boxoffset)
    assert (px2>=0 and px2<=8*box)\
            and (py2>=0 and py2<=8*box),\
            "pixel not in board"
    return px2//box,py2//box
def index_to_centerpixel(x,y):
    assert (x>=0 and x<8)\
            and (y>=0 and y<8),\
            "square not in board"
    px2,py2 = box*x+box//2,box*y+box//2
    return px2+(boardxoffset+boxoffset),py2+(boardyoffset+boxoffset)