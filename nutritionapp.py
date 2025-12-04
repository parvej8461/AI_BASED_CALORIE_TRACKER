import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import altair as alt
import json
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---

# Load variables from .env file (GOOGLE_API_KEY)
load_dotenv()  # This reads the .env file in your project folder

API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="SnapCalorie AI", layout="centered")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY is missing. Please create a .env file with your API key.")
else:
    # Configure Gemini API using the key from .env
    genai.configure(api_key=API_KEY)


# --- 2. THE AI BRAIN (GEMINI 1.5 FLASH) ---
def get_nutritional_info(image):
    # If API key missing, don't call the model
    if not API_KEY:
        st.error("Cannot call Gemini API because GOOGLE_API_KEY is not set.")
        return None

    # We use Gemini 1.5 Flash - it's faster and cheaper for vision tasks
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # The Prompt: We explicitly ask for JSON format
    prompt = """
    You are an expert nutritionist. Analyze the food items in this image.
    Identify each food item and estimate its nutritional content based on portion size.
    
    Return the response strictly in this JSON format (no markdown, no other text):
    {
        "items": [
            {"name": "Food Name", "calories": 0, "protein": 0, "carbs": 0, "fat": 0},
            ...
        ],
        "total": {
            "calories": 0, "protein": 0, "carbs": 0, "fat": 0
        }
    }
    """
    
    try:
        response = model.generate_content([prompt, image])
        # Clean the response to ensure it's pure JSON
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
    except Exception as e:
        st.error(f"Error parsing AI response: {e}")
        return None


# --- 3. UI HELPERS ---
def make_donut_chart(protein, carbs, fat):
    # Create a DataFrame for the chart
    source = pd.DataFrame({
        "Category": ["Protein", "Carbs", "Fat"],
        "Value": [protein, carbs, fat]
    })
    
    # Altair Donut Chart
    base = alt.Chart(source).encode(
        theta=alt.Theta("Value", stack=True)
    )
    pie = base.mark_arc(outerRadius=120).encode(
        color=alt.Color("Category"),
        order=alt.Order("Value", sort="descending"),
        tooltip=["Category", "Value"]
    )
    text = base.mark_text(radius=140).encode(
        text=alt.Text("Value", format=".1f"),
        order=alt.Order("Value", sort="descending"),
    )
    return pie + text


# --- 4. MAIN APP LAYOUT ---
st.title("🍎 SnapCalorie AI")
st.write("Upload a photo of your meal to get instant nutritional insights.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Meal", use_column_width=True)
    
    if st.button("Analyze Meal"):
        with st.spinner("🤖 AI is analyzing your food..."):
            data = get_nutritional_info(image)
            
            if data:
                # --- SECTION A: SUMMARY CARDS ---
                st.subheader("Total Nutrition")
                totals = data["total"]
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories", f"{totals['calories']} kcal", delta_color="off")
                c2.metric("Protein", f"{totals['protein']}g", "💪")
                c3.metric("Carbs", f"{totals['carbs']}g", "🍞")
                c4.metric("Fat", f"{totals['fat']}g", "🥑")
                
                st.divider()
                
                # --- SECTION B: VISUALIZATION & BREAKDOWN ---
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("Macro Distribution")
                    chart = make_donut_chart(
                        totals["protein"],
                        totals["carbs"],
                        totals["fat"]
                    )
                    st.altair_chart(chart, use_container_width=True)
                
                with col2:
                    st.subheader("Item Breakdown")
                    for item in data["items"]:
                        with st.expander(f"🍽️ {item['name']} ({item['calories']} kcal)"):
                            st.write(f"- **Protein:** {item['protein']}g")
                            st.write(f"- **Carbs:** {item['carbs']}g")
                            st.write(f"- **Fat:** {item['fat']}g")
                            
                # --- SECTION C: AI ADVICE ---
                st.success(
                    "💡 **Healthy Tip:** "
                    + (
                        "Great protein source!"
                        if totals["protein"] > 30
                        else "Consider adding more protein next time."
                    )
                )
