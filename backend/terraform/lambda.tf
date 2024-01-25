module "translation" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "translation-lambda"
  description   = "Provides the /translation endpoint for the grammr application"

  create_package         = false
  local_existing_package = "../package_generative.zip"
  handler                = "lambda_functions_generative.translation_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout                                 = 5
  create_current_version_allowed_triggers = false
  allowed_triggers                        = local.allowed_triggers
  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

module "literal_translation" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "literal-translation-lambda"
  description   = "Provides the /literal-translation endpoint for the grammr application"

  create_package         = false
  local_existing_package = "../package_generative.zip"
  handler                = "lambda_functions_generative.literal_translation_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout                                 = 10
  memory_size                             = 512
  create_current_version_allowed_triggers = false
  allowed_triggers                        = local.allowed_triggers
  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

module "response_suggestion" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "response-suggestion-lambda"
  description   = "Provides the /response-suggestion endpoint for the grammr application"

  create_package         = false
  local_existing_package = "../package_generative.zip"
  handler                = "lambda_functions_generative.response_suggestion_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout     = 5
  memory_size = 256

  create_current_version_allowed_triggers = false
  allowed_triggers                        = local.allowed_triggers
  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

variable "openai_api_key" {
  type = string
}

locals {
  allowed_triggers = {
    apigateway = {
      service    = "apigateway"
      source_arn = "arn:aws:execute-api:eu-central-1:246770851643:*"
    }
  }
}