#www.slothparadise.com/nba_py-documentation/
import nba_py as nba
from nba_py.constants import CURRENT_SEASON
from nba_py import game
summary = game.BoxscoreSummary("0021600457")
print(summary.game_summary())
'''sc = nba.Scoreboard(month=1,day=30,year=2017,league_id='00',offset=0)
warriors = 1610612744
roster = nba.commonteamroster(Season=2017,TeamID=warriors)
print roster'''
