module "ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "${var.name}-lambda"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [
    data.aws_caller_identity.current.arn,
    module.lambda_function_container_image.lambda_role_arn
  ]

  repository_lifecycle_policy = local.repository_lifecycle_policy
}

locals {
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep 3 images",
        selection    = {
          tagStatus     = "untagged",
          countType     = "imageCountMoreThan",
          countNumber   = 2
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}