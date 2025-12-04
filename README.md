# SnapCalorie AI – Smart Image-Based Calorie Tracker

SnapCalorie AI is a computer vision and generative AI powered nutrition tracker that analyzes food images and returns structured nutritional data (calories, protein, carbohydrates, fat) in real time.  
It is built using Google Gemini 1.5 Flash, Streamlit, and Altair for professional data visualization.

Live Application:  
https://aibasedcalorietracker-7evsnm23969cadjuvnuufd.streamlit.app/

---

## Features

- Upload a meal image for instant nutrition analysis  
- Structured JSON output for professional UI rendering  
- Displays total calories, protein, carbs, and fat  
- Macronutrient distribution donut chart  
- Per-item food breakdown  
- Dynamically generated healthy tip  
- Secure API key handling using .env file  
- Powered by Gemini 1.5 Flash for fast image inference  

---

## Technology Stack

- Frontend Framework: Streamlit  
- AI Model: Google Gemini 1.5 Flash  
- Visualization: Altair  
- Image Processing: Pillow  
- Data Handling: Pandas  
- Environment Variables: python-dotenv  

---

## Project Structure

snapcalorie/
│
├── nutrition_app.py
├── .env
├── .gitignore
├── requirements.txt
└── venv/

## Application Workflow

- User uploads a food image

- Image is sent to Gemini 1.5 Flash with a structured JSON prompt

## AI returns:

- Individual food items

- Calories, protein, carbs, and fat

- Total nutritional summary

## The app renders:

- Nutrition summary cards

- Donut chart for macronutrient distribution

- Expandable food-wise breakdown

- A short healthy recommendation

- Use Cases

- Personal calorie tracking

- Fitness and bodybuilding nutrition monitoring

- Diet planning applications

- Healthcare and wellness AI products

- Computer vision and generative AI portfolios

## Future Enhancements

- Daily calorie tracking with progress visualization

- Meal history and user accounts

- Nutrition report export as PDF

- Barcode scanning for packaged foods

- Integration with fitness platforms

## Author

- Developed by Parvej
- AI Engineer and Data Scientist

## License

This project is open source and available for learning and personal use.
