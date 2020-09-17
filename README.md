# vlrscrape-engine-v2
scrapes vlr.gg for team ratings

#created by shawn oh, 2020

webscrapes the website vlr.gg for the ELO ratings of professional VALORANT teams.
this elo is not official to the VALORANT professional leagues, but rather is calculated using the elo system by vlr.gg separately (third party), based off tournament results.
using statistics calculations with standard deviation, the teams are split into groups that approximate which teams belong in which tiers and graphs it.
pandas is NOT used for this grouping, since i wanted to develop my own algorithm. selected region and maximum teams displayed are modifiable in settings. due to the recursive nature of my algorithm and the elo disparity between certain top tier teams, the amount of resulting tiers may not be as expected.
