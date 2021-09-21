import pandas as pd
import numpy as np

df = pd.read_csv('FantasyPros_Fantasy_Football_Points_2021.csv')  # already sorted on points / week

#  create a subset of each position group that represents the caliber of player likely to be starting against you each week
#  10 teams in a league, each team has one QB. Likely you will be facing a top-10 fantasy QB in league in a given week
rb = df.loc[df['Position'] == 'RB', :][:22]
qb = df.loc[df['Position'] == 'QB', :][:12]
wr = df.loc[df['Position'] == 'WR', :][:22]
te = df.loc[df['Position'] == 'TE', :][:12]

#  outside of the top 20 WR's and RB's, add in some additional players in these position groups to fill FLEX spots
flx = df.loc[ (df['Position'] == 'RB') | (df['Position'] == 'WR') , :]
flx = flx[ ~ ( flx.Player.isin(rb.Player) | flx.Player.isin(wr.Player) ) ]

flx = flx[:12]

for df in [rb, qb, wr, te, flx]:
    df.insert(7, "Pos. Mean", np.repeat(0, len(df)))
    #  calculate points / week among position group, BUT remove given player from position group
    #  avg is estimate of players you will likely face at that position group, and you won't face your own player
    for i in range(len(df)):
        df.iloc[i, 7] = (sum( df['Avg']) - list(df['Avg'] )[i]) / (len(df) - 1)
        
for df in [rb, qb, wr, te, flx]:
    df.insert(8, "Diff", np.repeat(0, len(df)))
    #  calculate difference between given players expected points / week and that of his position group
    for i in range( len(df) ):
        df.iloc[i, 8] = df.iloc[i, 6] - df.iloc[i, 7]

df = pd.concat([rb, qb, wr, te])

with pd.ExcelWriter('fantasy_cheatsheet_2021.xlsx') as writer:  
    #  export pandas DataFrame to xlsx workbook, one worksheet for potential starters and another for flex
    df.to_excel(writer, sheet_name = 'Starters')
    flx.to_excel(writer, sheet_name = 'Flex')
