# CyaAPI
An API for spaced repetition learning using SM-2 algorithm, built in FastAPI.

## Motivation
The goal was to create a tool to track my spaced reptition learning, using FastAPI, SQLAlchemy, PostgreSQL and my package SuperMemo2.

## Run the API
```bash
./start.sh
```

## Run the tests
**Note:** install `pytest` using [pip](https://pip.pypa.io/en/stable/quickstart/).
```bash
pytest
```

## API Resources
<details open>
<summary>Stack</summary>

+ [GET /stacks](#get-stacks)
+ [GET /stacks/[stack_id]](#get-stacks_stack_id)
+ [GET /stacks/[stack_id]/cards](#get-stacks_stack_id_cards)
+ [POST /stacks](#post-stacks)
+ [PUT /stacks/[stack_id]](#put-stacks_stack_id)
+ [DELETE /stacks/[stack_id]](#delete-stacks_stack_id)
</details>

<details open>
<summary>Card</summary>

+ [GET /cards](#get-cards)
+ [GET /cards/[card_id]](#get-cards_card_id)
+ [POST /cards](#post-cards)
+ [POST /cards/first-review](#post-cards_first_review)
+ [PATCH /cards/[card_id]](#patch-cards_card_id)
+ [PATCH /cards/[card_id]/review](#patch-cards_card_id_review)
+ [DELETE /cards/[card_id]](#delete-cards_card_id)
</ul>
</details>

<br>

### GET /stacks
---
Returns a list of all the stacks.

<details>

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:** 
    ```json
    [ { "id": 1, "name": "Stack One", "cards": [] }, { "id": 2, "name": "Stack Two", "cards": [] } ]
    ```

</details>
<br>

<a name="get-stacks_stack_id">

### GET /stacks/[stack_id]
---
Returns a stack.

<details>

- **URL Params** <br>
Required: <br>
`stack_id=[integer]`

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:** { "id": 1, "name": "Stack Name", "cards": [] }

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:** { detail : "Stack with id={stack_id} not found" }
</details>

<br>

<a name="get-stacks_stack_id_cards">

### GET /stacks/[stack_id]/cards
---
Returns all the cards in a stack.

<details>

-  **URL Params** <br>
Required: <br>
`stack_id=[integer]`

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:** 
    ```json
    [
        {
            "name": "Card Name",
            "stack_id": 1,
            "prev_easiness": 2.5,
            "prev_interval": 1,
            "prev_repetitions": 1,
            "prev_review_date": "2021-03-03",
            "quality": 5,
            "id": 42,
            "easiness": 2.6,
            "interval": 1,
            "repetitions": 2,
            "review_date": "2021-03-04"
        }
    ]
    ```

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:** 
    ```json
    { "detail" : "Stack with id={stack_id} not found" }
    ```
</details>

<br>

### POST /stacks
---
Adds a new stack and returns it.

<details>

-  **Data Params** <br>
Required: <br>
`name=[string]`

- **Success Response:**
    - **Code:** 200 <br>
    **Content:** 
    ```json
    { "id": 1, "name": "Stack One", "cards": [] }
    ```

- **Error Response:**
    - **Code:** 422 Unprocessable Entity <br>
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    ```
</details>

<br>

<a name="put-stacks_stack_id">

### PUT /stacks/[stack_id]
---
Updates a stack.

<details>

-  **URL Params** <br>
Required: <br>
`stack_id=[integer]`

-  **Data Params** <br>
Required: <br>
`name=[string]`

- **Success Response:**
    - **Code:** 200 <br>
    **Content:**
    ```json
    { "id": 1, "name": "Stack One", "cards": [] }
    ```
- **Error Response:**
    - **Code:** 422 Unprocessable Entity <br>
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    ```

</details>

<br>

<a name="delete-stacks_stack_id">

### DELETE /stacks/[stack_id]
---
Deletes a stack.

<details>

-  **URL Params** <br>
Required: <br>
`stack_id=[integer]`

- **Success Response:**
    - **Code:** 204 No Content <br>
    **Content:** None

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:** 
    ```json
    { "detail": "Stack with id={stack_id} is not found" }
    ```
</details>

<br>

### GET /cards
---
Returns all cards

<details>

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:**
    ```json
    [
        {
            "name": "Card Name",
            "stack_id": 1,
            "prev_easiness": 2.5,
            "prev_interval": 1,
            "prev_repetitions": 1,
            "prev_review_date": "2021-03-03",
            "quality": 5,
            "id": 42,
            "easiness": 2.6,
            "interval": 1,
            "repetitions": 2,
            "review_date": "2021-03-04"
        }
    ]
    ```

</details>

<br>

<a name="get-cards_card_id">

### GET /cards/[card_id]
---
Returns a card.

<details>

-  **URL Params** <br>
Required: <br>
`card_id=[integer]`

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:**
    ```json
    {
        "name": "Card Name",
        "stack_id": 1,
        "prev_easiness": 2.5,
        "prev_interval": 1,
        "prev_repetitions": 1,
        "prev_review_date": "2021-03-03",
        "quality": 5,
        "id": 42,
        "easiness": 2.6,
        "interval": 1,
        "repetitions": 2,
        "review_date": "2021-03-04"
    }
    ```

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:**
    ```json
    { "detail" : "Card with id={card_id} not found" }
    ```

</details>

<br>

### POST /cards
---
Adds a card into a stack.

<details>

-  **Data Params** <br>
Required: <br>
`name=[string]` <br>
`stack_id=[integer]` <br>
`quality=[integer]` <br>
`prev_easiness=[float]` <br>
`prev_interval=[integer]` <br>
`prev_repetitions=[integer]` <br>
`prev_review_date=[date]`

- **Success Response:**
    - **Code:** 201 Created <br>
    **Content:**
    ```json
    {
        "name": "Card Name",
        "stack_id": 1,
        "prev_easiness": 2.5,
        "prev_interval": 1,
        "prev_repetitions": 1,
        "prev_review_date": "2021-03-03",
        "quality": 5,
        "id": 42,
        "easiness": 2.6,
        "interval": 1,
        "repetitions": 2,
        "review_date": "2021-03-04"
    }
    ```

- **Error Response:**
    - **Code:** 422 Unprocessable Entity <br>
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "{ONE OF THE DATA PARAMS}"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    ```
</details>

<br>

<a name="post-cards_first_review">

### POST /cards/first-review
---
Adds a first time reviewed card into a stack.
<details>

-  **Data Params** <br>
Required: <br>
`name=[string]` <br>
`stack_id=[integer]` <br>
`quality=[integer]`

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:**
    ```json
    {
        "name": "Card Name",
        "stack_id": 1,
        "prev_easiness": 2.5,
        "prev_interval": 1,
        "prev_repetitions": 1,
        "prev_review_date": "2021-03-03",
        "quality": 5,
        "id": 1,
        "easiness": 2.6,
        "interval": 1,
        "repetitions": 2,
        "review_date": "2021-03-04"
    }
    ```

- **Error Response:**
    - **Code:** 422 Unprocessable Entity <br>
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "{ONE OF THE DATA PARAMS}"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    ```

</details>

<br>

<a name="patch-cards_card_id">

### PATCH /cards/[card_id]
---
Partially updates a card.

<details>

-  **URL Params** <br>
Required: <br>
`card_id=[integer]`

-  **Data Params** <br>
Optional: <br>
`name=[string]` <br>
`stack_id=[integer]` <br>
`quality=[integer]` <br>
`prev_easiness=[float]` <br>
`prev_interval=[integer]` <br>
`prev_repetitions=[integer]` <br>
`prev_review_date=[date]`

- **Success Response:**
    - **Code:** 200 OK <br>
    **Content:**
    ```json
    {
        "name": "Card Name",
        "stack_id": 1,
        "prev_easiness": 2.5,
        "prev_interval": 1,
        "prev_repetitions": 1,
        "prev_review_date": "2021-03-03",
        "quality": 5,
        "id": 1,
        "easiness": 2.6,
        "interval": 1,
        "repetitions": 2,
        "review_date": "2021-03-04"
    }
    ```

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:**
    ```json
    { "detail" : "Card with id={card_id} not found" }
    ```

</details>

<br>

<a name="patch-cards_card_id_review">

### PATCH /cards/[card_id]/review
---
Updates a card with the review quality and calculates the next review date.

 <details>

-  **URL Params** <br>
Required: <br>
`card_id=[integer]`

-  **Data Params** <br>
Required: <br>
`quality=[integer]` <br>
Optional: <br>
`prev_review_date=[date]`

- **Success Response:**
    - **Code:** 200 <br>
    **Content:**
    ```json
    {
        "name": "Card Name",
        "stack_id": 1,
        "prev_easiness": 2.5,
        "prev_interval": 1,
        "prev_repetitions": 1,
        "prev_review_date": "2021-03-03",
        "quality": 5,
        "id": 1,
        "easiness": 2.6,
        "interval": 1,
        "repetitions": 2,
        "review_date": "2021-03-04"
    }
    ```

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:**
    ```json
    { "detail" : "Card with id={card_id} not found" }
    ```

    - **Code:** 422 Unprocessable Entity <br>
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "quality"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    ```

</details>

<br>

<a name="delete-cards_card_id">

### DELETE /cards/[card_id]
---
Deletes a card.

<details>

-  **URL Params** <br>
Required: <br>
`card_id=[integer]`

- **Success Response:**
    - **Code:** 204 No Content <br>
    **Content:** None

- **Error Response:**
    - **Code:** 404 NOT FOUND <br>
    **Content:**
    ```json
    { "detail" : "Card with id={card_id} not found" }
    ```

</details>

<br>