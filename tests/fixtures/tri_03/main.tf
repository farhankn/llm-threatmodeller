resource "aws_db_instance" "app_db" {
  identifier            = "app-db"
  engine                = "postgres"
  publicly_accessible   = true
  skip_final_snapshot   = true
}
