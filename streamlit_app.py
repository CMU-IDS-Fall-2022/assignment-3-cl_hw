import streamlit as st
st.set_page_config(layout="wide")  # increase the width of web page
import pandas as pd
import numpy as np
import altair as alt
from re import U
from PIL import Image

st.title("What are the factors that can impact innovation in America?")
image = Image.open('unleashing-innovation-image.jpg')
# the code to center the image is referenced from  https://discuss.streamlit.io/t/how-to-center-images-latex-header-title-etc/1946/6
col1, col2, col3 = st.beta_columns([1,6,1])

with col1:
st.write("")

with col2:
st.image(image, caption ='Innovation')
    
with col3:
st.write("")

st.image(image, caption ='Innovation')

st.write("We will explore this question in three parts - children exposure to innovation, parent income, and the year inventors were born ")
st.write()
@st.cache(allow_output_mutation=True)  # add caching so we load the data only once
def load_data(file_path):
    return pd.read_csv(file_path)
@st.cache
def get_slice_membership(df, states, cohort_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.
    
    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)

    if states:
        labels &= df['state'].isin(states)
    if cohort_range is not None:
        labels &= df['cohort'] >= cohort_range[0]
        labels &= df['cohort'] <= cohort_range[1]
    return labels

########################################################################################################################################
############################################################### Main Code ##############################################################
########################################################################################################################################

################################################################  Part II  #############################################################
st.header("Part1. The Importance of Exposure to Innovation")
df = load_data('Innovation by Current State, Year of Birth and Age.csv')
st.text("Let's look at the dataset - Innovation Rates by Current State, Year of Birth and Age")

# show dataframe or not
if st.checkbox("Show Raw Data"):
    st.write(df)
st.header("Which neighborhoods in America offer children the best chance to become inventors?")
st.subheader("Which state has the highest average number of grants per individual over the years?")

df['num_of_grantee'] = np.round(df['count'] * df['num_grants'],0)
data_subset = df[["state", "count", "num_of_grantee"]]
data_sums = data_subset.groupby("state").aggregate("sum")
data_sums["grant_rate"] = np.round(data_sums["num_of_grantee"]/data_sums["count"], 4)
data_sums = data_sums.reset_index()


brush = alt.selection(type='interval', encodings =['x'])
avg_grant_rate_by_state =  alt.Chart(data_sums).mark_point().encode(
                                 y=alt.Y("state", sort='-x', scale=alt.Scale(zero=False)),
                                 x=alt.X(field = "grant_rate", title='average grant rate', scale=alt.Scale(zero=False)),
                                 color = alt.Color("grant_rate:Q")
                                ).properties(
                                    width=900, height=800
                                ).add_selection(brush).interactive()

# st.write(avg_grant_rate_by_state)

st.subheader("The top 3 states are Vermont, Masschusetts and California")
st.markdown("*The pink line shows the overall mean")
st.subheader("It is not surprising that MA and CA are within the top states, but why Vermont? \
              Let us dig deeper to find out possible reasons.")


st.write("Dataset -> Inventors in America: Innovation Rates by Childhood Commuting Zone, Gender, and Parent Income")
inventor = load_data('invention.csv')
if st.checkbox("Hit me if you want to see raw data"):
    st.write(inventor)


avg_inventor_state_chart = alt.Chart(inventor).mark_bar().encode(
   y= alt.Y("par_state", title = "Childhood State"),
   x= alt.X("average(inventor)", title = "Average Inventor Rate by State")
).transform_filter(
   alt.FieldOneOfPredicate(field='par_state', oneOf =['Vermont', 'California', 'Massachusetts'])
).properties(
   height=200, width=360
)

top5Cited_chart = alt.Chart(inventor).mark_bar().encode(
   y= alt.Y("par_state", title = "Childhood State"), 
   x= alt.X("average(top5cit)", title = "Average Highly Cited Inventor Rate by State")
).transform_filter(
   alt.FieldOneOfPredicate(field='par_state', oneOf =['Vermont', 'California', 'Massachusetts'])
).properties(
   height=200, width=360
)

# Go horizontal with columns: referenced from https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
cols = st.columns(2)
with cols[0]:
    st.write(avg_inventor_state_chart, use_column_width=True)
with cols[1]:
    st.write(top5Cited_chart,use_column_width=True)

