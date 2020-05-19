**Create Survey**
----
  Create a survey by giving a name

* **URL**

  `survey/`

* **Method:**

  `POST`

* **Data Params**

  ```
  {
    "survey_name": (name)
  }
  ```
* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:** 
    ```
    {
        'name': (name),
        'questions': [],
        'average': None,
        'standard_deviation': None,
        'minimum': None,
        'maximum': None
    }
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** 'survey_name' not passed as data params <br />
    **Content:**
    ```
    {
        'error': "'survey_name' has to be a data param"
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** A survey with the 'survey_name' already exists <br />
    **Content:**
    ```
    {
        "error": "survey name already exist, please choose a new one"
    }
    ```
---