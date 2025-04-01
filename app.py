import pandas as pd
import streamlit as st
print("Libraries Imported Successfully")

# GitHub raw CSV URL (replace with your actual link)
csv_url = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/emission_factor_formated.csv"

# Load DataFrame from GitHub
df = pd.read_csv(csv_url)

print("Dataset Loaded Successfully")

def format_activity_name(activity):
    activity_mappings = {
        "Domestic flight": "How many KM of Domestic Flights taken per year",
        "International flight": "How many KM of International Flights taken per year",
        "km_diesel_local_passenger_train_traveled": "What distance in KM have you traveled by diesel-powered local passenger trains per year",
        "km_diesel_long_distance_passenger_train_traveled": "What distance in KM have you traveled by diesel-powered long-distant passenger trains per year",
        "km_electric_passenger_train_traveled": "What distance in KM have you traveled by electric-powered passenger trains per year",
        "km_bus_traveled": "What distance in KM have you traveled by bus per year",
        "km_petrol_car_traveled": "What distance in KM have you traveled by petrol-powered car per year",
        "km_Motorcycle_traveled": "What distance in KM have you traveled by motorcycle per year",
        "km_ev_scooter_traveled": "What distance in KM have you traveled by electric scooter per year",
        "km_ev_car_traveled": "What distance in KM have you traveled by electric-powered car per year",
        "diesel_car_traveled": "What distance in KM have you traveled by diesel-powered car per year",
        "water_consumed": "How much water have you consumed in liters per year",
        "electricity_used": "How much electricity have you used in kWh per year",
        "beef_products_consumed": "How much beef have you consumed in Kg per year",
        "beverages_consumed": "How much beverages have you consumed in liters per year",
        "poultry_products_consumed": "How much poultry have you consumed in Kg per year",
        "pork_products_consumed": "How much pork have you consumed in Kg per year",
        "processed_rice_consumed": "How much processed rice have you consumed in Kg per year",
        "sugar_consumed": "How much sugar have you consumed in Kg per year",
        "vegetable_oils_fats_consumed": "How much vegetable oils and fats have you consumed in Kg per year",
        "other_meat_products_consumed":  "How much other meat products have you consumed in Kg per year",
        "dairy_products_consumed": "How much dairy products have you consumed in Kg per year",
        "fish_products_consumed": "How much fish products have you consumed in Kg per year",
        "other_food_products_consumed": "How much other food products have you consumed in Kg per year",
        "hotel_stay": "How many nights have you stayed in a hotel per year"
    }
    return activity_mappings.get(activity, activity.replace("_", " ").capitalize())

print("Formating Done Successfully")

# Streamlit UI to collect name and gender
st.title("Carbon Footprint Calculator")

# Display an image
st.image('carbon_image.jpg', use_container_width=True)

# Collect identity and mood
identity = st.text_input("Type your Champ:")
mood = st.selectbox("Select your mood:", ["is Happy", "is slightly Happy"])
print("identity and Mood Created Successfully")

# Check if mood are entered
if not identity or not mood:
    st.warning("Please enter your identity and select your mood before proceeding.")
else:
    # Display message based on identity 
    st.write(f"Welcome {identity}! Let's calculate your Carbon Footprint.")

# Initialize session state for tracking which activity to show
if "current_activity_start" not in st.session_state:
    st.session_state.current_activity_start = 0  # Start with the first activity
    st.session_state.emission_values = {}  # Store input values for each activity

# Number of activities to show per page
activities_per_page = 5

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
            

else:
    st.warning("Please select a country.")

print("Completed!")
