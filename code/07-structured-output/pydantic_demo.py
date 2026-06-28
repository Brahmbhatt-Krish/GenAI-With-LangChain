from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Student(BaseModel):
    name:str = 'krish' # default value    name:str   <-- this is also valid.
    age:Optional[int]
    email:EmailStr
    marks: float = Field(gt=0,lt=10,default=3,description='a decimal value of students marks')

one_student = {'age':21,'email':'abc@gmail.com'}

new_stu = Student(**one_student)

print(new_stu)