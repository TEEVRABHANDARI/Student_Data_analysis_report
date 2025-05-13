import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Load and rename dataset
df = pd.read_csv('data/student_lifestyle_dataset.csv')
df.rename(columns={
    'Sleep_Hours_Per_Day': 'SleepHours',
    'Study_Hours_Per_Day': 'StudyHours',
    'Physical_Activity_Hours_Per_Day': 'PhysicalActivityHours',
    'Social_Hours_Per_Day': 'SocialHours',
    'Extracurricular_Hours_Per_Day': 'ExtracurricularHours',
    'Stress_Level': 'StressLevel'
}, inplace=True)

# Page config
st.set_page_config(page_title="Student Lifestyle Dashboard", layout='wide')
st.title("Student Lifestyle Analytics Dashboard")

# =============================
# Sidebar Filters
# =============================
st.sidebar.header("Filters")

stress_levels = sorted(df['StressLevel'].unique())
selected_stress = st.sidebar.multiselect("Stress Level", stress_levels, default=stress_levels)

gpa_range = st.sidebar.slider("GPA Range", float(df.GPA.min()), float(df.GPA.max()), (float(df.GPA.min()), float(df.GPA.max())))
sleep_range = st.sidebar.slider("Sleep Hours", int(df.SleepHours.min()), int(df.SleepHours.max()), (int(df.SleepHours.min()), int(df.SleepHours.max())))
study_range = st.sidebar.slider("Study Hours", int(df.StudyHours.min()), int(df.StudyHours.max()), (int(df.StudyHours.min()), int(df.StudyHours.max())))
activity_range = st.sidebar.slider("Physical Activity", int(df.PhysicalActivityHours.min()), int(df.PhysicalActivityHours.max()), (int(df.PhysicalActivityHours.min()), int(df.PhysicalActivityHours.max())))
social_range = st.sidebar.slider("Social Time", int(df.SocialHours.min()), int(df.SocialHours.max()), (int(df.SocialHours.min()), int(df.SocialHours.max())))

# =============================
# Filter Data
# =============================
filtered_df = df[
    (df['StressLevel'].isin(selected_stress)) &
    (df['GPA'].between(*gpa_range)) &
    (df['SleepHours'].between(*sleep_range)) &
    (df['StudyHours'].between(*study_range)) &
    (df['PhysicalActivityHours'].between(*activity_range)) &
    (df['SocialHours'].between(*social_range))
]

# =============================
# KPI Section
# =============================
st.markdown("### Key Lifestyle Metrics")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Average GPA", f"{filtered_df['GPA'].mean():.2f}")
kpi2.metric("Avg Sleep", f"{filtered_df['SleepHours'].mean():.1f} hrs/day")
kpi3.metric("Avg Study", f"{filtered_df['StudyHours'].mean():.1f} hrs/day")
kpi4.metric("Avg Activity", f"{filtered_df['PhysicalActivityHours'].mean():.1f} hrs/day")
kpi5.metric("Avg Social", f"{filtered_df['SocialHours'].mean():.1f} hrs/day")

st.caption(f"🔍 Showing {len(filtered_df)} of {len(df)} records based on filters.")

# =============================
# Scatter Plots
# =============================
st.markdown("### Lifestyle Factors vs GPA")

r1c1, r1c2 = st.columns(2)
with r1c1:
    fig_sleep = px.scatter(filtered_df, x='SleepHours', y='GPA', color='StressLevel',
                           template='plotly_white', title='Sleep Hours vs GPA')
    st.plotly_chart(fig_sleep, use_container_width=True)

with r1c2:
    fig_study = px.scatter(filtered_df, x='StudyHours', y='GPA', color='StressLevel',
                           template='plotly_white', title='Study Hours vs GPA')
    st.plotly_chart(fig_study, use_container_width=True)

r2c1, r2c2 = st.columns(2)
with r2c1:
    fig_social = px.scatter(filtered_df, x='SocialHours', y='GPA', color='StressLevel',
                            template='plotly_white', title='Social Time vs GPA')
    st.plotly_chart(fig_social, use_container_width=True)

