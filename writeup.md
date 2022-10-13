# How social and economic factors impact innovation in America? <br />
We used data source from Social mobility in the U.S.(https://opportunityinsights.org/data/ ). Specifically, our team has focused on two main aspects - neighborhood commuting zone & parent income.
By visualizing the relationship between commuting zone and innovation rate and parental income and their children innovation rate, we are able to conclude that neighborhood and parent income do impact innovation in America. <br />

- East and west coast have higher invention rates than other parts of the U.S.  <br />
- The higher income of a parent, the great possibility that his/her children would become inventors.

### Based on the interactive charts from our app, Vermont is the 1st inventor state in the U.S. 
![image](https://user-images.githubusercontent.com/75749274/195476987-e54a8120-7b2f-4975-9e57-b92aedbe7705.png)
## Project Goals

Innovation is widely viewd as the engine of economic growth, many investments are used to develop STEM education. However, without knowing what factors induce children to become inventors, the effectiveness of STEM education is unclear. The goal of this project is to look at the relationship among child commuting zone, parental income and innovation rates by states in America. 


## Design

Define a goal by reviewing the dataset, then discover insights by asking various hypotheses and testing them out.
### Part1. The relationship between commuting zone & state and innovation rates
We use a point chart to list states on the y-axis and the mean of grant_rate on the x-axis. This design helps users easily spot which state(s) has the highest average grant rate. Then we pick the top three states to dig deeper from both invention quantity and invention quality (top 5% of patent citation) perspective.

### Part2. The relationship between parent income and children innovation rate
The intention for this part to show how parent's income affect children innovation. The original dataset divides all parent's into five categories, top 20%, 20%-40%, 40%-60%, 60%-80% and the bottom 20%. We want our audience to make comparison between two income categories to see the differences in children invention rate. We make two bar charts side by side, one is reference group and another one is the experiment group. By keep the reference group the same such as choosing it as the top 20% income, and change the experiment group to 20-40%, 40-60%, 60-80% or bottom 20%, we can see the difference. After the exploration, our audience will find that the higher parent income, the higher children innovation rate. The alternative method of showing the relationship between parent income and children innovation rate is to use a bar chart with five columns, each representing top 20%, 20%-40%, 40%-60%, 60%-80% and the bottom 20%. However, showing these with all states would make the charts too busy. And it is hard for the audience to explore the relationship by themselves. Therefore, we did not choose this method. 

### Part3. The relationship between the year of birth and innovation
We use multiple line charts to show the relationship between birth year and the average number of patents granted per individual. By adding age as the color category, this chart shows that 1963 is the year of birth with the most average number of grants, and inventors aged 40 are the most productive. Initially, I chose point chart instead of the line chart, but it isn't easy to find insights from many data points. 

## Development

We had three meetings in total for this project from begin to finish.  <br />
### Meeting 1. We made a decision on the datasets and split the workload 
-	Cuiting: discover how parent income impact innovation
-	Haoyu: find how childhood commuting zone and cohort impact innovation 
### Meeting 2. Check-in on each other's progress
### Meeting 3. Review each other's work and finalize the app

Efforts		


| Team Member     | Efforts                        | Aspects took the most time                           |
| :---            |    :----:                      |          ---:                                        |
| Haoyu Wang      | 25h                            | Dataset EDA and build meaningful interactive charts  |
| Cuiting Li      | 15h                            | Build and Refine Interaction                         | 

Haoyu: 
- 10/7    Dataset Discover : 3h 
- 10/8    Meeting #1 + EDA : 5h
- 10/9    Meeting #2 + Build Interactive App: 5h
- 10/10   Improve App + TA: 3h
- 10/11   Improve App + Writeup: 6h	
- 10/12   Finalize : 3h

Cuiting:
- 10/8    Meeting #1 + EDA : 2h
- 10/10   Build Interaction: 5h
- 10/11   refine Interaction: 5h
- 10/13   Finalize and finish write-up 3h


## Success Story

The neighborhood does impact innovation in America. East and West coast have higher invention rates than other parts of the U.S.  Based on the interactive charts from our app, Vermont is the 1st inventor state in the U.S.  Massachusetts ranks 2nd place with a focus on the Drugs and Medical patent category. The outstanding performance in the Computers and Communications field wins California 3rd place.  <br />
By selecting different parent income in two columns, we can clearly see that parent income has a significant impact on children invention rate. The higher income of a parent, the great possiblity that his/her children would become inventors. 

### Something interesting: 
• The birth year between 1960 and 1965 has the highest average number of patent grants per individual; Inventors aged around 40 are most productive based on the average number of patent grants per individual 😎.  <br />
• Massachusetts is the Drugs and Medical inventor incubator state (0.0013); And California, no surprise, is the state where Computers and Communications inventors grew up. 
• Parent's income in the top 20% can raise almost same amount children with parents in 20-40%, 40-60%, 60-80% and bottom 20% combined together. 

### Next Steps
- Discover Innovation Rates by College
- Discover male and female innovator distributions in different innovation categories 

