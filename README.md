
# Urban Footprints

"Urban Footprints" is a Streamlit-based web application designed to provide interactive mapping functionalities tailored for urban planning and analytics. This application allows users to log in to view specific mapped regions, presenting detailed metrics and data visualization related to urban footprints.

![Webpage](images/screenshot.png "Frontend")


## Features

- **User Authentication**: Secure login and logout functionality.
- **Dynamic Mapping**: Interactive maps displaying specific urban data.
- **Metrics Display**: Real-time data metrics about the displayed maps.
- **Responsive Design**: Professionally styled interface for a better user experience.

## Installation

To get started with "Urban Footprints", follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/urban-footprints.git
   cd urban-footprints
   ```

2. **Run run_app.py**
   ```bash
   python3 run_app.py
   ```
### It's that easy!

## Usage

After launching the app by running run_app.py, you will see sample user names printed on your terminal. In the login screen use any of the predefined user credentials to log in and view the maps. Note - All users have admin password.

**Note** - You can also skip second step which initialises the DB and creates map for dummy users, as they are already added as part of this repo. You can directly run this after cloning the repo   
```bash
   streamlit run app.py
   ```
and use the existing DB. List of user names for this (all have password set as "admin"):

['ChadBeck', 'MeganParrish', 'SarahGibson', 'HaileyZavala', 'TonyDay', 'Dr.MarioFrench', 'KellyGarciaMD', 'MistyZuniga', 'StephanieSmith', 'ErikGates']

Once logged in, you can view interactive maps and associated metrics. Use the sidebar to toggle metrics visibility or to log out.

## Project Structure

urban-footprints/ <br>
├── data/                    <br>
   &nbsp;&nbsp; ├── user1_map.html       <br>
   &nbsp;&nbsp; ├── user2_map.html       <br>
   &nbsp;&nbsp; └── ...                  <br>
├── app.py                   <br>
├── db_init.py               <br>
├── map_generator.py         <br>
├── requirements.txt         <br>
└── style.css                <br>
└── run_app.py               <br> 
└── README.md                <br>
└── streets_assignment.db    <br>


## Map Generator

`map_generator.py` is a Python script used to generate and update the HTML files for each user-specific map. Run this script whenever there is an update in the geographic data or user base.

## Contributing

Contributions to "Urban Footprints" are welcome! Please fork the repository and submit a pull request with your suggested changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any additional questions or feedback, please contact [urbanfootprints@uw.edu.pl](mailto:urbanfootprints@uw.edu.pl).


