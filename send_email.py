import sys
import os
import json
import pandas as pd
import csv
from collections import namedtuple
from datetime import datetime

default_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default')
datetime_ = datetime.now()
default_ = (os.path.join(default_dir, 'email_template.json'),
            os.path.join(default_dir, 'customers.csv'),
            os.path.join(default_dir, f'{datetime_.date()}/{datetime_.time()}/output.json'),
            os.path.join(default_dir, f'{datetime_.date()}/{datetime_.time()}/errors.csv'))

FileMail = namedtuple('FileMail', ('template', 'customers', 'output', 'errors'), defaults=default_)
Customer = namedtuple('Customer', ('TITLE', 'FIRST_NAME', 'LAST_NAME', 'EMAIL'))
sys.argv.pop(0)

file_mail = FileMail(*sys.argv)


def auto_generate_folder():
    try:
        if sys.argv:
            for file_path in file_mail:
                directory = os.path.exists(os.path.dirname(file_path))
                if not directory:
                    os.makedirs(str(directory))
        else:
            os.makedirs(os.path.join(default_dir, f'{datetime_.date()}/{datetime_.time()}'))
    except Exception as e:
        raise Exception(e, "can't create file")


def get_template():
    with open(file_mail.template, 'r+') as f:
        template = json.load(f)
    return template


def send_customers(customers, next_coroutine):
    try:
        next_coroutine.send(customers)
    except StopIteration:
        ...
    next_coroutine.close()


def handler(next_coroutine_success, next_coroutine_error):
    customers = (yield)
    for customer in customers.iterrows():
        customer = Customer(*customer[1])
        if pd.isna(customer.EMAIL):
            next_coroutine_error.send(customer)
        else:
            next_coroutine_success.send(customer)


def output_success():
    try:
        template = get_template()
        date_ = datetime_.date().strftime('%d %B %Y')
        while True:
            customer = (yield)
            customer = customer._asdict()
            customer['TODAY'] = date_
            template_copy = template.copy()
            template_copy['body'] = template_copy.get('body').format().format(**customer)
            with open(file_mail.output, 'a+') as f:
                json.dump(template_copy, f, indent=4)
                f.write('\n')
    except GeneratorExit:
        pass
    except Exception as e:
        print('errors', e)


def output_error():
    try:
        while True:
            customer = (yield)
            with open(file_mail.errors, 'a+') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(customer)
    except GeneratorExit:
        pass


def execute(customer):
    osc = output_success()
    ope = output_error()
    osc.__next__()
    ope.__next__()
    hd = handler(next_coroutine_success=osc, next_coroutine_error=ope)
    hd.__next__()
    send_customers(customers=customer, next_coroutine=hd)


def producer(chunk_size=500):
    auto_generate_folder()
    with pd.read_csv(file_mail.customers, header=None, chunksize=chunk_size, skiprows=1, sep=';') as customers:
        for customer in customers:
            execute(customer)


if __name__ == '__main__':
    producer()
