import pandas as pd
import streamlit as st
print("Libraries Imported Successfully")

# GitHub raw CSV URL (replace with your actual link)
csv_url = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/emission_factor_formated.csv"

# Load DataFrame from GitHub
df = pd.read_csv(csv_url)

print("Dataset Loaded Successfully")
per_capita_EU_27 = emission_factor_formated.loc["per_capita", "European Union (27)"]
per_capita_World = emission_factor_formated.loc["per_capita", "World"]

def format_activity_name(activity):
    activity_mappings = {
        "Domestic flight": "How many km of Domestic Flights taken the last month",
        "International flight": "How many km of International Flights taken the last month",
        "km_diesel_local_passenger_train_traveled": "How many km traveled by diesel-powered local passenger trains the last month",
        "km_diesel_long_distance_passenger_train_traveled": "How many km traveled by diesel-powered long-distant passenger trains the last month",
        "km_electric_passenger_train_traveled": "How many km traveled by electric-powered passenger trains the last month",
        "km_bus_traveled": "How many km traveled by bus the last month",
        "km_petrol_car_traveled": "How many km traveled by petrol-powered car the last month",
        "km_Motorcycle_traveled": "How many km traveled by motorcycle the last month",
        "km_ev_scooter_traveled": "How many km traveled by electric scooter the last month",
        "km_ev_car_traveled": "How many km traveled by electric-powered car the last month",
        "diesel_car_traveled": "How many km traveled by diesel-powered car the last month",
        "water_consumed": "How much water consumed in liters the last month",
        "electricity_used": "How much electricity used in kWh the last month",
        "beef_products_consumed": "How much beef consumed in kg the last month",
        "beverages_consumed": "How much beverages consumed in liters the last month",
        "poultry_products_consumed": "How much poultry consumed in Kg the last month",
        "pork_products_consumed": "How much pork have you consumed in kg the last month",
        "processed_rice_consumed": "How much processed rice consumed in kg the last month",
        "sugar_consumed": "How much sugar have you consumed in kg the last month",
        "vegetable_oils_fats_consumed": "How much vegetable oils and fats consumed in kg the last month",
        "other_meat_products_consumed":  "How much other meat products consumed in kg the last month",
        "dairy_products_consumed": "How much dairy products consumed in kg the last month",
        "fish_products_consumed": "How much fish products consumed in kg the last month",
        "other_food_products_consumed": "How much other food products have you consumed in kg the last month",
        "hotel_stay": "How many nights stayed in hotels the last month"
    }
    return activity_mappings.get(activity, activity.replace("_", " ").capitalize())

print("Formating Done Successfully")

# Streamlit UI to collect name and gender
st.title("Carbon Footprint Calculator")

# Markdown
st.markdown("""
Show that you care about the Environment. Calculate your carbon footprint and get the ball rolling towards offsetting them. 
""")

# Display an image
st.image('carbon_image.jpg', use_container_width=True)

# Collect identity and mood
name = st.text_input("Type your name:")
mood = st.selectbox("Select your mood:", ["is Happy", "is slightly Happy"])
print("Name and Mood Created Successfully")

# Check if name and mood are entered
if not name or not mood:
    st.warning("Please enter your name and select your mood before proceeding.")
else:
    # Display message based on identity 
    st.write(f"Welcome {name}! Let's calculate your Carbon Footprint.")

# Initialize session state for tracking which activity to show
if "current_activity_start" not in st.session_state:
    st.session_state.current_activity_start = 0  # Start with the first activity
    st.session_state.emission_values = {}  # Store input values for each activity

# Number of activities to show per page
activities_per_page = 25

# Extract country names (all columns except 'Activity')
country_list = df.columns[1:].tolist()

# Select country
country = st.selectbox("Select a country:", country_list)
print("Country Selected Successfully")

if country:
    # Get the current set of activities to show
    activities = df['Activity'].tolist()
    activities_to_display = activities[st.session_state.current_activity_start: st.session_state.current_activity_start + activities_per_page]

    # Display the activities
    for activity in activities_to_display:
        activity_row = df[df['Activity'] == activity]
        activity_description = format_activity_name(activity)
        factor = activity_row[country].values[0]
        
        # Get user input for the current activity
        user_input = st.number_input(f"{activity_description}", min_value=0, step=1, key=activity)

        # Store the input value for later use
        st.session_state.emission_values[activity] = user_input * factor

    # Show "Next" button if there are more activities to show
    if st.session_state.current_activity_start + activities_per_page < len(activities):
        next_button = st.button("Next")
        if next_button:
            st.session_state.current_activity_start += activities_per_page  # Move to the next set of activities

    # If we have shown all activities, display the "Calculate" button
    if st.session_state.current_activity_start + activities_per_page >= len(activities):
        calculate_button = st.button("Calculate")
        if calculate_button:
            # Calculate total emission after clicking "Calculate"
            total_emission = sum(st.session_state.emission_values.values())
            st.subheader(f"Your Carbon Footprint is: {total_emission:.4f}")
            
st.subheader(f"Per Capita Emission for European Union (27) is: {per_capita_EU_27} kgCO2 equivalent")
st.subheader(f"Per Capita Emission for World is: {per_capita_World} kgCO2 equivalent")
else:
    st.warning("Please select a country.")

print("Completed!")
