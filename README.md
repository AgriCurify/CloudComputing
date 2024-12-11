<h1 align="center">AgriCurify</h1>
<p align="center">Capstone Project Bangkit Academy 2024 Batch 2</p>
<p align="center">Cloud Computing</p>

## The service available:
- Authentications
  <pre>POST /login</pre>
  <pre>POST  /register</pre>
  <pre>POST  /logout</pre>

- User
  <pre>GET  /user</pre>
  <pre>PUT  /user</pre>
  <pre>PUT  /users/updateProfile</pre>
  <pre>PUT  /users/changePassword</pre>

- Predictions
  <pre>POST /predict/apple</pre>
  <pre>POST /predict/grape</pre>
  <pre>POST /predict/tomato</pre>

## Tech Stack 
Javascript, Node.js, Express.js, MySQL, Prisma, Python, Flask, App Engine, Cloud Build, Cloud SQL, Cloud Storage, Secret Manager.

## Documentation API

<details>
  <summary>User</summary>

  - **Register**
  <pre>POST /register</pre>
  Request Body:
  ```json
  {
    "username": "John",
    "email": "john@gmail.com",
    "password": "john12345"
  }
  ```
  Response Body:
  ```json
  {
    "message": "User created successfully"
  }
  ```
  - **Login**
  <pre>POST /login</pre>
  Request Body:
  ```json
  {
    "email": "john@gmail.com",
    "password": "john12345"
  }
  ```
  Response Body:
  ```json
  {
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImVtYWlsIjoiaGVsbG8zQGdtYWlsLmNvbSIsImlhdCI6MTczMzkyMTk1MiwiZXhwIjoxNzM0MDA4MzUyfQ.tmWOVP2LJw_jBUQ27eTiaOcT3ORbQAQcEId_7bjAVf8"
  }
  ```
  - **Logout**
  <pre>POST /logout</pre>
  Response Body:
  ```json
  {
    "message": "Logged out successfully"
  }
  ```
  - **View Profile**
  <pre>GET /users</pre>
  Response Body:
  ```json
  {
    "message": "Success grab data user",
    "data": {
        "name": "John",
        "email": "john@gmail.com",
        "image": "https://i.imgur.com/HFmWnmJ.png"
    }
  }
  ```
  - **Update Profile**
  <pre>POST /users</pre>
  Request Body:
  ```json
  {
    "name": "John D",
    "email": "john@gmail.com"
  }
  ```
  Response Body:
  ```json
  {
    "message": "User updated successfully",
    "data": {
        "id": 1,
        "email": "john@gmail.com",
        "name": "John D",
        "image": "https://i.imgur.com/dETmvGX.png"
    }
  }
  ```
  - **Update Profile Image**
  <pre>POST /users/updateProfile</pre>
  Response Body:
  ```json
  {
    "message": "Profile image updated successfully"
  }
  ```

  - **Change Password**
  <pre>POST /users/changePassword</pre>
  Response Body:
  Request Body:
  ```json
  {
    "oldPassword": "john12345",
    "newPassword": "john123456",
    "confirmPassword": "john123456"
  }
  ```
  Response Body:
  ```json
  {
    "message": "Password successfully updated"
  }
  ```
</details>
<details>
  <summary>Predictions</summary>

  - **Predict**
  <pre>POST /predict/apple</pre>
  Response Body:
  ```json
  {
    "label": "Apple__Apple_scab",
    "confidence": 100.0,
    "disease_info": {
        "description": "Apple scab is a fungal disease that causes dark, sunken lesions on apples.",
        "name": "Apple Scab",
        "treatment": [
            "Grow scab-resistant apple cultivars such as Akane, Chehalis, Liberty, Prima, and Tydeman Red.",
            "Apply nitrogen to fallen leaves in the fall to increase decomposition and make them more palatable to earthworms. Use liquid fish solution or 16-16-16 fertilizer.",
            "Shred fallen leaves in the fall with a lawn mower to speed up decomposition.",
            "Prune trees to improve air circulation.",
            "Avoid wetting foliage when watering.",
            "Apply dolomitic lime in the fall to increase pH and reduce fungal spores.",
            "Spray fungicides (Bonide Captan, wettable sulfur, summer lime sulfur, or Spectracide Immunox) when temperatures are above 60°F and leaves or flowers are wet."
        ]
    },
  }
  ```
</details>