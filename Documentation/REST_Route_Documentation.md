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

**Create Question**
----
  Create and add a question inside an existing survey

* **URL**

  `question/`

* **Method:**

  `POST`

* **Data Params**

  ```
  {
    "survey_name": (name),
    "question_text": (question)
  }
  ```
* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:** 
    ```
    {
        "question": (question),
        "answers": [],
        "average": null,
        "standard_deviation": null,
        "minimum": null,
        "maximum": null
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
    **Cause:** 'question_text' not passed as data params <br />
    **Content:**
    ```
    {
        'error': "'question_text' has to be a data param"
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** A survey with the 'survey_name' does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey does not exist'
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** A question with the 'question_text' already exist <br />
    **Content:**
    ```
    {
        'error': 'question already exist, find a new one'
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** You have exeeded the number of questions that can be stored (max = 10) <br />
    **Content:**
    ```
    {
        'error': 'you cannot add another question (maximum questions = 10)'
    }
    ```
---