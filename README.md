# WebAPI

This repo is used to host my FastAPI script, along with the required dockerfile for creating the docker image to be used on AWS lambda, and the buildspec.yaml for deployment via AWS CodeBuild.

More info can be found at https://jonathangosling.co.uk

## Get FastAPI app in python ready for deployment on Lambda
1. Lambda needs a 'handler function' that it can work with. When lambda is run, it will execute the handler function.
2. Use Mangum for the handler function: "Mangum is an adapter for **running ASGI** (FastAPI is an ASGI web framework) applications in **AWS Lambda** to handle Function URL, API Gateway, ALB, and Lambda@Edge events."
3. This is highly convenient as it will automatically route the handler function request to our app (FastAPI object) subpaths.
4. In python script 'from mangum import Mangum'
5. Simply pass the FastAPI app object into Mangum function: handler = Mangum(app)

## Create Lambda function
1. In Lambda, 'Create function' with a 'Python \<version\>' runtime
2. In 'runtime setting' 'edit' the handler to \<python file name\>.\<handler name\> (e.g. main.handler) so that lambda can locate the handler once files uploaded
3. Need to upload all dependencies/packages used.
    - Can zip files, along with all packages/modules used (from your local (virtual) environment, in Lib/site-packages.  Note: in lambda all environment packages will need to be in the base directory as it will not interpret them as part of an environment so 'import' calls to packages will look in the base directory where the python script is located)
    - In this project, we use a docker image. In which case select 'container image' when creating lambda function. You may want to have a docker image ready to test.
4. Create a test - In 'Code source' - Click 'Test' to 'configure test event' - give it any name - in 'template' choose 'API Gateway AWS Proxy'
    - Edit the 'Event JSON' created by the template to direct to a test "path" (e.g. the root "/") and with a correct "httpMethod" for the application (e.g. "GET"). Copy these changes through to the "proxy" ("/") and "path" and "httpMethod" later in the JSON script
