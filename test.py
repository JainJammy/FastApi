"""importing the required modules for pytest fastapi mongodb"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List
from pymongo import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId
"""creating the pydantic models and the schema structure of employee and department"""
class Employee(BaseModel):
    name: str
    email: str
    department_id: str
class Department(BaseModel):
    name:str      
app = FastAPI()
# MongoDB connection
"""creating mongo database connection using localhost"""
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("EmployeManagement")
employees_collection = db.get_collection("employees")
departments_collection = db.get_collection("departments")
client = TestClient(app)

"""Post request for employees to insert the data"""
@app.post("/employees/")
async def create_employee(employee: Employee):
   print(employee)
   result = employees_collection.insert_one(employee.dict())
   print("your employee record is",result)
"""Get request for employees to get the employee specific record"""   
@app.get("/employees/{employee_id}")
async def read_employee(employee_id:str):
    employee_fetched_data=employees_collection.find_one({"_id":ObjectId(employee_id)})
    print("employee fetched data is",employee_fetched_data)
"""Put request for employees to update the specific employee record"""    
@app.put("/employees/{employee_id}")
async def update_employee(employee_id:str,employee:Employee):
    employee_updated_data=employees_collection.update_one({"_id":ObjectId(employee_id)},{"$set":employee.dict()})
    print(employee_updated_data)
"""Delete request for employees to delete the specific employee record"""    
@app.delete("/employees/{employe_id}")
async def delete_employee(employee_id:str):
    employee_delete_data=employees_collection.delete_one({"_id":ObjectId(employee_id)})
    print(employee_delete_data)
"""Post request for departments to insert the record"""    
@app.post("/departments/")
async def create_department(department:Department):
    department_create=departments_collection.insert_one(department.dict())
    print("department_create",department_create)
"""Get request for departments to get specific records for department"""    
@app.get("/departments/{department_id}")
async def read_department(department_id:str):
    department_fetched_data=departments_collection.find_one({"_id":ObjectId(department_id)}) 
    print(department_fetched_data)
"""Put request for departments to update the specific records for department"""    
@app.put("/departments/{department_id}")
async def update_department(department_id:str,department:Department):
    department_updated_data=departments_collection.update_one({"_id":ObjectId(department_id)},{"$set":department.dict()})
    print(department_updated_data)
"""Delete request for departments to delete the specific records for department"""    
@app.delete("/departments/{department_id}")
async def delete_department(department_id:str):
    department_delete_data=departments_collection.delete_one({"_id":ObjectId(department_delete_data)})
    print(department_delete_data)    
"""Get the records of employee with departments"""
@app.get("/employeedepartments/{employeedepartmentid}")
async def get_employee_deparment(employeedepartmentid:str):
    """Not Implementing the paginator logic beacuse this is mongo db mongo db always filter single document using collection.find({filter:value})"""
    employees_department=employees_collection.find_one({"_id":ObjectId(employeedepartmentid)})
    print("employees_department is",employees_department)
    temp_dict={}
    for data in employees_department:
        print("data is",data)
        temp_dict["name"]=employees_department.get(data)
        temp_dict["email"]=employees_department.get(data)
        if "department_id" in data:
            """fetched the record of specific document of employee that department id reference to department collection using department id fetching the department document"""
            department_data=departments_collection.find_one({"_id":ObjectId(employees_department.get("department_id"))})
            print("your department_data is",department_data)
"""Implementing the test cases for specific api request  unit test using pytest for testing  run command on terminal pytest -s"""    
@pytest.fixture
def sample_employee():
    return {"name": "rinkit Doe", "email": "ronit@example.com", "department_id": "65cfbb3513f07f5006a4a6ec"}
@pytest.fixture
def sample_employee_update():
    return {"name":"John Doe","email":"john5@example.com","department_id":"1"}
@pytest.fixture
def sample_department():
    return {"name":"CS"}
@pytest.fixture
def sample_department_update():
    return {"name":"CS"}

def test_create_employee(sample_employee):
    response = client.post("/employees/", json=sample_employee)
    print("response is",response)
def test_get_employee():
    employee_id="65cfbd98c70e4fa69a90e590"#Mongo db employee collection specific _id unique for employee document
    response=client.get(f"/employees/{employee_id}")
    print("response is",response)
def test_update_employee(sample_employee_update):
    employee_id="65cfbd98c70e4fa69a90e590"#Mongo db employee collection specific _id unique for employee document
    response=client.put(f"/employees/{employee_id}",json=sample_employee_update)
    print("response is",response)
def test_delete_employee():
    employee_id="65cfbd98c70e4fa69a90e590"#Mongo db employee collection specific _id unique for employee document
    response=client.delete(f"/employees/{employee_id}")
    print("response is",response)
def test_create_department_data(sample_department):
    response=client.post("/departments/",json=sample_department)
    print("response is",response)
def test_get_department():
    department_id="65cfbae2db62ac770d5d64ba"#Mongo db department collection specific _id unique for department document
    response=client.get(f"/departments/{department_id}")
    print("response is",response)
def test_update_department(sample_department_update):
    department_id="65cfbae2db62ac770d5d64ba"#Mongo db department collection specific _id for department document
    response=client.put(f"/departments/{department_id}",json=sample_department_update)
    print("response is",response)
def test_delete_department():
    department_id="65cfbae2db62ac770d5d64ba"#Mongo db department collection specific _id for department document
    response=client.delete(f"/departments/{department_id}")
    print("response is",response)
def test_employeewithdepartment():
    employeedepartmentid=ObjectId("65cfbd98c70e4fa69a90e590")#getting the specific document of employee from employee collection
    response=client.get(f"/employeedepartments/{employeedepartmentid}")
    print("response is",response)
"""running on localhost to test the api endpoints command to run uvicorn test:app --reload"""    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
