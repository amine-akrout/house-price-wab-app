from pycaret.classification import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
model = load_model('Final_model')

def predict(model, input_df):
	predictions_df = predict_model(estimator=model, data=input_df)
	predictions = predictions_df['Label'][0]
	return predictions

dic_ExterQual= { 'Excellent' : 'Ex',
                'Good' : 'Gd',
                'Average/Typical' : 'TA',
                'Fair' : 'Fa',
                'Poor' : 'Po'}

dic_BsmtQual = {'Excellent (100+ inches)':'Ex',
       'Good (90-99 inches)':'Gd',
       'Typical (80-89 inches)':'TA',
       'Fair (70-79 inches)':'Fa',
       'Poor (<70 inches':'Po',
       'No Basement':'NA'}

def main():
	from PIL import Image
	image = Image.open('icone.jpg')
	image2 = Image.open('image.png')
	st.image(image,use_column_width=False)
	add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?",
	("Online", "Batch"))
	st.sidebar.info('This app is created to predict House prices')
	st.sidebar.image(image2)
	st.title("Predicting house price")
	if add_selectbox == 'Online':
		LotArea=st.number_input('Lot size in square feet :' , min_value=1300, max_value=21600, value=10000)
		OverallQual =st.selectbox('Rates the overall material and finish of the house :',['10 Very Excellent', '9 Excellent','8 Very Good','7 Good' ,'6 Above Average','5 Average','4 Below Average','3 Fair','2 Poor','1 Very Poor'])
		YearBuilt = st.number_input('Original construction date :', min_value=1872, max_value=2020, value=1950)
		YearRemodAdd = st.number_input('Remodel year :', min_value=1950, max_value=2010, value=1995)
		TotRmsAbvGrd = st.number_input('Total rooms above grade (does not include bathrooms) : ', min_value=2, max_value=14, value=3)
		TotalBsmtSF = st.number_input('Total square feet of basement area : ', min_value=0, max_value=7000, value=700)
		GrLivArea = st.number_input('Above grade (ground) living area square feet : ',  min_value=0, max_value=7000, value=700)
		GarageCars = st.selectbox('Size of garage in car capacity : ',  ['0', '1','2','3','4','5'])
		ExterQual = st.selectbox('Evaluates the quality of the material on the exterior : ',  ['Excellent','Good','Average/Typical','Fair','Poor'])
		BsmtQual = st.selectbox('Evaluates the height of the basement',  ['Excellent (100+ inches)','Good (90-99 inches)', 'Typical (80-89 inches)','Fair (70-79 inches)','Poor (<70 inches','No Basement'])
		output=""
		input_dict={'LotArea':LotArea,'OverallQual':[int(s) for s in OverallQual.split() if s.isdigit()][0],'YearBuilt':YearBuilt,'YearRemodAdd':YearRemodAdd,'TotRmsAbvGrd':TotRmsAbvGrd,'TotalBsmtSF':TotalBsmtSF,'GrLivArea':GrLivArea,'GarageCars':GarageCars,'ExterQual':dic_ExterQual[ExterQual],'BsmtQual':dic_BsmtQual[BsmtQual]}
		input_df = pd.DataFrame([input_dict])
		if st.button("Predict"):
			output = predict(model=model, input_df=input_df)
			output = str(output)
		st.success('The estimated parice is : {} $'.format(output))
	if add_selectbox == 'Batch':
		file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
		if file_upload is not None:
			data = pd.read_csv(file_upload)
			predictions = predict_model(estimator=model,data=data)
			st.write(predictions)
if __name__ == '__main__':
	main()