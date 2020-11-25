import dash_core_components as dcc

content = dcc.Markdown("""
        ## What is the aim of this dashboard?
        To visualize the percentage of significant innings in each of the batting position from 1 to
        11 for every team in the ODI Cricket World Cup History.

        ## What exactly is a Significant Innings?
        Any Innings which is significant enough for the particular match is called a significant Innings. It varies
        based on the match. For a low-scoring match, even a 30 run innings can be considered as significant. However,
        for a high-scoring match, even a half-century may not be good enough to be classified as significant.   
        
        ##  This seems really complicated, how do you mathematically define it?
        For that, I define a cut-off for every match. And every score above that cut-off score is considered significant
        for that particular match. Here is the formula I used for defining the cut-off score.
        
        Cut-off score for the match = max(30, average score in the match)
                                    = max(30, total runs/ total batsman batted in the match)
        
        ##  Can you give me an example?
        Sure. In the [2011 Cricket World Cup final](http://www.howstat.com/cricket/Statistics/WorldCup/MatchScorecard.asp?MatchCode=3283)
        between India and Sri Lanka, Sri Lanka scored 274/6 and India chased it by scoring 277/4. Total runs scored in this
        match is 551 and total batsmen batted is 8+6 = 14. For this match, the cut-off score is max(30, 551/14) = 39.36.
        Every score above this cut-off score will be considered significant for this
        match based on my algorithm. For Sri Lanka, Mahela Jayawardene's 103<sup>`*`</sup> and Kumar Sangakkara's 48 are
        considered significant and for India Gautam Gambhir's 97 and Mahendra Singh Dhoni's 91<sup>`*`</sup> 
        are considered significant.
        
        ##  How do you calculate the significant innings percentage of all batting positions of a team?
        For every match, I calculated 2 Counters for batting position 1 to 11.
        The <b>Significant innings</b> Counter and the <b>Total Innings</b> Counter. Now, this formula is used:
         
         <b>Significant Innings % at batting position 1</b>
        = (sum of Significant innings at batting position 1)/ (sum of Total innings at batting position 1)
        
         This is extended to all the batting positions and for all the matches in the selected World-Cup years.
        
        """, id='article', dangerously_allow_html=True)
