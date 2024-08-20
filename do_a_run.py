import page_parser
import sys

next_game = 'https://j-archive.com/showgame.php?game_id={}'.format(sys.argv[1])
for n in range(0, int(sys.argv[2])):
    next_game = page_parser.parse_page(next_game)
