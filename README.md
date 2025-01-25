# FastApi-Backend
## To setup the project locally on your machine
1. Get started in a code editor (Preferably Pycharm)
  
  ```sh
  git clone https://github.com/Adityasinghvats/FastApi-Backend.git
  ```
2. Need to setup MongoDB on local system.
  
3. In the root directory open integrated terminal and run the command
```sh
pip install -r requirements.txt
```

4. Run to parse the data to MongoDB.
 ```sh
script.py
 ``` 
5. Now run the project locally
  
   ```sh
   cd app
   uvicorn main:app --reload
   ```
6. To get api docs in Swagger format
   - Open the url provided by uvicron in terminal directly 
     
     ```sh
     http://127.0.0.1:8000/docs
     http://127.0.0.1:8000/redoc
     ```
7. Install Docker Desktop , then run the following command in root directory

   ```sh
   docker build -t my_python_app .
   docker run -d --name fast_api -p 80:80 my_python_app
   ```
8. Demo
   
![Screenshot 2024-08-27 182929](https://github.com/user-attachments/assets/c4c66d22-4fa6-4a1f-9d52-490d830b4bb0)