with r2c2:
    fig_activity = px.scatter(filtered_df, x='PhysicalActivityHours', y='GPA', color='StressLevel',
                              template='plotly_white', title='Physical Activity vs GPA')
    st.plotly_chart(fig_activity, use_container_width=True)

# =============================
# GPA by Stress Level
# =============================
st.markdown("### GPA by Stress Level")
fig_bar = px.bar(
    filtered_df.groupby('StressLevel')['GPA'].mean().reset_index(),
    x='StressLevel', y='GPA', text_auto='.2f',
    template='plotly_white', title='Average GPA by Stress Level',
    color_discrete_sequence=["#FF6B6B"]
)
st.plotly_chart(fig_bar, use_container_width=True)

# =============================
# Correlation Matrix Heatmap
# =============================
st.markdown("### Correlation Matrix")
numeric_df = filtered_df[['GPA', 'SleepHours', 'StudyHours', 'PhysicalActivityHours', 'SocialHours']]
corr = numeric_df.corr().round(2)

fig_corr = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.values,
    colorscale='Blues',
    showscale=True,
    hoverinfo="z"
)
st.plotly_chart(fig_corr, use_container_width=True)

# =============================
# Insights Section
# =============================
with st.expander("### Insights & Observations"):
    st.markdown("""

This dashboard provides a comprehensive analysis of how various lifestyle factors impact student performance, especially GPA. Based on the visualizations and correlation matrix, several key insights emerge:
                

**1. Strong Relationship Between Study Hours and GPA**

- There is a **strong positive correlation (0.73)** between **Study Hours** and **GPA**.
- This indicates that students who dedicate more time to studying are more likely to achieve higher academic performance.
- The scatter plot reinforces this trend with a clear upward slope, regardless of stress levels.

**2. Negligible Influence of Sleep Hours on Academic Performance**

- The correlation between **Sleep Hours** and **GPA** is approximately **0.00**, showing no linear relationship.
- This suggests that while sleep is important for overall well-being, its direct impact on academic scores is not significant in this dataset.
- The distribution of GPA across varying sleep durations remains almost uniform.

**3. Physical Activity and Social Time Have Mild to Moderate Negative Correlation with GPA**

- **Physical Activity Hours** have a **moderate negative correlation (-0.34)** with GPA.
- This could imply that excessive time spent on physical activities might reduce the time available for academics, but it doesn't suggest causation.
- **Social Hours** show a **weak negative correlation (-0.09)** with GPA, suggesting a slightly inverse relationship, although not strong enough to be conclusive.

**4. Stress Level Appears to Affect Academic Performance**

- From the **"GPA by Stress Level"** bar chart, it is evident that students with **lower stress levels tend to have higher GPA values** on average.
- Higher stress levels are associated with a noticeable drop in academic performance.
- This reinforces the importance of mental health management and stress reduction strategies for students.

**5. No Multicollinearity Between Most Lifestyle Variables**

- The correlation matrix shows relatively low interdependence between variables like Sleep, Social Hours, and Study Hours.
- This independence means each variable can be analyzed without significant overlap or redundancy.
- Notably, **Study Hours and Physical Activity Hours** have a moderately strong **negative correlation (-0.49)**, suggesting students may trade-off study time for physical engagement.

**6. Consistency Across Stress Levels**

- All scatter plots are color-coded by stress level. Across all lifestyle metrics, a consistent trend emerges:
    - **Lower stress levels** consistently cluster around higher GPA ranges.
    - This supports the bar chart findings and underlines the **psychological dimension** of academic performance.


""")




with st.expander("Conclusion"):
    st.markdown("""
This dashboard effectively highlights the impact of lifestyle habits on academic performance. While **Study Hours remain the most significant driver of GPA**, **stress management**, **balanced social life**, and **optimal physical activity** play supporting roles in shaping a student's academic outcomes. The data indicates that **prioritizing consistent study routines** and **reducing stress** are the most impactful actions students can take to improve academic success.
""")


# =============================
# Show Filtered Data
# =============================
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)