5. Test the function - go to 'test' and click test
6. *Can* add a HTTP endpoint directly to the lambda in 'configuration' -> 'function URL' -> 'create function URL' -> 'Auth type' NONE for public access (also add 'configure cross-origin resource sharing) -> Save

## Dockerfile (and building docker image and pushing to ECR)
1. Create dockerfile:
   - base image 'FROM public.ecr.aws/lambda/python:3.8' for python on lambda
   - COPY requirements.txt and application (main.py) files
   - RUN pip install -r /requirements.txt to set up environment dependencies
   - CMD ["/main.handler"] to execute the handler function as required by lambda
2. Create ECR repo
3. (If not using code build, or manually testing) build docker image and push to ECR repo
4. Commands for this can be found in the ECR repo under 'view push commands'. They are:
   - aws ecr get-login-password --region \<your-availability-zone\> | docker login --username AWS --password-stdin \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com
   - docker build -t \<your-ecr-repo\>
   - docker tag \<your-ecr-repo\>:latest \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest
   - docker push \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest
5. If the lambda function is already created, can update with the new docker image from the lambda console or using:
   - aws lambda update-function-code --function-name \<your-lambda-function\> --image-uri \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest

## Using CodeBuild to automate the process of building and pushing docker image, and updating lambda
1. Create buildspec.yaml file. This is the file CodeBuild will use to execute comands
    - version: 0.2
    - phases:
      - prebuild: in here we will run the command for signing into ecr and docker (aws ecr get-login-password --region \<your-availability-zone\> | docker login --username AWS --password-stdin \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com)
      - build: here, we will build and push the docker image ('docker build -t \<your-ecr-repo\>' 'docker tag \<your-ecr-repo\>:latest \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest' 'docker push \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest)'
      - post_build: here we'll update the lambda (aws lambda update-function-code --function-name \<your-lambda-function\> --image-uri \<your-aws-account-number\>.dkr.ecr.\<your-availability-zone\>.amazonaws.com/\<your-ecr-repo\>:latest)
2. In CodeBuild, 'create new project'
3. Enter a name and description
4. Select GitHub as 'source provider', choose your desired repo and enter 'main' as the source version
5. Enable 'webhook' and select 'Event type' 'PUSH' for CD every time we push to main
6. 'Operating system' - 'Ubuntu'
7. 'Runtime' - 'Standard'
8. 'Image' - choose any e.g. standard:5.0
9. Enable 'Privileged' to allow codebuild to build docker images
10. Edit the service role policies to allow access to ECR and lambda
    - Go to the service role (Can find the service role in 'build details' of the build project)
    - In permissions policies, click on the CodeBuildBasePolicy…. 
    - Click 'edit policy' and edit the JSON to include these permissions, review and save:
```json
        {
            "Effect": "Allow",
            "Action": [
                "lambda:AddPermission",
                "lambda:RemovePermission",
                "lambda:CreateAlias",
                "lambda:UpdateAlias",
                "lambda:DeleteAlias",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:PutFunctionConcurrency",
                "lambda:DeleteFunctionConcurrency",
                "lambda:PublishVersion"
            ],
            "Resource": "arn:aws:lambda:<your-availability-zone>:<your-aws-account-number>:function:<your-lambda-function>"
        },
        {
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Resource": "arn:aws:ecr:<your-availability-zone>:<your-aws-account-number>:repository/<your-ecr-repo>",
            "Effect": "Allow"
        },
```
11. Test: make a push to github and check
    - CodeBuild runs without any errors (errors can be found in the 'phase details' and 'build logs' of the build project)
    - The lambda function is updated as expected (test the lambda in aws or check the url)

## 	Build REST API on API Gateway:
1. Click 'build' on REST API
2. Create 'New API'
3. Enter 'API name'
4. Hit 'Create'
5. It will now want you to make your new API
6. On Actions, choose 'create method'
7. Choose 'GET' (this will allow us to setup the action of get requests to the root)
8. Click the tick (validate)
9. Integration type: Lambda Function
10. Tick 'Use Lambda Proxy Integration'
11. Add your lambda function in 'Lambda Function'
12. Hit 'Save'
13. 'Test'
14. Add sub pages/endpoints. NOTE: API Gateway is quite funny about this - I learnt this the hard way after much frustration! You can’t direct multiple endpoints to the same lambda function without using proxy! Essentially, API Gateway wants to take care of endpoints itself, to take care of them in your FastAPI script in the lambda function you have to use proxy integration in API Gateway.
    - To catch all possible endpoint go - 'Actions', 'Create resource'
    - Tick 'Configure as proxy resource'
    - Hit 'create resource'
    - Add a get method in the 'proxy' sub directory following the same process as above
15.  On 'Actions', click 'Deploy API'
16.  Under 'Deployment stage', select 'new stage'
17.  Give it a name, i.e. 'dev'
18.  Click 'deploy'

## Direct custom URL in Route 53 to API Gateway:
1. On the API Gateway page, click 'custom domain names'
2. Click 'create'
3. Add domain name (jonathangosling.co.uk or api.jonathangosling.co.uk …)
4. Click 'Create a new ACM certificate'
   - On the ACM manager, click 'request'
   - 'request public certificate' -> next
   - Use DNS validation
   - 'confirm and request'
   - Certificate will be 'pending validation'. Need to validate in Route 53 and add a CNAME record. Can get AWS to do this for us by clicking 'Create record in Route 53'
   - Wait for status to reach 'issued'
5. Choose certificate for the domain name
6. Hit 'create domain name'
7. On your custom domain name in the API Gateway page, click on 'API mappings'
8. 'add new mapping'
9. Add the API Gateway and stage from the dropdowns and hit 'save'
10. Move over to Route 53
11. Click 'create record'
12. Record name should match your API gateway custom domain (jonathangosling.co.uk or add any prefix)
13. Record type A
14. Make it an 'alias'
15. 'Route traffic to' 'Alias to API Gateway API'
16. Choose region corresponding to your API Gateway
17. 'Choose endpoint' to point to your API Gateway
18. Hit 'create records'

## Phew, that was a lot of detail (maybe a little too much).
Anyway, here's some links to even more details:
1. FastAPI on Lambda
   
   https://www.youtube.com/watch?v=RGIM4JfsSk0
2. API gateway with custom domain name
   
   https://www.youtube.com/watch?v=ESei6XQ7dMg&t=722s (connecting API gateway to Route 53)

   https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/learn/lecture/13672554#overview (using API gateway with lambda - a short video from a paid course on Udemy. Will need to have access to the course :(, but it's extremely helpful for getting to grips with AWS if interested :))
3. Some resources on using numerous endpoints and the root all using the same lambda function with proxy integration
   
   https://stackoverflow.com/questions/35773025/is-it-possible-to-use-wildcards-or-catch-all-paths-in-aws-api-gateway
   
   https://aws.amazon.com/blogs/aws/api-gateway-update-new-features-simplify-api-development/
   
   https://stackoverflow.com/questions/60498809/how-can-i-use-proxy-to-handle-the-root-resource-on-api-gateway-to-return-body
4. Using CodeBuild for CI/CD from github with docker/ECR and lambda

   https://www.youtube.com/watch?v=AmHZxULclLQ&t=563s (lambda)

   http://beta.awsdocs.com/services/code_build/build_docker_images/ (docker)

   https://www.youtube.com/watch?v=3CcGtRidF9c (docker)

    Note: in these docs they use the command

    $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)

    in the buildspec. Found a few problems using this:
    - Get-login --no-include-email is a depracated command
    - The $() syntax used for command substitution in Linux-based shells caused error, passing command directly solved error
    - Found I needed to 'authenticate docker client'

    Using the command

    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 517574620103.dkr.ecr.us-east-1.amazonaws.com

    Solves all.
