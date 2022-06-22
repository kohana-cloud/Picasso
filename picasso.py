from src.aws_session import AWS_Session
from src.aws_ecr import AWS_ECR

if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    aws_ecr_instance = AWS_ECR(aws_internal_session)
    #aws_ecr_instance.aws_ecr_add('hello-kohana', 'hello-kohana')
    #aws_ecr_instance.aws_ecr_delete('hello-kohana', 'latest')
    
    print(aws_ecr_instance.aws_ecr_list_repo())