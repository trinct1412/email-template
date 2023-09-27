## WorkDirectory:


    ├─┬ pi
    │ ├─┬ default                          # Directory for input for email include: template and customers
    │ │ ├─┬ customers.csv                  # file for customers
    │ │ ├─┬ email_template.json            # file for template
    │ ├─┬ test                             # Directory for test
    │ │ ├─┬ unit_test.py                   # file for template
    ├─ docker-compose.yml                  # Docker build app
    ├─ Dockerfile                          # Docker build image
    ├─ README.md                           # Readme file 
    ├─ requirements.txt                    # Package file requirements
    ├─ send_mail.py                        # Run send_mail


## Requiments:

    - python: 3.8.6

## Run Project:

    1. pip install virtualenv
    2. python -m virtualenv env
    3. source env/bin/activate
    4. pip install -r requirements.txt
    5. python send_email.py
    or 
    5. python send_email.py ./default/email_template.json ./default/customers.csv ./default/output.json ./default/errors.csv

## Run Project By Docker:

    1. pip freeze > requirements.txt
    2. docker-compose up

## Tutorial Test :

    1. Unit test:
       - python -m unittest test.unit_test

###What do you love about your solution?
 - About design:
   - I choose the coroutine to design because i will expand the feature for send mail by SMTP in the future
 - About the Project:
   - Build the docker file to create the image run project
   - If i have more time to build I will write more test for it specially unittest and integration test.
   - Export just one the procedure function in the module send_email.py
 
