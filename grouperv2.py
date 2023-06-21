import numpy as np
import pandas as pd
import streamlit as st

def save_dataframe_to_excel(df, file_name):
    try:
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'
        df.to_excel(file_name, index=True)
        st.success("DataFrame saved to Excel file: " + file_name)
    except Exception as e:
        st.error("An error occurred while saving the DataFrame: " + str(e))

def main():
    st.title("Student Grouping App")
    
    # Load the Excel file
    file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if file is not None:
        try:
            df = pd.read_excel(file)
            st.success("File uploaded successfully.")
            
            # Perform data analysis
            dfrandomised = df.sample(frac=1)
            dfrandomgendersort = dfrandomised.sort_values(by='Gender').reset_index(drop=True)
            dfrandom = dfrandomgendersort
            gendergroups = dfrandom.groupby(["PROGRAMME OF STUDY", "Gender"]).groups
            gender_keys_list = list(gendergroups)
            total_female_students = dfrandom['Gender'].value_counts().f
            total_male_students = dfrandom['Gender'].value_counts().m
            total_students = len(dfrandom.index)
            total_programmes = len(dfrandom.groupby("PROGRAMME OF STUDY").groups)
            total_gender_programmes = len(gendergroups)
            
            # Display the analysis results
            st.subheader("Data Analysis Results")
            st.write("Total number of students: ", total_students)
            st.write("Total number of programmes: ", total_programmes)
            st.write("Total gender and programme groups: ", total_gender_programmes)
            st.write("Total female students: ", total_female_students)
            st.write("Total male students: ", total_male_students)
            
            # Get desired group size from the user
            desired_group_size = st.number_input("Enter desired group size", value=1, step=1)
            number_of_teams = total_students / float(desired_group_size)
            remainder_people = total_students % int(desired_group_size)
            st.write("Number of teams to be generated: ", int(number_of_teams))
            st.write("Remainder people to be paired: ", round(remainder_people))
            
            # Generate teams
            length_of_array = total_students - (total_students % int(desired_group_size))
            forced_array = np.arange(0, length_of_array, 1)
            reshape_array = forced_array.reshape(int(desired_group_size), int(number_of_teams))
            
            # Display teams
            st.subheader("Generated Teams")
            for i, team in enumerate(reshape_array[0]):
                st.write("Team ", i + 1, ":", reshape_array[:, i])
            
            # Add remainders as wildcards
            if remainder_people > 0:
                start = len(forced_array)
                stop = len(forced_array) + remainder_people
                step = 1
                wildcards = np.arange(start, stop, step)
            else:
                wildcards = np.array([])
            
            newindex = []
            for i, team in enumerate(reshape_array[0]):
                newindex.extend(reshape_array[:, i])
            newindex.extend(wildcards)
            
            # Output to Excel file
            file_name = st.text_input("Enter the name of the Excel file:")
            if st.button("Save as Excel"):
                if len(file_name) > 0:
                    df2 = dfrandom
                    df3 = df2.reindex(newindex)
                    save_dataframe_to_excel(df3, file_name)
                else:
                    st.warning("Please enter a file name.")
        
        except Exception as e:
            st.error("An error occurred while loading the file: " + str(e))
    
    else:
        st.warning("No file selected.")

if __name__ == '__main__':
    main()
