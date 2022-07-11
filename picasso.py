from src.aws_session import AWS_Session
from src.aws_ecr import AWS_ECR
from src.aws_ecs import AWS_ECS
from src.aws_s3 import AWS_S3

if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    aws_ecr_instance = AWS_ECR(aws_internal_session)
    aws_ecs_instance = AWS_ECS(aws_internal_session)
    aws_s3_instance = AWS_S3(aws_internal_session)

    #aws_s3_instance.create("omg-the-bucket", "us-east-2")
    all_account_buckets = aws_s3_instance.list_all()
    first_bucket = all_account_buckets[0]
    print(first_bucket)
    #print(aws_s3_instance.destroy(all_account_buckets[2]['Name']))
    #print(aws_s3_instance.apply_bpa(first_bucket['Name']))


    #aws_ecr_instance.aws_ecr_add('hello-kohana', 'hello-kohana')
    #aws_ecr_instance.aws_ecr_delete('hello-kohana', 'latest')
    #print(aws_ecr_instance.aws_ecr_list_repo())

    #aws_ecs_instance.create_instance_profile('sample-cluster-009-instance-profile', 'la-merda')
    #aws_ecs_instance.aws_ecs_create("sample-cluster-003", 't2-micro', '821323055621.dkr.ecr.us-east-1.amazonaws.com/hello-kohana:latest', 'sample-stage-service-003', 'sample-stage-container-003')
    #aws_ecs_instance.aws_ecs_delete_cluster("webservices-cluster32")
    

    
    