st.subheader("Vermont has the highest average inventor rate and Masschusetts\
            is the No.1 state with the highest average top 5 citation rate")


st.subheader("Let us look into commuting zones for these top 3 states(CA, MA and VT)")
top5Cited_zone = alt.Chart(inventor).mark_bar().encode(
   alt.Y("par_czname", sort = '-x' , title = 'Childhood Commuting Zone of Residence'), # descending order
   alt.X("average(top5cit)", title = "Average Highly Cited Inventor Rate")
).transform_filter(
   alt.FieldOneOfPredicate(field='par_state', oneOf =['Vermont', 'California', 'Massachusetts'])
).properties(
   height=360, width=600
)
st.write(top5Cited_zone)

st.text("let us add a state brush then we will know which zone is from which state")
state_brush = alt.selection_multi(fields=['par_state'])
zone_brush = alt.selection_multi(fields=['par_czname'])

top3State = ['Vermont', 'California', 'Massachusetts']
top3InventorState = inventor[inventor['par_state'].isin(top3State)]


state_chart = alt.Chart(top3InventorState).mark_bar().encode(
    x= alt.X("average(top5cit)", title = "average highly cited rates by state"),
    y= alt.Y('par_state', sort='x', title = "Childhood State"),
    color= alt.condition(state_brush, alt.value('steelblue'), alt.value('lightgray'))
).transform_filter(zone_brush).add_selection(state_brush).interactive()

zone_chart = alt.Chart(top3InventorState).mark_bar().encode(
    x= alt.X('average(top5cit)', title ="average highly cited rates by zone"),
    y= alt.Y('par_czname', sort='-x', title = "Childhood Commuting Zone of Residence"),
    color= alt.condition(zone_brush, alt.value('pink'), alt.value('lightgray'))
).transform_filter(state_brush).add_selection(zone_brush).interactive()

st.altair_chart(state_chart & zone_chart)

st.markdown(
    """
    ###     From interactive charts above, we can see that childhood commuting zone of residence: \
              Oak Bluffs in MA is No.1 with highest share of children with patent\
              citations in the top 5 percent of their birth cohort (using total number of citations).\
              Let us find out which inventor cateogry(s) contribute to this result :smile:
    """
            )

top5_CZ = ['Oak Bluffs', 'Claremont', 'Burlington', 'San Francisco', 'Santa Barbara']
top_state = ['CA', 'MA', 'VT']
top5Zone = inventor[inventor['par_czname'].isin(top5_CZ)]
top5ZoneState = top5Zone[top5Zone['par_stateabbrv'].isin(top_state)]
st.text("top5cit_zone & state")
st.write(top5ZoneState)


top5ZoneState_top5cit = top5ZoneState[['par_czname', 'top5cit_cat_1','top5cit_cat_2','top5cit_cat_3','top5cit_cat_4','top5cit_cat_5','top5cit_cat_6','top5cit_cat_7']]

top5ZoneState_top5cit["id"] = top5ZoneState_top5cit.index
top5_cit_category = pd.wide_to_long(top5ZoneState_top5cit,["top5cit_cat_"], i = "id", j ="seq")
top5_cit_category_sorted = top5_cit_category.sort_values(['par_czname', 'top5cit_cat_'], ascending=[True, False])
st.text("top5_cit_zone sorted by commuting zone name (ascending) and technology patent category value (descending)")
st.write(top5_cit_category_sorted)

st.text("-> Burlington, VT has three highly cited category which are 4 -Electrical and Electronic, 2-Computers and Communications , 5-Mechanical ")
st.text("-> Claremont, VT has three highly cited category which are 6- others, 7 - Design and Plant, 3 - Drugs and Medical")
st.text("-> Oak Bluffs, MA has one highly cited category which is 3 - Drugs and Medical")
st.text("-> San Francisco, CA has one highly cited category which is 2 - Computers and Communications ")
st.text("-> Santa Barbara, CA has one highly cited category which is 6 - Others")

st.subheader("Among the top 5 highly cited zones, Vermont shares 2 out of 5. And Vermont’s patent category covers 6 categories out of 7. That concludes why Vermont is the top 1 inventor state in the U.S.  ")
st.subheader("Massachusetts is the Drugs and Medical inventor incubator state (0.0013); And California, no surprise, is the state where Computers and Communications inventors grew up. ")

