**Course URL**  
https://www.youtube.com/playlist?list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM


**Git Repo**
Self  : <https://github.com/himanshuSPaul/FASTAPI>

## **Execute the code**

**Get into This path**  
(venv) D:\Learning\VSCode\FastAPI\FASTAPI\YTLearning\code

**Run uvicorn server**  
uvicorn main:app --reload

**API URL**      <http://127.0.0.1:8000>   
**Swagger Url**  <http://127.0.0.1:8000/docs#/>

## **Asignment**  
Video :8
> Create defination for root path .
> Create two function with different defination for root path to test function precedency order

Video :9  
> Set up Postman tool to test FAST Api Endpoint.

Video :10
> Create Post request path and send input data from Postman body and show it in webpage as output

Video :11    Schema validation Using Pydantic model
> Define a pydandantice model to validate user input

> Modify the pydantice model to handle missing field in user input using default Value 
  
> Modify the pydantice model to handle missing field in user input by making the field optionl

Video :12  
> Exaplain CRUD Operation  

Video :13 Create CRUD based Application  
> Take the user input from Postman , insert into to post list . It should return what ever object inserted into list  

> Show all the entries presen in list using POST request. 

Video :14 
> Save Request Sessions in PostMan for Create post and List Posts endpoints.

Video :15
> Get Post for specific id using path parameter  

> Test application behavior by passing different type of input data in POST requst while fetching specific id using Path pareameter. Also , understand difference between specifying function data type and hardcodind input datan type to desire data type inside function .

Video :16  Path precedency
> Define path for getting latest post. Also, understand path prcedency . Understand different approach to fix the issue .

Video :17 Handle Respose Status Code
> Define Proper Response Code For :
    - When requested post id is not found , then send 404 HTTP status code along with HTTP exception.
    - When requested post is created , then send 201 HHTP status code.
    - When requested post is 

Video :18 Delet operartion of CRUD
> Delete post based on input post id . While deleteing handle appropeate return Status code . If Requested post id not avaialble raise HTTPException

Video :19 Update operartion of CRUD
> Update content based on input post id. While updating, if input post id is not present then raise HTTP Not found exception

Video 20: FAST APi documentation
Video 21: Moving code to src folder 
Video 22 to 37 : Basics Of Postgres Database and SQL 
