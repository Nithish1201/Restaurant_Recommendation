import streamlit as st
import pandas as pd

st.header('Chennai Restaurant Recommendation System')
userChoice = st.multiselect("What do you feel like having?",
                             ['Chinese', 'North Indian', 'South Indian', 'Fast Food', 'Beverages',
                              'Biryani', 'Desserts', 'Cafe', 'Chettinad', 'Continental',
                              'Middle Eastern', 'Italian', 'Seafood', 'Asian', 'Pizza', 'Barbeque',
                              'Wraps', 'Healthy Food'])
data = pd.read_csv('C:\cuisine_update.csv')
minMaxPrice = st.slider('Price for 2',0, 5000, (1000, 2500),100)
minMaxRating = st.slider('Restaurant Rating', 0.0, 5.0, (4.0, 5.0),0.1)
col1, col2, col3 = st.columns(3)
with col3:
    sortByPrice = st.radio("Sort By Order",('Descending','Ascending'))
with col1:
    preferance = st.radio("Preferance",('Cuisine Quantity','Price'))

c1, c2, c3= st.columns(3)
with c2:
    submit = st.button('Get Recommendation')
if(submit):
    #print(minMaxPrice,minMaxRating,sortByPrice,sortByRating)
    #user_choice = ['North Indian', 'Beverages', 'Desserts'] #To be taken from User
    data['Cuisine'] = data['Cuisine'].apply(eval)
    dataList = []
    for i in data.index:
        for j in userChoice:
            if j in data['Cuisine'][i]:
                dataList.append(data['Name of Restaurant'][i])

    count = 0
    count1 = 0
    countlist = []
    namelist = []
    for i in range(1,len(dataList)):
        if i <= len(dataList)-2:
            if dataList[i] == dataList[i-1]:
                count1 += 1
            else:
                namelist.append(dataList[i-1])
                countlist.append(count1+1)
                count1 = 0
        else:
            if dataList[i] == dataList[i-1]:
                count1 += 1
                namelist.append(dataList[i-1])
                countlist.append(count1)
                count1 = 0

    # with st.expander("Filter"):
    #     minMaxPrice = st.slider('Price for 2',0, 5000, (1000, 2500))
    #     minMaxRating = st.slider('Restaurant Rating', 0, 5, (4, 5))
    #     sortByPrice = st.radio("Sort By - Price for 2",('Ascending', 'Descending'))
    #     sortByRating = st.radio("Sort By - Rating",('Ascending', 'Descending'))
    #     st.info(minMaxPrice)
    #     apply = st.button("Apply")
    #     if apply:
    #         st.info("CLICKED!")

    df = data[data['Name of Restaurant'].isin(namelist)]
    df['count'] = countlist
    df = df[df['Price for 2']>=minMaxPrice[0]]
    df = df[df['Price for 2']<=minMaxPrice[1]]
    df = df[df['Dining Rating'] >= minMaxRating[0]]
    df = df[df['Dining Rating'] <= minMaxRating[1]]
    df.drop(['Cuisine'], axis=1, inplace=True)
    finalDF = pd.DataFrame([], columns=['Zomato URL', 'Name of Restaurant', 'Address', 'Price for 2',
                                        'Dining Rating', 'Dining Rating Count', 'count', 'PriceForTwoCount'])
    #df.sort_values(by=['count', 'Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=False, inplace=True)
    if(preferance == "Price"):
        if(sortByPrice=="Descending"):
             #df.sort_values(by=['Price for 2', 'count', 'Dining Rating', 'Dining Rating Count'], ascending=False,inplace=True)
             df.sort_values(by=['Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=False,
                            inplace=True)
        else:
             df.sort_values(by=['Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=True,inplace=True)
             df.reset_index(drop=True, inplace=True)
             lst = []
             cnt = 0
             maxOfI = 0
             for i in range(df.shape[0] - 1):
                 if (df['Price for 2'][i] == df['Price for 2'][i + 1]):
                     lst.append(cnt)
                 else:
                     lst.append(cnt)
                     cnt = cnt + 1
                 maxOfI = i

             if (df['Price for 2'][maxOfI] == df['Price for 2'][maxOfI + 1]):
                 lst.append(cnt)
             else:
                 lst.append(cnt + 1)
             # lst
             df['PriceForTwoCount'] = lst

             noOfRows = int(df.shape[0])
             noOfRows = noOfRows - 1
             arr = []
             indexC = 0
             ij = 0
             for i in range(noOfRows):
                 if (df['PriceForTwoCount'][i] == indexC):
                     arr.append([df['Zomato URL'][i], df['Name of Restaurant'][i], df['Address'][i],
                                 df['Price for 2'][i], round(df['Dining Rating'][i],1), df['Dining Rating Count'][i],
                                 df['count'][i], df['PriceForTwoCount'][i]])
                     if (df['PriceForTwoCount'][i] != df['PriceForTwoCount'][i + 1]):
                         df10 = pd.DataFrame(arr, columns=['Zomato URL', 'Name of Restaurant', 'Address', 'Price for 2',
                                                           'Dining Rating', 'Dining Rating Count', 'count',
                                                           'PriceForTwoCount'])
                         df10.sort_values(by=['Dining Rating', 'Dining Rating Count'], ascending=False, inplace=True)
                         df10.reset_index(drop=True, inplace=True)
                         finalDF = pd.concat([finalDF, df10])
                         indexC = indexC + 1
                         arr = []
                 ij = i

             if (df['PriceForTwoCount'][ij] == indexC):
                 arr.append([df['Zomato URL'][ij], df['Name of Restaurant'][ij], df['Address'][ij],
                             df['Price for 2'][ij], round(df['Dining Rating'][ij],1), df['Dining Rating Count'][ij],
                             df['count'][ij], df['PriceForTwoCount'][ij]])
                 if (df['PriceForTwoCount'][ij] != df['PriceForTwoCount'][ij + 1]):
                     indexC = indexC + 1
                     arr.append(
                         [df['Zomato URL'][ij + 1], df['Name of Restaurant'][ij + 1], df['Address'][ij + 1],
                          df['Price for 2'][ij + 1], round(df['Dining Rating'][ij + 1],1),
                          df['Dining Rating Count'][ij + 1], df['count'][ij + 1], df['PriceForTwoCount'][ij + 1]])
                     df10 = pd.DataFrame(arr, columns=['Zomato URL', 'Name of Restaurant', 'Address', 'Price for 2',
                                                       'Dining Rating', 'Dining Rating Count', 'count',
                                                       'PriceForTwoCount'])
                     df10.sort_values(by=['Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=False,
                                      inplace=True)
                     df10.reset_index(drop=True, inplace=True)
                     finalDF = pd.concat([finalDF, df10])
                     indexC = indexC + 1
                     arr = []
                 else:
                     arr.append(
                         [df['Zomato URL'][ij + 1], df['Name of Restaurant'][ij + 1], df['Address'][ij + 1],
                          df['Price for 2'][ij + 1], round(df['Dining Rating'][ij + 1],1),
                          df['Dining Rating Count'][ij + 1], df['count'][ij + 1], df['PriceForTwoCount'][ij + 1]])
                     df10 = pd.DataFrame(arr, columns=['Zomato URL', 'Name of Restaurant', 'Address', 'Price for 2',
                                                       'Dining Rating', 'Dining Rating Count', 'count',
                                                       'PriceForTwoCount'])
                     df10.sort_values(by=['Dining Rating', 'Dining Rating Count'], ascending=False, inplace=True)
                     df10.reset_index(drop=True, inplace=True)
                     finalDF = pd.concat([finalDF, df10])

             finalDF.reset_index(drop=True, inplace=True)
             finalDF.drop(finalDF.shape[0] - 1, axis=0, inplace=True)
             # df.sort_values(by=['Price for 2'], ascending=True,inplace=True)
             # df.sort_values(by=['Dining Rating', 'Dining Rating Count'], ascending=False,inplace=True)
    else:
        if(sortByPrice == "Descending"):
             df.sort_values(by=['count', 'Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=False,inplace=True)
        else:
             df.sort_values(by=['count', 'Price for 2', 'Dining Rating', 'Dining Rating Count'], ascending=True,inplace=True)

    df.reset_index(drop = True,inplace=True)

    df1 = df.loc[:,['Name of Restaurant','Price for 2','Dining Rating']]
    if(len(df1.index)>20):
        st.error("Showing "+str(len(df1.index))+" Restaurants in Chennai")
    else:
        st.success("Showing "+str(len(df1.index))+" Restaurants in Chennai")

    if ((preferance == "Price")and (sortByPrice == "Ascending")):
        finalDF.round({"Dining Rating": 1})
        finalDF['Dining Rating'].round(decimals = 1)
        finalDF.drop(['Address','Zomato URL','Dining Rating Count','count','PriceForTwoCount'], axis=1, inplace=True)
        st.dataframe(finalDF)
    else:
        df1.round({"Dining Rating": 1})
        st.dataframe(df1)

