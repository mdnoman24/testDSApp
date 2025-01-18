from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis=get_redis_connection(
    host='redis-13980.c339.eu-west-3-1.ec2.redns.redis-cloud.com',
    port=13980,
    password='A9EAM68RA1HgkYsP4jxFQctXE5ZRuaiP',
    decode_responses=True
)
class Product(HashModel):
    name: str
    price: float
    quantity: int  
    
    class Meta:
        database = redis
       
class Patient(HashModel):
    patient_key: str
    person_id_hashed: str
    full_name: str
    first_name: str
    last_name: str
    phone_number: str
    address: str
    postal_code: str
    street_number: str
    street_name: str
    gender_code: str
    gender: str
    birth_year: str
    birth_date: str
    patient_id: str

    class Meta:
        database = redis

@app.post('/patients')
def create_product(patient: Patient):
    patient.save()
    return patient 

@app.get('/patients')
def all_products():
    
    return [format_patient(pk) for pk in Patient.all_pks()]


@app.post('/products')
def create_product(product: Product):
    
    return product.save()

def format_product (pk:str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }
def format_patient(pk: str):
    patient = Patient.get(pk)
    return {
        'id': patient.pk,
        'patient_key': patient.patient_key,
        'full_name': patient.full_name,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'phone_number': patient.phone_number,
        'address': patient.address,
        'postal_code': patient.postal_code,
        'street_number': patient.street_number,
        'street_name': patient.street_name,
        'gender_code': patient.gender_code,
        'gender': patient.gender,
        'birth_year': patient.birth_year,
        'birth_date': patient.birth_date,
        'patient_id': patient.patient_id
    }

@app.get('/products')
def all_products():
    
    return [format_product(pk) for pk in Product.all_pks()]


@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete_product(pk: str):
    return Product.delete(pk)



    