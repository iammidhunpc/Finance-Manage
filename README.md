# Finance-Manage
## Getting Started

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

To create new superuser:

    $ python manage.py createsuperuser

You can now run the development server:

    $ python manage.py runserver
    Access the apis by login as superuser

Tests
To run the tests, cd into the directory where manage.py is:

	$ python manage.py test

For the Stripe payment testing refer to the [basic test card numbers](https://stripe.com/docs/testing#cards) for more details.

Api documentaion refer [postman doc](https://documenter.getpostman.com/view/5357735/TzJrByfy)

#### WebHooks

    Stripe uses webhooks to notify application when an event happens in the account.
    In order to use webhooks, we need to:
1) Install Stripe CLI and test the endpoint using the [Stripe CLI](https://stripe.com/docs/stripe-cli)
2) Register the endpoint with Stripe refer [ endpoint register](https://dashboard.stripe.com/test/webhooks)

### Main features

* Financial department owner/head can add/update an invoice record.

* Shorten url is generated while creating each invoice using Bit.ly.

* Customers can pay using the shorten url using stripe payment.



