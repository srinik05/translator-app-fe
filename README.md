# translator-app-fe

✅ Steps to fix

Delete the old venv in the frontend folder:

rm -r venv


Create a fresh virtual environment:

python -m venv venv


Activate the new virtual environment:

# Windows PowerShell
.\venv\Scripts\activate


Install the required packages (including Streamlit):

#pip install --upgrade pip
python -m pip install --upgrade pip
pip install streamlit requests


Run the app:

streamlit run streamlit_app.py