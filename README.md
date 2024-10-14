# Step 1: Set Up a Virtual Environment
1.	Create a Virtual Environment
If you don't already have one, create a fresh virtual environment to isolate your project dependencies.

```bash
  python3 -m venv myenv
```

2.	Activate the Virtual Environment

```bash
 source myenv/bin/activate
```
________________________________________
# Step 2: Install Required Packages
Install the necessary Python libraries for the application:

•	pygame: For adding sound notifications.

•	pyinstaller: To build an executable file of the app.

Run the following command:
```bash
 pip install pygame pyinstaller
```



________________________________________
# Step 3: Write the Stopwatch Code
Create a new Python file called 
```bash
 nano stopwatch.py
```
 and insert the code given above.


________________________________________
# Step 4: Add a Sound Notification
Make sure you have a sound file named notify.wav in the same directory as your stopwatch.py.
 
This file will be used to play a sound when the timer stops or completes a lap.

If you don't have a .wav file, you can download one or create a simple sound file.
________________________________________
# Step 5: Create the Executable Using PyInstaller
Run the following PyInstaller command to package your Python app into an executable:
pyinstaller --onefile --add-data "notify.wav:." stopwatch.py
After the process completes, your executable will be placed in the dist folder.
________________________________________
# Step 6: Run the Executable
Navigate to the dist directory and run the newly created executable.

```bash
cd dist
```
```bash
./stopwatch
```

# Additional Tips
Error Messages: 

If any error occurs, take a note of it and share it here.

Check Python Version: Make sure you're using Python 3.6 or later, as some libraries may not work with earlier versions.

Using pipx for Installation: 

If you continue to face issues with pip install, consider using pipx, which can manage virtual environments for Python packages.
