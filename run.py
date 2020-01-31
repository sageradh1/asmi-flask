# import os
# from dotenv import load_dotenv
# dotenv_path = '.env'  # Path to .env file
# load_dotenv(dotenv_path)

from app import app

if __name__ == "__main__":
    app.run(debug=True)