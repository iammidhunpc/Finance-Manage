# Finance-Manage
# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/iammidhunpc/Finance-Manage.git
    $ cd Finance-Manage
    
Activate the virtualenv for your project.

     $ virtualenv env
     $ source env/bin/activate

Install project dependencies:

    $ pip install -r requirements.txt
    

Then simply apply the migrations:

    $ python manage.py migrate
    use same databse to use admin token

To create new superuser:

    $ python manage.py createsuperuser
    create admin token using the admin panel for accessing the apis.

You can now run the development server:

    $ python manage.py runserver
    
### Main features

* Financial department owner/head can add/update an invoice record.

* Shorten url is generated while creating each invoice using Bit.ly.

* Customers can pay using the shorten url using stripe payment.


