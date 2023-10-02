To run this project, run the command python ./serverSide/app.py
Open [http://localhost:5000] to view the application running.

This app uses sqlite to store data about users, sold buildings and appointments for the users who want to see a building. Only one user at a time can have an appointment for a building at a specific hour.
An user can create an account, login into his account, see available buildings.
An admin can see the existing buildings, add other buildings and see a chart for every building with the reservations for that building in the actual month.