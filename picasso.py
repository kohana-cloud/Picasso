from src.aws_session import AWS_Session
from src.aws_ecr import AWS_ECR
from src.aws_ecs import AWS_ECS

if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    aws_ecr_instance = AWS_ECR(aws_internal_session)
    aws_ecs_instance = AWS_ECS(aws_internal_session)
    #aws_ecs_instance.create_instance_profile('sample-cluster-009-instance-profile', 'la-merda')
    aws_ecs_instance.aws_ecs_create("sample-cluster-001", 't2-micro', '032622136258.dkr.ecr.us-east-1.amazonaws.com/hello-kohana:latest', 'sample-stage-service-001', 'sample-stage-container-001')
    #aws_ecs_instance.aws_ecs_delete_cluster("webservices-cluster32")
    #aws_ecr_instance.aws_ecr_add('hello-kohana', 'hello-kohana')
    #aws_ecr_instance.aws_ecr_delete('hello-kohana', 'latest')
    
    #print(aws_ecr_instance.aws_ecr_list_repo())