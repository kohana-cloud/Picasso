from src.aws_session import AWS_Session

if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    aws_internal_session.aws_ecr_add('test-repo', 'hello-kohana')
    #print(aws_internal_session.aws_ecr_list_repo())