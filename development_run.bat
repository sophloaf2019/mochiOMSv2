call npm install

call pip install -r requirements.txt

start cmd /k "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"

call flask run --debug

pause