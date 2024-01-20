module "lambda_function_container_image" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "translation-lambda"
  description   = "Provides the translation endpoint for the grammr application"

  create_package = false

  image_uri    = "${module.ecr.repository_url}:latest"
  package_type = "Image"

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

variable "openai_api_key" {
  type = string
}