
import classes
import varbs


def InitalizeTimer(blacks=False):
    return classes.Timer(20*60,(varbs.boardyoffset+8*varbs.box-8*varbs.box*blacks,varbs.boardxoffset))


def InitalizePieces(blacks=False):
    pawns = [classes.Pawn(varbs.index_to_centerpixel(i,6-5*blacks),
                          blacks)\
             for i in range(8)]
    rooks = [classes.Rook(varbs.index_to_centerpixel(0,7-7*blacks),
                          blacks),
             classes.Rook(varbs.index_to_centerpixel(7,7-7*blacks),
                                   blacks)]
    knigh = [classes.Knight(varbs.index_to_centerpixel(1,7-7*blacks),
                          blacks),
             classes.Knight(varbs.index_to_centerpixel(6,7-7*blacks),
                                   blacks)]
    bisho = [classes.Bishop(varbs.index_to_centerpixel(2,7-7*blacks),
                          blacks),
             classes.Bishop(varbs.index_to_centerpixel(5,7-7*blacks),
                                   blacks)]
    queen = [classes.Queen(varbs.index_to_centerpixel(3,7-7*blacks),
                          blacks)]
    king = [classes.King(varbs.index_to_centerpixel(4,7-7*blacks),
                          blacks)]
    return pawns+rooks+knigh+bisho+queen+king