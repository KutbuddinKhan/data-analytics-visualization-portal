# import libraries
import pandas as pd
import plotly.express as px 
import streamlit as st

st.set_page_config(
    page_title="Interactive Data Analysis and Visualization Portal",
    page_icon="📊",
)

# app title
st.title(":blue[Interactive] Data Analysis and Visualization Portal")
st.subheader('Explore Data with ease.')
st.markdown('---------')

# file upload
file = st.file_uploader("Drop csv or excel file", type=["csv", "xlsx"])

if file != None:
    # read file
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    
    # show data
    st.dataframe(data)
    st.info("File is successfully uploaded",icon='🚨')

    st.subheader(':blue[Basic information of the dataset]')
    st.markdown('----')
    tab1,tab2,tab3,tab4 = st.tabs(["Summary", "Top and Bottom Rows", "Data Types", "Columns"])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
        st.subheader(':orange[Statistical Summary of the dataset]')

    with tab2:
        # for top rows
        st.subheader('Top Rows')
        toprows = st.slider('Number of rows you want', 1, data.shape[0], key="topSlider")
        st.dataframe(data.head(toprows))
        # for bottom rows
        st.subheader('Bottom Rows')
        bottomrows = st.slider('Number of rows you want', 1, data.shape[0], key="bottomSlider")
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader('Data types of Column')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader("Column Name in Dataset")
        # st.dataframe(data.columns)
        st.write(list(data.columns))

    st.subheader('Column Values to Count')
    st.markdown('----')

    with st.expander("Value Count"):
        col1, col2 = st.columns(2)

        with col1:
            column = st.selectbox("Choose Column name", options=list(data.columns))
        with col2:
            toprows = st.number_input("Top rows", min_value=1, step=1)

        count = st.button("Count")
        if count == True:
            result = data[column].value_counts().reset_index().head(toprows)
            result.columns = [column, 'count']
            st.dataframe(result)

            st.subheader("Visualization")
            st.markdown('----')

            fig = px.bar(data_frame=result,x=column,y='count', text="count", template="plotly_white")
            st.plotly_chart(fig)

            fig = px.line(data_frame=result, x=column, y='count', text='count', template="plotly_white")
            st.plotly_chart(fig)

            fig = px.pie(data_frame=result, names=column, values="count")
            st.plotly_chart(fig)

    st.subheader("Groupby : Simplify your data analysis")
    st.write('The groupby lets you summarize data by specific categories and groups')
    st.markdown('----')

    with st.expander("Group By your columns"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby', options=list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox("Choose operation", options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if groupby_cols:
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col, operation)
            ).reset_index()

            st.dataframe(result)
            
            st.subheader("Data Visualization")
            st.markdown('----')

            graphs = st.selectbox("Choose your gaphs", options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
            if graphs == 'line':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))

                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)

            elif graphs == 'bar':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                st.plotly_chart(fig)

            elif graphs == 'scatter':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                size = st.selectbox('Size Information', options=[None] + list(result.columns))

                if size:
                    result[size] = result[size].abs()
                    result[size] = result[size].replace(0, result[size].mean()) 

                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)
            
            elif graphs == 'pie':
                values = st.selectbox('Choose Numerical values', options=list(result.columns))
                name = st.selectbox('Choose labels', options=list(result.columns))
                fig = px.pie(data_frame=result, values=values, names=name)
                st.plotly_chart(fig)

            elif graphs == 'sunburst':
                path = st.multiselect('Choose your path', options=list(result.columns))
                fig = px.sunburst(data_frame=result, path=path, values='newcol')
                st.plotly_chart(fig)

        else:
            st.write("Please select at least one column to groupby")
