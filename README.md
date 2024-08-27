# FastApi-Backend
## To setup the project locally on your machine
- Get started in a code editor (Preferably Pycharm)
  
  ---
  - `git clone https://github.com/Adityasinghvats/FastApi-Backend.git`
  ---
- Need to setup MongoDB on local system.
- In the root directory
  
  ---
  - Open integrated terminal and run the command
  - `pip install -r requirements.txt`
  ---
- Run `script.py` to parse the data to MongoDB.
- Now run the project locally
  
   ---
   - `cd app`
   - `uvicorn main:app --reload`
   ---
- To get api docs in Swagger format
   - Open the url provided by uvicron in terminal directly 
     
     ---
     - `http://127.0.0.1:8000/docs`
     - `http://127.0.0.1:8000/redoc`
     ---
- Install Docker Desktop , then run the following command in root directory

   ---
   - `docker build -t my_python_app .`
   - `docker run -d -p 80:80 my_python_app`
   ---
![Screenshot 2024-08-27 182929](https://github.com/user-attachments/assets/c4c66d22-4fa6-4a1f-9d52-490d830b4bb0)
