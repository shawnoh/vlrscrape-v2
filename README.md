# vlrscrape-v2
scrapes vlr.gg for team ratings

#created by shawn oh, 2020

webscrapes the website vlr.gg for the ELO ratings of pro teams.
this elo is not official to the VALORANT leagues, but rather is calculated using the elo system by vlr.gg separately (third party).
using statistics calculations with standard deviation, the given amount of teams is split into groups that approximate which teams belong in which tiers and graphs it.
pandas is NOT used for this grouping, since i wanted to develop my own algorithm.
