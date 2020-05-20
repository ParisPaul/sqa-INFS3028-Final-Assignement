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

**Get List Servey**
----
  Get a list of the names of all the existing surveys

* **URL**

  `survey/`

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```
    {
        'surveys': []
    }
    ```
---

**Get one survey**
----
  Get all information about a survey

* **URL**

  `survey/<str:survey_name>/`

* **Method:**

  `GET`

* **URI Params**

  survey_name: (string)

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```
    {
        'name': (survey_name),
        'questions': [],
        'average': None,
        'standard_deviation': None,
        'minimum': None,
        'maximum': None
    }
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** A survey with the 'survey_name' does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey does not exist'
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

**Create Survey Response**
----
  Create a survey response for a desired survey

* **URL**

  `survey_response/`

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
        'survey_name': (name),
        'id': int,
        questions....
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
    **Cause:** The desired survey does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey does not exist'
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** When there is no questions in the survey <br />
    **Content:**
    ```
    {
        'error': 'this survey has no questions'
    }
    ```
---

**Update survey response**
----
  Once you know the answers you want to submit, you update the survey response and it it will replace in the app with wat you answered
* **URL**

  `survey_response/`

* **Method:**

  `PATCH`

* **Data Params**

  ```
  {
  'survey_response': {
    'id': '0',
    'survey_name': (survey_name),
    'description': 'Each questions can be answered with a number between 1 and 5 included.',
    'questions': {
        "(question)": (answer)
        ...
      }
    }
  }
  ```
* **Success Response:**

  * **Code:** 200 CREATED <br />
    **Content:** 
    ```
    {
    'survey_response': {
      'id': '0',
      'survey_name': (survey_name),
      'description': 'Each questions can be answered with a number between 1 and 5 included.',
      'questions': {
          "(question)": (answer)
          ...
        }
      }
    }
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** Survey does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey does not exist, name may be wrong'
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** Survey response does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey response does not exist, it may be wrong'
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** When a question does not exist or has changed <br />
    **Content:**
    ```
    {
        'error': "the question '(questio)' does not exist OR the number is not between 1 and 5"
    }
    ```

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** When an answer is not between 1 and 5 included <br />
    **Content:**
    ```
    {
        'error': "the question '(question)' does not exist OR the number is not between 1 and 5"
    }
    ```
---

**Get all survey response**
----
  Get all survey responses from one survey
* **URL**

  `survey_response/<str:survey_name>/`

* **Method:**

  `GET`

* **URI Params**

  survey_name: (string)

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```
    {
    'survey_responses': [(survey_response), ...]
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Cause:** Survey does not exist <br />
    **Content:**
    ```
    {
        'error': 'survey does not exist, name may be wrong'
    }
    ```
---
