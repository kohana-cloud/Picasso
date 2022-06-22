from src.aws_session import AWS_Session
from src.aws_ecr import AWS_ECR
from src.aws_ecs import AWS_ECS

if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    aws_ecr_instance = AWS_ECR(aws_internal_session)
    aws_ecs_instance = AWS_ECS(aws_internal_session)
    #aws_ecs_instance.aws_ecs_create("webservices-cluster2", "test", "test")
    aws_ecs_instance.aws_ecs_delete_cluster("webservices-cluster2")
    #aws_ecr_instance.aws_ecr_add('hello-kohana', 'hello-kohana')
    #aws_ecr_instance.aws_ecr_delete('hello-kohana', 'latest')
    
    #print(aws_ecr_instance.aws_ecr_list_repo())