################################################################  Part II  ##############################################################
st.write("")
st.header("Part2: Correlation between Invention Rate and Parent Income")
inventor_clean = inventor

cols = st.columns(2)
with cols[0]:
    left = st.selectbox('Parent Income 1', ['top 20%', '20 - 40%', '40 - 60%', '60 - 80%', 'bottom 20%'])
with cols[1]:
    right = st.selectbox('Parent Income 2', ['top 20%', '20 - 40%', '40 - 60%', '60 - 80%', 'bottom 20%'])

top_20_chart = alt.Chart(inventor_clean).mark_bar().encode(
        alt.Y(field = "inventor_pq_5", aggregate = 'average', type ='quantitative', title = 'children inventor rate', scale=alt.Scale(domain=(0.002, 0.02))),
        alt.X("par_state", title = 'top 25 states with highest invention rate', sort = '-y'),
).properties(
   height=500, width=730
).transform_window(
    rank='rank(inventor_pq_5)',
    sort=[alt.SortField('inventor_pq_5', order='descending')]
).transform_filter(
    (alt.datum.rank < 66)
)

top_20_40_chart = alt.Chart(inventor_clean).mark_bar().encode(
        alt.Y(field = "inventor_pq_4", aggregate = 'average', type ='quantitative', title = 'children inventor rate', scale=alt.Scale(domain=(0.002, 0.02))),
        alt.X("par_state", title = 'top 25 states with highest invention rate', sort = '-y'),
).properties(
   height=500, width=730
).transform_window(
    rank='rank(inventor_pq_4)',
    sort=[alt.SortField('inventor_pq_4', order='descending')]
).transform_filter(
    (alt.datum.rank < 66)
)

top_40_60_chart = alt.Chart(inventor_clean).mark_bar().encode(
        alt.Y(field = "inventor_pq_3", aggregate = 'average', type ='quantitative', title = 'children inventor rate', scale=alt.Scale(domain=(0.002, 0.02))),
        alt.X("par_state", title = 'top 25 states with highest invention rate', sort = '-y'),
).properties(
   height=500, width=730
).transform_window(
    rank='rank(inventor_pq_3)',
    sort=[alt.SortField('inventor_pq_3', order='descending')]
).transform_filter(
    (alt.datum.rank < 66)
)

top_60_80_chart = alt.Chart(inventor_clean).mark_bar().encode(
        alt.Y(field = "inventor_pq_2", aggregate = 'average', type ='quantitative', title = 'children inventor rate', scale=alt.Scale(domain=(0.002, 0.02))),
        alt.X("par_state", title = 'top 25 states with highest invention rate', sort = '-y'),
).properties(
   height=500, width=730
).transform_window(
    rank='rank(inventor_pq_2)',
    sort=[alt.SortField('inventor_pq_2', order='descending')]
).transform_filter(
    (alt.datum.rank < 66)
)

bottom_20_chart =  alt.Chart(inventor_clean).mark_bar().encode(
        alt.Y(field = "inventor_pq_1", aggregate = 'average', type ='quantitative', title = 'children inventor rate', scale=alt.Scale(domain=(0.002, 0.02))),
        alt.X("par_state", title = 'top 25 states with highest invention rate', sort = '-y'),
).properties(
   height=500, width=730
).transform_window(
    rank='rank(inventor_pq_1)',
    sort=[alt.SortField('inventor_pq_1', order='descending')]
).transform_filter(
    (alt.datum.rank < 66)
)

st.caption("*the left column serve as reference group and the right as experiment group. By changing the right coulmn, we can see the differences in children inventor rate.")

colss = st.columns(2)
with colss[0]:
    if left == "top 20%":
        st.write(top_20_chart)
    elif left == "20 - 40%":
        st.write(top_20_40_chart)
    elif left == '40 - 60%':
        st.write(top_40_60_chart)
    elif left == '60 - 80%':
        st.write(top_60_80_chart)
    elif left == 'bottom 20%':
        st.write(bottom_20_chart)
        
with colss[1]:
    if right == "top 20%":
        st.write(top_20_chart)
    elif right == "20 - 40%":
        st.write(top_20_40_chart)
    elif right == '40 - 60%':
        st.write(top_40_60_chart)
    elif right == '60 - 80%':
        st.write(top_60_80_chart)
    elif right == 'bottom 20%':
        st.write(bottom_20_chart)

