import os
import subprocess

def install_requirements():
    print("Installing requirements...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

def run_db_init():
    print("Running database initialization...")
    subprocess.run(["python", "db_init.py"], check=True)

def run_map_generator():
    print("Running map generator...")
    subprocess.run(["python", "map_generator.py"], check=True)

def run_streamlit_app():
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"], check=True)

if __name__ == "__main__":
    try:
        install_requirements()
        run_db_init()
        run_map_generator()
        run_streamlit_app()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
