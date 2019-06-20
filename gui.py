#%%
import tkinter as tk
from tkinter import messagebox
import pygame as pg
from pygame.locals import *
import varbs
import classes
import initalize
#%%

def main():
    pg.init()
    screen = pg.display.set_mode((varbs.screenW, varbs.screenH))
    pg.display.set_caption("Chess for Chumps")
    #
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))
    background.blit(pg.image.load('data/board.png'),
                    (varbs.boardxoffset, varbs.boardyoffset))
    
    #Initalize
    whites = pg.sprite.Group(initalize.InitalizePieces(False))
    blacks = pg.sprite.Group(initalize.InitalizePieces(True))
    alive = pg.sprite.RenderUpdates(whites.sprites()+blacks.sprites())
    dead = pg.sprite.RenderUpdates([])
    active = pg.sprite.RenderUpdates([])
    pActive = pg.sprite.GroupSingle([])
    available = whites
    wTimer = initalize.InitalizeTimer(False)
    bTimer = initalize.InitalizeTimer(True)
    timers = pg.sprite.RenderUpdates([wTimer,bTimer])
    activeTimer = pg.sprite.Group([wTimer])
    possSquares = pg.sprite.RenderUpdates([])
    #
    screen.blit(background, (0,0))
    alive.draw(screen)
    pg.display.update()
    #
    clock = pg.time.Clock()
    
    
    while 1:
        dt = clock.tick(varbs.fps)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return
            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:
                    try:
                        x,y = varbs.pixel_to_index(*event.pos)
                    except AssertionError:
                        x,y = -1,-1
                    if len(active.sprites())==0:
                        clicked = [s for s in available.sprites()\
                                   if s.index[0]==x and s.index[1]==y]
                        if len(clicked)==1:
                            possSq = clicked[0].genPossible(alive,pActive)
                            #Only pickup movable pieces
                            if len(possSq)!=0:
                                for sq in possSq:
                                    possSquares.add(classes.Square(*sq))
                                active.add(clicked[0])
                            
                    else:
                        possMove = [sq for sq in possSquares.sprites()\
                                    if sq.index[0]==x and sq.index[1]==y]
                        # must be valid move
                        if len(possMove)==0:
                            pass
                        # Place piece
                        elif active.sprites()[0].place(event.pos):
                            # Perform Piece adjustments
                            if len(possMove[0].occupant)==1:
                                # Capture
                                if possMove[0].occupant[0].blacks != active.sprites()[0].blacks:
                                    captS = possMove[0].occupant[0]
                                    captS.kill()
                                    t = captS.blacks
                                    n = len([s for s in dead if s.blacks==t])
                                    dead.add(captS)
                                    captS.rect.center = varbs.boardxoffset\
                                                                +2*varbs.boxoffset\
                                                                +7*varbs.box\
                                                                +varbs.box//2\
                                                                +((n%4)+1)*varbs.box,\
                                                             varbs.boardyoffset\
                                                                +varbs.boxoffset\
                                                                +varbs.box//2\
                                                                +t*7*varbs.box\
                                                                +(1-2*t)*(n//4)*varbs.box
                                # Perform Castle
                                else:
                                    possMove[0].occupant[0].indexOld = 1*possMove[0].occupant[0].index
                                    x,y = active.sprites()[0].index
                                    possMove[0].occupant[0].index = x+(1-2*(x>3)),1*y
                                    possMove[0].occupant[0].rect.center = varbs.index_to_centerpixel(*possMove[0].occupant[0].index)
                                    possMove[0].occupant[0].unmoved = False
                            # Check for promotion
                            if active.sprites()[0].k=="P" and (active.sprites()[0].index[1]==0 or active.sprites()[0].index[1]==7):
                                root = tk.Tk()
                                root.wm_withdraw()
                                l = messagebox.askquestion('Promotion',
                                                           'Promote to Queen?\n(else Knight)')
                                if l=="yes":
                                    np = classes.Queen(active.sprites()[0].rect.center,
                                                       active.sprites()[0].blacks)
                                else:
                                    np = classes.Knight(active.sprites()[0].rect.center,
                                                        active.sprites()[0].blacks)
                                root.destroy()
                                active.clear(screen,background)
                                active.sprites()[0].kill()
                                active.empty()
                                active.add(np)
                                alive.add(np)
                                available.add(np)
                            # Update associations
                            pActive.add(active.sprites()[0])
                            active.remove(active.sprites()[0])
                            activeTimer.remove(activeTimer.sprites()[0])
                            possSquares.clear(screen,background)
                            possSquares.empty()
                            if available == whites:
                                available = blacks
                                activeTimer.add(bTimer)
                            else:
                                available = whites
                                activeTimer.add(wTimer)
                    
        
        # Clear
        alive.clear(screen,background)
        dead.clear(screen, background)
        timers.clear(screen,background)
        possSquares.clear(screen,background)
        # Update
        active.update(pg.mouse.get_pos())
        activeTimer.update(dt)
        # Draw
        dirty_rects = timers.draw(screen)
        dirty_rects += possSquares.draw(screen)
        dirty_rects += dead.draw(screen)
        dirty_rects += alive.draw(screen)
        #Flip display
        pg.display.update(dirty_rects)
        
#%%
if __name__ == "__main__":
    main()