st.subheader("Conclusion: the higher parent income, the higher children innovation rate.")


################################################################  Part III  ##############################################################

st.header("Part3. The year most inventors were born")
if st.checkbox("Hit me if you want to check on the raw data"):
    st.write(df)
st.text("Dataset ->  Innovation by Current State, Year of Birth and Age ")
st.text("The dataset reports patenting outcomes for individuals aged 20 to 80 in years 1996-2012 by year of birth")

# create Tooltip, below code are referenced from https://altair-viz.github.io/gallery/multiline_tooltip.html

nearest = alt.selection(type='single', nearest=True, on='mouseover',fields=['x'], empty='none')

line = alt.Chart(df).mark_line(interpolate='basis').encode(
                   x= alt.X('cohort', scale=alt.Scale(zero=False), title = "Year of Birth"), 
                   y= alt.Y(field = "num_grants", aggregate = 'mean', type ='quantitative', sort='-y', scale=alt.Scale(zero=False), title = "average number of patents grants per individual"),
                   color = alt.Color('age')
                )
selectors = alt.Chart(df).mark_point().encode(
    x='x:Q',
    opacity=alt.value(0)).add_selection(nearest)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)
# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'y:Q', alt.value(' '))
)
# Draw a rule at the location of the selection
rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='x:Q',
).transform_filter(
    nearest
)
# Put the five layers into a chart and bind the data
layer = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)
st.altair_chart(layer)

st.text("Cohort Range (1960 - 1965) has the highest average number of patents grants per individual")

# nearest = alt.selection(type='single', nearest=True, on='mouseover',fields=['x'], empty='none')
# line = alt.Chart(df).mark_bar(interpolate='basis').encode(
#                    x= alt.X('year', scale=alt.Scale(zero=False), title = "Calendar Year"), 
#                    y= alt.Y(field = "num_grants", aggregate = 'mean', type ='quantitative', sort='-y', scale=alt.Scale(zero=False), title = "average number of patents grants per individual"),
#                    color= alt.Color('cohort')
#                 )
# selectors = alt.Chart(df).mark_point().encode(
#     x='x:Q',
#     opacity=alt.value(0)).add_selection(nearest)

# # Draw points on the line, and highlight based on selection
# points = line.mark_point().encode(
#     opacity=alt.condition(nearest, alt.value(1), alt.value(0))
# )
# # Draw text labels near the points, and highlight based on selection
# text = line.mark_text(align='left', dx=5, dy=-5).encode(
#     text=alt.condition(nearest, 'y:Q', alt.value(' '))
# )
# # Draw a rule at the location of the selection
# rules = alt.Chart(df).mark_rule(color='gray').encode(
#     x='x:Q',
# ).transform_filter(
#     nearest
# )
# # Put the five layers into a chart and bind the data
# layer2 = alt.layer(
#     line, selectors, points, rules, text
# ).properties(
#     width=600, height=300
# )
# st.altair_chart(layer2)

# st.subheader("Calendar year 2003 has the highest average number of patents grants per individual.")               
st.markdown(
    """
    #### Inventors aged around 40 are most productive based on the average number of patents grants per individual :sunglasses:
    """
    )

st.subheader("Custom Slicing Based on State and Year of Birth")

cols = st.columns(2)
with cols[0]:
    states = st.multiselect('State: ',df['state'].unique())  #drop down for categorical variable
with cols[1]:
    cohort_range = st.slider('Cohort',
                    min_value=int(df['cohort'].min()),
                    max_value=int(df['cohort'].max()),
                    value=(int(df['cohort'].min()), int(df['cohort'].max()))
                    )

slice_labels = get_slice_membership(df, states, cohort_range)

# st.write("The sliced dataset contains {} elements".format(slice_labels.sum()))

Inslice_num_grants = df[slice_labels]['num_grants'].mean()
Noslice_num_grants = df[~slice_labels]['num_grants'].mean()

col1, col2 = st.columns(2)
with col1:
    st.header("In Slice")
    st.metric('Num of Grants', '{:.2%}'.format(Inslice_num_grants))

with col2:
    st.header("Out of Slice")
    st.metric('Num of Grants', '{:.2%}'.format(Noslice_num_grants))





st.markdown("This project was created by Cuiting Li and Haoyu Wang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
